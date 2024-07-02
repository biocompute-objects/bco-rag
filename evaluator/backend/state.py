"""Handles all app and run state changes."""

import os
import json
from bcorag import misc_functions as misc_fns
from .custom_types import AppState, RunState, create_run_state
from .miscellaneous import log_state


def create_new_user(app_state: AppState, first_name: str, last_name: str) -> AppState:
    """Creates a new user.

    Parameters
    ----------
    app_state : AppState
        The current app state.
    first_name : str
        The user's first name.
    last_name : str
        The user's last name.

    Returns
    -------
    AppState
        The updated app state.
    """
    app_state["logger"].info(f"Creating new user for {last_name}, {first_name}")
    app_state["users_data"][app_state["user_hash"]] = {
        "first_name": first_name,
        "last_name": last_name,
    }
    app_state["user_results_data"][app_state["user_hash"]] = {}
    return app_state


def set_resume_session(app_state: AppState, resume_session: bool) -> AppState:
    """Sets the resume session boolean.

    Parameters
    ----------
    app_state : AppState
        The current app state.
    resume_session : bool
        The resume_session value to set.

    Returns
    -------
    AppState
        The updated app state.
    """
    app_state["resume_session"] = resume_session
    return app_state


def save_state(app_state: AppState) -> None:
    """Saves the state.

    Parameters
    ----------
    app_state : AppState
        The app state to save.
    """
    app_state["logger"].info("Writing data...")
    misc_fns.write_json(
        output_path=os.path.join(
            app_state["results_dir_path"], app_state["bco_results_file_name"]
        ),
        data=app_state["bco_results_data"],
    )
    misc_fns.write_json(
        output_path=os.path.join(
            app_state["results_dir_path"], app_state["user_results_file_name"]
        ),
        data=app_state["user_results_data"],
    )
    misc_fns.write_json(
        output_path=os.path.join(
            app_state["results_dir_path"], app_state["users_file_name"]
        ),
        data=app_state["users_data"],
    )


def load_run_state(run_index: int, total_runs: int, app_state: AppState) -> RunState:
    """Create run state.

    Parameters
    ----------
    run_index : int
        The run index to load from.
    total_runs : int
        The total number of potential evaluation runs.
    app_state : AppState
        The current app state.

    Returns
    -------
    tuple (dict, dict)
        The generated domain dict and the human curated domain dict.
    """
    current_run = 0

    for directory in app_state["generated_directory_paths"]:

        output_map = misc_fns.load_json(os.path.join(directory, "output_map.json"))
        if output_map is None:
            misc_fns.graceful_exit(
                1, f"Error: Output map not found in directory `{directory}`"
            )

        for domain in output_map:
            for domain_param_set in output_map[domain]:
                for domain_run in domain_param_set["entries"]["runs"]:

                    if current_run == run_index:

                        generated_domain_path = str(domain_run["json_file"])
                        generated_domain: dict | str | None = None
                        if os.path.isfile(generated_domain_path):
                            generated_domain = misc_fns.load_json(
                                generated_domain_path
                            )
                            if generated_domain is None:
                                misc_fns.graceful_exit(
                                    1,
                                    f"Unable to load generated JSON data at `{generated_domain_path}`.",
                                )
                        else:
                            generated_domain_path = domain_run["txt_file"]
                            raw_txt = open(generated_domain_path, "r").read()
                            generated_domain = f"Failed JSON serialization. Raw text output:\n\n{raw_txt}"

                        domain = os.path.basename(generated_domain_path.split("-")[0])

                        human_curated_path = os.path.join(
                            app_state["generated_output_dir_root"],
                            "human_curated",
                            f"{os.path.basename(directory)}.json",
                        )
                        if not os.path.isfile(human_curated_path):
                            misc_fns.graceful_exit(
                                1,
                                f"Human curated BCO file not found at filepath `{human_curated_path}`.",
                            )
                        human_curated_json = misc_fns.load_json(human_curated_path)
                        if human_curated_json is None:
                            misc_fns.graceful_exit(
                                1,
                                f"Unable to load human curated JSON at path `{human_curated_path}`.",
                            )
                        human_curated_domain_formatted_json = {
                            f"{domain}_domain": human_curated_json[f"{domain}_domain"]
                        }
                        human_curated_domain = json.dumps(
                            human_curated_domain_formatted_json, indent=4
                        )

                        param_set = json.dumps(
                            domain_param_set["entries"]["params"], indent=4
                        )

                        reference_nodes = open(
                            domain_run["source_node_file"], "r"
                        ).read()

                        already_evaluated = False
                        if (
                            os.path.basename(generated_domain_path)
                            in app_state["user_results_data"][app_state["user_hash"]]
                        ):
                            already_evaluated = True

                        run_state = create_run_state(
                            domain=domain,
                            generated_domain=generated_domain,
                            generated_file_path=generated_domain_path,
                            human_curated_domain=human_curated_domain,
                            param_set=param_set,
                            reference_nodes=reference_nodes,
                            run_index=run_index,
                            total_runs=total_runs,
                            already_evaluated=already_evaluated,
                            logger=app_state["logger"],
                        )

                        log_state(run_state, "run")
                        return run_state

                    current_run += 1

    misc_fns.graceful_exit(1, f"Failed to load run state for run index `{run_index}`.")
