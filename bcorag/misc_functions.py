""" Miscellaneous helper functions.
"""

import sys
import json
import csv
import logging
import os
import datetime
import pytz
from typing import Optional, NoReturn, cast, get_args
from . import TIMEZONE, TIMESTAMP_FORMAT
from .custom_types import OutputTrackerFile, DomainKey


def graceful_exit() -> NoReturn:
    """Gracefully exits the program with a 0 exit code."""
    print("Exiting...")
    logging.info("Exiting with status code 0.")
    logging.info(
        "---------------------------------- RUN END ----------------------------------"
    )
    sys.exit(0)


def load_json(filepath: str) -> Optional[dict]:
    """Loads a JSON file and returns the deserialized data (or
    an empty dict if the file doesn't exist).

    Parameters
    ----------
    filepath : str
        File path to the JSON file to load.

    Returns
    -------
    dict or None
        The deserialized JSON data or None if the file doesn't exist.
    """
    if not os.path.isfile(filepath):
        return None
    with open(filepath, "r") as f:
        data = json.load(f)
        return data


def load_output_tracker(filepath: str) -> Optional[OutputTrackerFile]:
    """Loads the JSON output tracker file or returns None if it doesn't
    exist (or on some other unforeseen error).

    Parameters
    ----------
    filepath : str
        File path to the JSON file to load.

    Returns
    -------
    OutputTrackerFile or None
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
    data : dict or list
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
                        entry["txt_file"],
                        entry["json_file"],
                        entry["source_node_file"],
                        entry_set["hash_str"],
                        entry_set["entries"]["params"]["loader"],
                        entry_set["entries"]["params"]["vector_store"],
                        entry_set["entries"]["params"]["llm"],
                        entry_set["entries"]["params"]["embedding_model"],
                        entry_set["entries"]["params"]["similarity_top_k"],
                        entry_set["entries"]["params"]["chunking_config"],
                        entry_set["entries"]["params"]["git_user"],
                        entry_set["entries"]["params"]["git_repo"],
                        entry_set["entries"]["params"]["git_branch"],
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
    name : str (default: "bcorag")
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
    parent_logger : str (default: "bcorag")
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
