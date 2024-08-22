""" Simple CLI interface for choosing one of the pre-selected baseline testing paper. 
Will automatically grab any PDF file in the `../../papers/` directory. 
"""

import os
from pick import pick
from bcorag import misc_functions as misc_fns
from typing import Literal, Tuple, Optional, get_args
from .custom_types.core_types import (
    UserSelections,
    GitData,
    GitFilter,
    GitFilters,
    create_git_data,
    create_git_filters,
    OptionKey,
)
from llama_index.readers.github import GithubRepositoryReader  # type: ignore

EXIT_OPTION = "Exit"


def initialize_picker(filetype: str = "pdf") -> Optional[UserSelections]:
    """Kicks off the initial pipeline step where the user picks their
    PDF file to index and chooser the data loader from a pre-set list.

    Parameters
    ----------
    filetype : str, optional
        The filetype to filter on, this project was build to handle PDF
        files so it is highly unlikely you will want to override this default.

    Returns
    -------
    UserSelections | None
        The user selections or None indicating user chose to exit or error.
    """

    presets = misc_fns.load_config_data("./bcorag/conf.json")
    if presets is None or isinstance(presets, list):
        print(f"Error reading config file. Got type `{type(presets)}` for `presets`.")
        misc_fns.graceful_exit()

    # set base keys
    return_data: UserSelections = {  # type: ignore
        f"{option}": None for option in presets["options"].keys()
    }

    target_file_information = _file_picker(presets["paper_directory"], filetype)
    if target_file_information is None:
        return None
    return_data["filename"] = target_file_information[0]
    return_data["filepath"] = target_file_information[1]

    option: OptionKey
    for option in get_args(OptionKey):
        target_option = _create_picker(
            option,
            presets["options"][option]["documentation"],
            presets["options"][option]["list"],
            presets["options"][option].get("default", None),
        )
        if target_option is None:
            return None
        return_data[option] = int(target_option) if option in {"similarity_top_k"} else target_option  # type: ignore

    repo_data = _repo_picker()
    if repo_data == 0:
        return None
    if repo_data is None:
        return_data["git_data"] = None
    else:
        return_data["git_data"] = repo_data

    in_progress_docs_path = _in_progress_docs()
    if in_progress_docs_path:
        return_data["other_docs"] = [in_progress_docs_path]

    return return_data


def _file_picker(path: str, filetype: str = "pdf") -> Optional[Tuple[str, str]]:
    """Create the CLI menu to pick the PDF file from the papers directory.

    Parameters
    ----------
    path : str
        The path to the directory to display the CLI menu for.
    filetype : str, optional
        The filetype to filter on, this project was build to handle PDF
        files so it is highly unlikely you will want to override this default.

    Returns
    -------
    (str, str) | None
        Returns the name and path of the selected file or None if the user selects exit.
    """
    target_files = misc_fns.get_file_list(path, filetype)
    pick_options = [os.path.basename(filename) for filename in target_files]
    pick_options.append(EXIT_OPTION)
    pick_title = "Please choose the PDF file to index:"
    option, _ = pick(pick_options, pick_title, indicator="->")
    option = str(option)
    if option == EXIT_OPTION:
        return None
    return str(option), f"{path}{option}"


