"""Handles the custom types for the App backend.
"""

from typing import TypedDict, Literal
from logging import Logger


class ConfigData(TypedDict):
    """Defines the schema for the JSON config data."""

    logger_path: str
    logger_name: str
    generated_output_dir_path: str
    glob_pattern: str
    results_dir_path: str
    ignore_files: list[str]
    bco_results_file_name: str
    user_results_file_name: str
    users_file_name: str
    padding: int
    font: str


class AppAttributes(TypedDict):
    """Handles the app initialization attributes."""

    logger: Logger
    results_dir_path: str
    bco_results_file_name: str
    bco_results_data: dict
    user_results_file_name: str
    user_results_data: dict
    users_file_name: str
    users_data: dict
    generated_output_dir_root: str
    generated_directory_paths: list[str]
    padding: int
    font: str


def create_app_attributes(
    logger: Logger,
    results_dir_path: str,
    bco_results_file_name: str,
    bco_results_data: dict,
    user_results_file_name: str,
    user_results_data: dict,
    users_file_name: str,
    users_data: dict,
    generated_output_dir_root: str,
    generated_directory_paths: list[str],
    padding: int,
    font: str,
) -> AppAttributes:
    """Constructor for the AppAttributes TypedDict."""
    return_data: AppAttributes = {
        "logger": logger,
        "results_dir_path": results_dir_path,
        "bco_results_file_name": bco_results_file_name,
        "bco_results_data": bco_results_data,
        "user_results_file_name": user_results_file_name,
        "user_results_data": user_results_data,
        "users_file_name": users_file_name,
        "users_data": users_data,
        "generated_output_dir_root": generated_output_dir_root,
        "generated_directory_paths": generated_directory_paths,
        "padding": padding,
        "font": font,
    }
    return return_data


AppStateKey = Literal[
    "logger",
    "results_dir_path",
    "bco_results_file_name",
    "bco_results_data",
    "user_results_file_name",
    "user_results_data",
    "users_file_name",
    "users_data",
    "generated_directory_paths",
    "padding",
    "font",
    "user_hash",
]


class AppState(AppAttributes):
    """Holds the application state information, essentially
    just the attributes plus the current user hash, new user
    flag and start from last session boolean.
    """

    user_hash: str
    new_user: bool
    resume_session: bool


def create_app_state(
    attributes: AppAttributes,
    user_hash: str,
    new_user: bool,
    resume_session: bool = False,
) -> AppState:
    """Constructor for the AppState TypedDict."""
    return_data: AppState = {
        "logger": attributes["logger"],
        "results_dir_path": attributes["results_dir_path"],
        "bco_results_file_name": attributes["bco_results_file_name"],
        "bco_results_data": attributes["bco_results_data"],
        "user_results_file_name": attributes["user_results_file_name"],
        "user_results_data": attributes["user_results_data"],
        "users_file_name": attributes["users_file_name"],
        "users_data": attributes["users_data"],
        "generated_output_dir_root": attributes["generated_output_dir_root"],
        "generated_directory_paths": attributes["generated_directory_paths"],
        "padding": attributes["padding"],
        "font": attributes["font"],
        "user_hash": user_hash,
        "new_user": new_user,
        "resume_session": resume_session,
    }
    return return_data


RunStateKey = Literal[
    "domain",
    "generated_domain",
    "generated_file_path",
    "human_curated_domain",
    "param_set",
    "reference_nodes",
    "run_index",
    "total_runs",
    "already_evaluated",
    "logger",
]


class RunState(TypedDict):
    """Holds the data for the current run being evaluated."""

    domain: str
    generated_domain: str
    generated_file_path: str
    human_curated_domain: dict
    param_set: str
    reference_nodes: str
    run_index: int
    total_runs: int
    already_evaluated: bool
    logger: Logger


def create_run_state(
    domain: str,
    generated_domain: str,
    generated_file_path: str,
    human_curated_domain: dict,
    param_set: str,
    reference_nodes: str,
    run_index: int,
    total_runs: int,
    already_evaluated: bool,
    logger: Logger,
) -> RunState:
    """Constructor for the RunState TypedDict."""
    return_data: RunState = {
        "domain": domain,
        "generated_domain": generated_domain,
        "generated_file_path": generated_file_path,
        "human_curated_domain": human_curated_domain,
        "param_set": param_set,
        "reference_nodes": reference_nodes,
        "run_index": run_index,
        "total_runs": total_runs,
        "already_evaluated": already_evaluated,
        "logger": logger,
    }
    return return_data
