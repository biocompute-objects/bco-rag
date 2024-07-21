""" Miscellaneous util functions.
"""

import sys
import re
import glob
import json
import csv
import logging
import os
import datetime
import pytz
from typing import Optional, NoReturn, cast, get_args
from . import TIMEZONE, TIMESTAMP_FORMAT
from .custom_types.core_types import DomainKey, ConfigObject
from .custom_types.output_map_types import OutputTrackerFile


def graceful_exit(exit_code: int = 0, error_msg: Optional[str] = None) -> NoReturn:
    """Gracefully exits the program with an exit code.

    Parameters
    ----------
    exit_code : int, optional
        The exit code.
    error_msg : str | None, optional
        The error message to print before exiting.
    """
    if exit_code != 0:
        if error_msg is not None:
            print(f"{error_msg}")
        print(f"exit code: {exit_code}")
    print("Exiting...")
    logging.info(f"Exiting with status code {exit_code}.")
    logging.info(
        "---------------------------------- RUN END ----------------------------------"
    )
    sys.exit(exit_code)


def load_json(filepath: str) -> Optional[dict]:
    """Loads a JSON file and returns the deserialized data (or
    an empty dict if the file doesn't exist).

    Parameters
    ----------
    filepath : str
        File path to the JSON file to load.

    Returns
    -------
    dict | None
        The deserialized JSON data or None if the file doesn't exist.
    """
    if not os.path.isfile(filepath):
        return None
    with open(filepath, "r") as f:
        data = json.load(f)
        return data


def load_config_data(filepath: str = "./conf.json") -> Optional[ConfigObject]:
    """Loads the config JSON object file.

    Parameters
    ----------
    filepath : str, optional
        File path to the config JSON file.

    Returns
    -------
    ConfigObject | None
        Casted ConfigObject or None on some type of error.
    """
    naive_load_data = load_json(filepath)
    if naive_load_data is None:
        return None
    if isinstance(naive_load_data, dict):
        config_object = cast(ConfigObject, naive_load_data)
        return config_object
    return None


def load_output_tracker(filepath: str) -> Optional[OutputTrackerFile]:
    """Loads the JSON output tracker file.

    Parameters
    ----------
    filepath : str
        File path to the JSON file to load.

    Returns
    -------
    OutputTrackerFile | None
        Casted OutputTrackerFile or None on some type of error.
    """
    naive_load_data = load_json(filepath)
    if naive_load_data is None:
        return None
    if isinstance(naive_load_data, dict):
        output_tracker_data = cast(OutputTrackerFile, naive_load_data)
        return output_tracker_data
    return None


def write_json(output_path: str, data: dict | list | OutputTrackerFile) -> bool:
    """Writes JSON out to the output path. Will create the file if it doesn't exist.

    Parameters
    ----------
    output_path : str
        The output file path.
    data : dict | list | OutputTrackerFile
        The data to dump.

    Returns
    -------
    bool
        Whether the process was successful.
    """
    try:
        with open(output_path, "w") as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        logging.error(f"Failed to dump JSON to output path '{output_path}'.\n{e}")
        return False


