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
MAX_TOKENS = 110_000  # leave 28k tokens for instructions, responses, etc
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

        token_count = self._count_tokens(prompt)
        print(f"Total prompt token count: {token_count}")

        if token_count <= MAX_TOKENS:
            self._process_prompt(prompt)
        else:
            chunks = self._split_prompt(prompt)
            self._process_chunks(chunks)

    def _process_prompt(self, prompt: str) -> None:
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
            response_content = response.choices[0].message.content
            with open(OUTPUT_PATH, "w") as out_file:
                if response_content:
                    out_file.write(response_content)

        except Exception as e:
            error_msg = f"Unexpected error in generating summary.\n{e}"
            graceful_exit(1, error_msg)

    def _split_prompt(self, prompt: str) -> list[str]:
        """Split a large prompt into smaller chunks that fit within the token limit.

        Parameters
        ----------
        prompt : str
            The original prompt to be split.

        Returns
        -------
        list[str]
            A list of prompt chunks, each within the token limit.
        """
        chunks = []
        current_chunk = ""
        lines = prompt.split("\n")

        for line in lines:
            if self._count_tokens(current_chunk + line + "\n") > MAX_TOKENS:
                chunks.append(current_chunk)
                current_chunk = f"{line}\n"
            else:
                current_chunk += f"{line}\n"

        if current_chunk:
            chunks.append(current_chunk)

        return chunks

    def _process_chunks(self, chunks: list[str]) -> None:
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
        full_response = ""
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
                full_response += f"{response.choices[0].message.content} + \n\n"
            except Exception as e:
                graceful_exit(
                    1, f"Unexpected error in generating summary for chunk {i + 1}.\n{e}"
                )

        with open(OUTPUT_PATH, "w") as out_file:
            out_file.write(full_response)

    def _count_tokens(self, text: str) -> int:
        """Count the number of tokens in the given text.

        Parameters
        ----------
        text : str
            The text to count tokens for.

        Returns
        -------
        int
            The number of tokens in the text.
        """
        encoding = tiktoken.encoding_for_model(MODEL)
        return len(encoding.encode(text))