def _repo_picker() -> Optional[GitData] | Literal[0]:
    """Allows the user to input a github repository link to be included in the indexing.

    Returns
    -------
    GitData | None | 0
        Returns parsed repo information from the link, None if the user skips this step,
        or 0 (exit status) if the user chooses to exit.
    """

    while True:

        url_prompt = 'If you would like to include a Github repository enter the URL below. Enter "x" to exit or leave blank to skip.\n> '
        url = input(url_prompt)
        if not url or url is None:
            print("Skipping Github repo...")
            return None
        elif url == "x":
            return 0

        match = misc_fns.extract_repo_data(url)
        if match is None:
            print("Error parsing repository URL.")
            continue
        user = match[0]
        repo = match[1]

        branch = input("Repo branch to index (case sensitive):\n> ")
        if not branch:
            branch = "main"

        git_filters: list[GitFilters] = []

        directory_filter_prompt = "Would you like to include a directory filter?"
        directory_filter_prompt += "\nEnter a list of comma-delimited directories to either conditionally exclude or inclusively include. "
        directory_filter_prompt += "Or leave blank to skip.\n> "
        directory_filter_val = input(directory_filter_prompt)
        if directory_filter_val and directory_filter_val is not None:
            directories = [
                dir.strip() for dir in directory_filter_val.split(",") if dir.strip()
            ]
            directory_filter_condition_prompt = (
                'Enter "include" or "exclude" for the directory filter.\n> '
            )
            directory_filter_condition_val = input(directory_filter_condition_prompt)
            directory_filter_type = (
                GithubRepositoryReader.FilterType.INCLUDE
                if directory_filter_condition_val.lower().strip() == "include"
                else GithubRepositoryReader.FilterType.EXCLUDE
            )
            directory_filter = create_git_filters(directory_filter_type, GitFilter.DIRECTORY, value=directories)
            git_filters.append(directory_filter)

        file_ext_filter_prompt = "Would you like to include a file extension filter?"
        file_ext_filter_prompt += "\nEnter a list of comma-delimited file extensions to either conditionally exclude or inclusively include. "
        file_ext_filter_prompt += "Or leave blank to skip.\n> "
        file_ext_filter_val = input(file_ext_filter_prompt)
        if file_ext_filter_val and file_ext_filter_val is not None:
            file_exts = [
                ext.strip() for ext in file_ext_filter_val.split(",") if ext.strip()
            ]
            file_ext_filter_condition_prompt = (
                'Enter "include" or "exclude" for the file extension filter.\n> '
            )
            file_ext_filter_condition_val = input(file_ext_filter_condition_prompt)
            file_ext_filter_type = (
                GithubRepositoryReader.FilterType.INCLUDE
                if file_ext_filter_condition_val.lower().strip() == "include"
                else GithubRepositoryReader.FilterType.EXCLUDE
            )
            file_ext_filter = create_git_filters(file_ext_filter_type, GitFilter.FILE_EXTENSION, value=file_exts)
            git_filters.append(file_ext_filter)

        return_data = create_git_data(user, repo, branch, git_filters)
        return return_data


def _create_picker(
    title_keyword: str,
    documentation: str,
    option_list: list[str],
    default: Optional[str] = None,
) -> Optional[str]:
    """Creates a general picker CLI based on a list of options and the
    functionality to optionally mark one option as the default.

    Parameters
    ----------
    title_keyword : str
        The keyword to use for the picker title.
    documentation : str
        Link to the documentation for the option.
    option_list : list[str]
        The list of options to display in the picker menu.
    default : str | None, optional
        The option to mark one option as the default.

    Returns
    -------
    str | None
        The chosen option of None if the user selected to exit.
    """
    pick_title = f"Please choose one of the following {title_keyword.replace('_', ' ').title()}s.\nDocumentation can be found at:\n{documentation}."
    pick_options = [
        f"{option} (default)" if option == default else option for option in option_list
    ]
    pick_options.append(EXIT_OPTION)
    option, _ = pick(pick_options, pick_title, indicator="->")
    option = str(option)
    if option == EXIT_OPTION:
        return None
    if " (default)" in option:
        option = option.replace(" (default)", "")
    return option

def _in_progress_docs() -> Optional[str]:
    """Checks if in progress documentation is found.
    
    Returns
    -------
    str or None
        The file path to the in progress documentation to include or None
        if the user chose not to include or no documentation was found.
    """
    in_progress_docs_path = os.path.join(os.getcwd(), "aggregator", "summary.md")
    if os.path.isfile(in_progress_docs_path):
        prompt = "Found summary.md, include it in the vector store? (y/n)\n> "
        answer = input(prompt)
        answer = answer.strip().lower()
        if answer == "y":
            return in_progress_docs_path
    return None