def dump_output_file_map_tsv(output_path: str, data: OutputTrackerFile):
    """Dumps the OutputTrackerFile object into a TSV table for better
    human readability.

    Parameters
    ----------
    output_path : str
        The output file path.
    data: OutputTrackerFile
        The OutputTrackerFile object to format for a TSV file.
    """
    with open(output_path, mode="w", newline="") as out_file:
        tsv_writer = csv.writer(out_file, delimiter="\t")
        tsv_writer.writerow(
            [
                "timestamp",
                "domain",
                "txt_file",
                "json_file",
                "node_source_file",
                "hash_string",
                "index",
                "loader",
                "vector_store",
                "llm",
                "embedding_model",
                "similarity_top_k",
                "chunking_config",
                "git_user",
                "git_repo",
                "git_branch",
                "directory_filter",
                "file_ext_filter",
                "elapsed_time",
                "version",
            ]
        )
        domain: DomainKey
        for domain in get_args(DomainKey):
            domain_entry_list = data[domain]
            for entry_set in domain_entry_list:
                for entry in entry_set["entries"]["runs"]:
                    row = [
                        entry["timestamp"],
                        domain,
                        os.path.basename(entry["txt_file"]),
                        os.path.basename(entry["json_file"]),
                        os.path.basename(entry["source_node_file"]),
                        entry_set["hash_str"],
                        entry["index"],
                        entry_set["entries"]["params"]["loader"],
                        entry_set["entries"]["params"]["vector_store"],
                        entry_set["entries"]["params"]["llm"],
                        entry_set["entries"]["params"]["embedding_model"],
                        entry_set["entries"]["params"]["similarity_top_k"],
                        entry_set["entries"]["params"]["chunking_config"],
                        entry_set["entries"]["params"]["git_user"],
                        entry_set["entries"]["params"]["git_repo"],
                        entry_set["entries"]["params"]["git_branch"],
                        entry_set["entries"]["params"]["directory_git_filter"],
                        entry_set["entries"]["params"]["file_ext_git_filter"],
                        entry["elapsed_time"],
                        entry["version"],
                    ]
                    tsv_writer.writerow(row)


def dump_string(output_path: str, data: str):
    """Dumps a string to a text file.

    Parameters
    ----------
    output_path : str
        The output file path.
    data: str
        The string to dump.
    """
    check_dir(os.path.split(output_path)[0])
    with open(output_path, "w") as f:
        f.write(data)


def check_dir(path: str):
    """Checks whether a directory creates and if it doesn't, create it. Note, this
    really only works for checking/creating the last level direcotry. Will fail if
    there are issues in the parent level directories in the path.

    Parameters
    ----------
    path : str
        Directory filepath to check.
    """
    if not os.path.isdir(path):
        os.mkdir(path)


def setup_root_logger(log_path: str, name: str = "bcorag") -> logging.Logger:
    """Configures the root logger.

    Parameters
    ----------
    log_path : str
        The filepath to the log handler.
    name : str, optional
        The name of the root logger.

    Returns
    -------
    logging.Logger
        The root logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename=log_path, encoding="utf-8", mode="w")
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def setup_document_logger(name: str, parent_logger: str = "bcorag") -> logging.Logger:
    """Configures a document specific logger.

    Parameters
    ----------
    name : str
        The name of the document to setup the logger for.
    parent_logger : str, optional
        Name of the parent logger to setup under.

    Returns
    -------
    logging.Logger
        The document logger.
    """
    document_logger_name = f"{parent_logger}.{name}"
    return logging.getLogger(document_logger_name)


def create_timestamp() -> str:
    """Creates a current timestamp.

    Returns
    -------
    str
        The current timestamp as a string.
    """
    timestamp = datetime.datetime.now(pytz.timezone(TIMEZONE)).strftime(
        TIMESTAMP_FORMAT
    )
    return timestamp


def extract_repo_data(url: str) -> Optional[tuple[str, str]]:
    """Extracts the repository information from the repo URL.

    Parameters
    ----------
    url : str
        The Github repository URL.

    Returns
    -------
    (str, str) | None
        Returns the tuple containing the extracted github user
        and repo or None on failure to parse the URL.
    """
    url = url.strip().lower()
    pattern = r"https://github\.com/([^/]+)/([^/]+)"
    match = re.match(pattern, url)
    if match is None:
        return None
    user = str(match.groups()[0])
    repo = str(match.groups()[1])
    return user, repo


def get_file_list(path: str, filetype: str = "pdf") -> list[str]:
    """Gets the files from a glob pattern.

    Parameters
    ----------
    path : str
        The file path to the target directory.
    filetype : str, optional
        The file type to capture.

    Returns
    -------
    list[str]
        List of the file paths found from the glob pattern.
    """
    target_files = glob.glob(os.path.join(path, f"*.{filetype}"))
    return target_files
