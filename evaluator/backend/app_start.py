"""Handles the app initilization procedure.
"""

from bcorag import misc_functions as misc_fns
from .custom_types import (
    ConfigData,
    AppAttributes,
    RunState,
    create_app_attributes,
    AppState,
)
from .state import load_run_state
from typing import Optional, cast
from glob import glob
import os


def initialization() -> AppAttributes:
    """Handles the app initialization process."""
    _config_data = _load_config_data()
    if _config_data is None:
        misc_fns.graceful_exit(1, "Error loading frontend configuration data.")

    logger = misc_fns.setup_root_logger(
        log_path=_config_data["logger_path"], name=_config_data["logger_name"]
    )
    logger.info(
        "################################## RUN START ##################################"
    )

    _raw_directory_paths = glob(
        os.path.join(
            _config_data["generated_output_dir_path"], _config_data["glob_pattern"]
        )
    )
    directory_paths = [
        x
        for x in _raw_directory_paths
        if not any(y in x for y in _config_data["ignore_files"])
    ]

    # load in existing evaluation data
    bco_results_data = misc_fns.load_json(
        os.path.join(
            _config_data["results_dir_path"], _config_data["bco_results_file_name"]
        )
    )
    user_results_data = misc_fns.load_json(
        os.path.join(
            _config_data["results_dir_path"], _config_data["user_results_file_name"]
        )
    )
    users_data = misc_fns.load_json(
        os.path.join(_config_data["results_dir_path"], _config_data["users_file_name"])
    )
    if bco_results_data is None or user_results_data is None or users_data is None:
        misc_fns.graceful_exit(1, "Error loading results files.")

    bco_results_data = _create_paper_keys(directory_paths, bco_results_data)

    app_attrs = create_app_attributes(
        logger=logger,
        results_dir_path=_config_data["results_dir_path"],
        bco_results_file_name=_config_data["bco_results_file_name"],
        bco_results_data=bco_results_data,
        user_results_file_name=_config_data["user_results_file_name"],
        user_results_data=user_results_data,
        users_file_name=_config_data["users_file_name"],
        users_data=users_data,
        generated_output_dir_root=_config_data["generated_output_dir_path"],
        generated_directory_paths=directory_paths,
        padding=_config_data["padding"],
        font=_config_data["font"],
    )

    return app_attrs


def create_init_run_state(app_state: AppState) -> RunState:
    """Creates the init run state.

    Parameters
    ----------
    app_state : AppState
        The current app state.

    Returns
    -------
    RunState
        The intial run state.
    """
    total_runs = _get_total_runs(app_state)
    run_state = load_run_state(run_index=0, total_runs=total_runs, app_state=app_state)
    return run_state


def _get_total_runs(app_state: AppState) -> int:
    """Get the total number of runs in the output directory.

    Parameters
    ----------
    app_state : AppState
        The current app state.

    Returns
    -------
    int
        The number of total potential generated domains
        to evaluate.
    """
    total_runs = 0
    for directory in app_state["generated_directory_paths"]:
        output_map = misc_fns.load_json(os.path.join(directory, "output_map.json"))
        if output_map is None:
            misc_fns.graceful_exit(
                1,
                f"Error: Output map not found in directory `{directory}` while calculating total runs.",
            )
        for domain in output_map:
            for domain_param_set in output_map[domain]:
                total_runs += len(domain_param_set["entries"]["runs"])
    return total_runs


def _create_paper_keys(directory_paths: list[str], bco_results_data: dict) -> dict:
    """Creates an entry for each paper in the evaluations file.

    Parameters
    ----------
    directory_paths : list [str]
        Path to the generated BCO directories.
    bco_results_data : dict
        The loaded BCO evaluations results file.

    Returns
    -------
    dict
        The updated BCO evaluations data.
    """
    directory_basenames = [os.path.basename(x) for x in directory_paths]
    for paper in directory_basenames:
        if paper not in bco_results_data:
            bco_results_data[paper] = {}
    return bco_results_data


def _load_config_data(
    filepath: str = "./evaluator/backend/conf.json",
) -> Optional[ConfigData]:
    """Loads the App configuration data.

    Parameters
    ----------
    filepath : str, optional
        Filepath to the App config data.

    Returns
    -------
    ConfigData | None
        The configuration data on success, None on error.
    """
    naive_load_data = misc_fns.load_json(filepath)
    if naive_load_data is None:
        return None
    if isinstance(naive_load_data, dict):
        config_object = cast(ConfigData, naive_load_data)
        return config_object
    return None
