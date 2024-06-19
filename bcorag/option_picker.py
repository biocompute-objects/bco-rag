""" Simple CLI interface for choosing one of the pre-selected baseline testing paper. 
Will automatically grab any PDF file in the ../../papers/ directory. 
"""

import glob
import os
import re
from pick import pick
from bcorag import misc_functions as misc_fns
from typing import Literal, Tuple, Optional
from .custom_types import UserSelections, GitData

EXIT_OPTION = "Exit"


def initialize_picker(filetype: str = "pdf") -> Optional[UserSelections]:
    """Kicks off the initial pipeline step where the user picks their
    PDF file to index and chooser the data loader from a pre-set list.

    Parameters
    ----------
    filetype : str (default: pdf)
        The filetype to filter on, this project was build to handle PDF
        files so it is highly unlikely you will want to override this default.

    Returns
    -------
    UserSelections or None
        The user selections or None indicating user chose to exit or error.
    """

    presets = misc_fns.load_json("./bcorag/conf.json")
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

    for option in presets["options"].keys():
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

    return return_data


def _file_picker(path: str, filetype: str = "pdf") -> Optional[Tuple[str, str]]:
    """Create the CLI menu to pick the PDF file from the papers directory.

    Parameters
    ----------
    path : str
        The path to the directory to display the CLI menu for.
    filetype : str (default: pdf)
        The filetype to filter on, this project was build to handle PDF
        files so it is highly unlikely you will want to override this default.

    Returns
    -------
    (str, str) or None
        Returns the name and path of the selected file or None if the user selects exit.
    """
    target_files = glob.glob(f"{path}*.{filetype}")
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
    GitData, None, or 0
        Returns parsed repo information from the link, None if the user skips this step,
        or 0 (exit status) if the user chooses to exit.
    """
    pattern = r"https://github\.com/([^/]+)/([^/]+)"
    while True:
        url = input(
            'If you would like to include a Github repository enter the URL below. Enter "x" to exit or leave blank to skip.\n'
        )
        url = url.strip()
        if not url or url is None:
            print("Skipping Github repo...")
            return None
        elif url == "x":
            return 0
        match = re.match(pattern, url.lower().strip())
        if match is None:
            print("Error parsing repository URL.")
            continue
        branch = input("Repo branch to index (case sensitive):\n")
        user = str(match.groups()[0].strip().lower())
        repo = str(match.groups()[1].strip().lower())
        return_data: GitData = {"user": user, "repo": repo, "branch": branch.strip()}
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
    default : str or None (default: None)
        The option to mark one option as the default.

    Returns
    -------
    str or None
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
