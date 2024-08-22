""" Handles the in progress documentation generator.
"""

import subprocess
import platform
import os
from dotenv import load_dotenv
from typing import Optional
from openai import OpenAI
import tiktoken
from bcorag.misc_functions import graceful_exit

# Mapping of operating systems and architectures to their respective binary filenames
BINARY_MAP = {
    "windows": {"x86_64": "codeprompt-Windows-x86_64.exe"},
    "linux": {"x86_64": "codeprompt-Linux-x86_64"},
    "darwin": {"x86_64": "codeprompt-macOS-Intel", "arm64": "codeprompt-macOS-ARM"},
}
PROMPT_PATH = os.path.join(os.path.dirname(__file__), "prompt.md")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "summary.md")
MAX_TOKENS = 115_000  # leave 28k tokens for instructions, responses, etc
MODEL = "gpt-4o-mini"
SYSTEM_PROMPT = "You are an assistant that helps summarize in progress project's into plain text documentation which follows the general structure of a BioCompute Object."


class Aggregator:
    """Classs to handle the in progress documentation of a repository. Processes the work done so far in a
    code repository and generates plain text documentation on the project that resembles a plain text Biocompute
    Object.

    Attributes
    ----------
    path: str
        Path to the directory to process.
    include: str
        Comma delimited list of glob patterns to include in processing.
    exclude: str
        Comma delimited list of glob patterns to exclude in processing.
    include_priority : bool
        Determines whether to prioritize the include or exclude pattern
        in the case that include and exclude patterns conflict.
    exclude_from_tree : bool
        Whether to exclude excluded files from the source tree path for
        prompt generation.
    client : OpenAI
        OpenAI API client.
    encoding : Encoding
        The encoding for the LLM.
    """

    def __init__(
        self,
        path: str,
        include: Optional[str],
        exclude: Optional[str],
        include_priority: bool = False,
        exclude_from_tree: bool = False,
    ):
        """Constructor.

        Parameters
        ----------
        path: str
            Path to the directory to process.
        include: str
            Comma delimited list of glob patterns to include in processing.
        exclude: str
            Comma delimited list of glob patterns to exclude in processing.
        include_priority : bool, optional
            Determines whether to prioritize the include or exclude pattern
            in the case that include and exclude patterns conflict.
        exclude_from_tree : bool, optional
            Whether to exclude excluded files from the source tree path for
            prompt generation.
        """
        load_dotenv()
        self.path = path
        self.include = include
        self.exclude = exclude
        self.include_priority = include_priority
        self.exclude_from_tree = exclude_from_tree
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.encoding = tiktoken.encoding_for_model(MODEL)

        host_os = platform.system().lower()
        machine = platform.machine().lower()
        if host_os not in BINARY_MAP:
            graceful_exit(1, f"OS `{os}` not supported.")
        if machine not in BINARY_MAP[host_os]:
            graceful_exit(1, f"{os} architecture for `{machine}` not supported.")

        self._binary_path = os.path.join(
            os.path.dirname(__file__), "binaries", BINARY_MAP[host_os][machine]
        )

    def get_prompt(self) -> str:
        """Calls the codeprompt binary and generates the LLM prompt."""
        cmd = [self._binary_path, self.path]

        if self.include:
            cmd.extend(["--include", f"{self.include}"])
        if self.exclude:
            cmd.extend(["--exclude", f"{self.exclude}"])
        if self.include_priority:
            cmd.append("--include-priority")
        if self.exclude_from_tree:
            cmd.extend(["--exclude-from-tree"])
        cmd.extend(["--output", PROMPT_PATH])
        cmd.extend(["-t", os.path.join(os.path.dirname(__file__), "template.hbs")])
        cmd.append("--no-clipboard")
        cmd.append("--spinner")
        cmd.append("--line-numbers")
        cmd.append("--tokens")

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            error_msg = (
                f"Command '{e.cmd}' returned non-zero exit status {e.returncode}."
            )
            error_msg += f"\nError output:\n{e.stderr}"
        except Exception as e:
            error_msg = f"Unexpected error in generating prompt.\n{e}"
        graceful_exit(1, error_msg)

    def generate_summary(self) -> None:
        """Entry point for generating the LLM documentation."""
        if not os.path.isfile(PROMPT_PATH):
            graceful_exit(1, f"No prompt found at `{PROMPT_PATH}`.")
        with open(PROMPT_PATH, "r") as f:
            prompt = f.read()

        tokens = self._count_tokens(prompt)
        token_count = len(tokens)
        print(f"Total prompt token count: {token_count}")

        if token_count <= MAX_TOKENS:
            response = self._process_prompt(prompt)
        else:
            print(
                f"Warning: Prompt size exceeds the max tokens limit ({MAX_TOKENS}), response will still be generated but will likely be somewhat degraded in quality. Consider limiting the include patterns."
            )
            chunks = self._split_prompt(tokens, token_count)
            responses = self._process_chunks(chunks)
            response = self._combine_responses(responses)
        
        self._write_output(response)

    def _process_prompt(self, prompt: str) -> str:
        """Process a single prompt using the OpenAI API.

        Parameters
        ----------
        prompt : str
            The prompt to be processed.

        Raises
        ------
        Exception
            If there's an unexpected error in generating the summary.
        """
        try:
            response = self.client.chat.completions.create(
                model=MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT,
                    },
                    {"role": "user", "content": prompt},
                ],
            )
            response_txt = (
                response.choices[0].message.content
                if response.choices[0].message.content
                else ""
            )

        except Exception as e:
            error_msg = f"Unexpected error in generating summary.\n{e}"
            graceful_exit(1, error_msg)

        return response_txt

    def _split_prompt(self, tokens: list[int], token_count: int) -> list[str]:
        """Split a large prompt into smaller chunks that fit within the token limit.

        Parameters
        ----------

        Returns
        -------
        list[str]
            A list of prompt chunks, each within the token limit.
        """
        print("Splitting prompt...")
        chunks = []

        start = 0
        while start < token_count:
            end = min(start + MAX_TOKENS, token_count)
            if end < token_count:
                split_range = max(10, int(MAX_TOKENS * 0.1))
                for i in range(end, end - split_range, -1):
                    if tokens[i] == self.encoding.encode("\n")[0]:
                        end = i + 1
                        break

            chunk_tokens = tokens[start:end]
            chunks.append(self.encoding.decode(chunk_tokens))
            start = end

        print(f"Split into {len(chunks)} chunks")
        return chunks

    def _process_chunks(self, chunks: list[str]) -> list[str]:
        """Process multiple prompt chunks and combine their responses.

        Parameters
        ----------
        chunks : list[str]
            A list of prompt chunks to be processed.

        Raises
        ------
        Exception
            If there's an unexpected error in generating the summary for any chunk.
        """
        responses: list[str] = []
        for i, chunk in enumerate(chunks):
            try:
                response = self.client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {
                            "role": "system",
                            "content": f"{SYSTEM_PROMPT} This is part {i + 1} of {len(chunks)}.",
                        },
                        {"role": "user", "content": chunk},
                    ],
                )
                response_txt = (
                    response.choices[0].message.content
                    if response.choices[0].message.content
                    else ""
                )
                responses.append(response_txt)
            except Exception as e:
                graceful_exit(
                    1, f"Unexpected error in generating summary for chunk {i + 1}.\n{e}"
                )
        return responses

    def _combine_responses(self, responses: list[str]) -> str:
        combine_prompt = f"""
        You are tasked with combining multiple responses into cohesive BioCompute Object-like (BCO) documentation. 
        The BCO-like plain text documentation should include the following domains:
        - Usability Domain
        - IO Domain
        - Description Domain
        - Execution Domain
        - Parametric Domain
        - Error Domain

        Here are the responses to combine:

        {' '.join(responses)}

        Please structure the information into a single, coherent BCO documentation, ensuring that:
        1. All relevant information from the responses is included.
        2. The information is organized under the appropriate BCO domains.
        3. Any redundant information is removed.
        4. The final document flows logically and reads cohesively.
        5. If specific information for a domain isn't available, mention that in the respective section.

        Format the output as markdown, with each domain as a second-level header (##).
        """
        try:
            response = self.client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": combine_prompt},
                ],
            )
            return (
                response.choices[0].message.content
                if response.choices[0].message.content
                else ""
            )
        except Exception as e:
            graceful_exit(1, f"{e}\nUnexpected error in combining responses.")

    def _count_tokens(self, text: str) -> list[int]:
        """Count the number of tokens in the given text.

        Parameters
        ----------
        text : str
            The text to count tokens for.

        Returns
        -------
        list[int]
            The number of tokens in each line of the text.
        """
        return self.encoding.encode(text)

    def _write_output(self, content: str) -> None:
        with open(OUTPUT_PATH, "w") as out_file:
            out_file.write(content)
