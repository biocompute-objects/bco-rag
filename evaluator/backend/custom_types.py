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
        "generated_directory_paths": generated_directory_paths,
        "padding": padding,
        "font": font,
    }
    return return_data


StateKey = Literal[
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
    "user_hash"
]


class AppState(AppAttributes):
    """Holds the application state information, essentially
    just the attributes plus the current user hash.
    """

    user_hash: str


def create_app_state(attributes: AppAttributes, user_hash: str) -> AppState:
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
        "generated_directory_paths": attributes["generated_directory_paths"],
        "padding": attributes["padding"],
        "font": attributes["font"],
        "user_hash": user_hash,
    }
    return return_data
