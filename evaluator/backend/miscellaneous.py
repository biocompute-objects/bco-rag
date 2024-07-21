from bcorag import misc_functions
from .custom_types import AppState, AppStateKey, RunState, RunStateKey
from typing import NoReturn, get_args, Literal, cast


def exit_app() -> NoReturn:
    """Gracefully exits the app."""
    misc_functions.graceful_exit(0)


def log_state(state: AppState | RunState, state_type: Literal["app", "run"]) -> None:
    """Logs the app state.

    Parameters
    ----------
    state : AppState or RunState
        The state to log.
    state_type : "app" or "run"
        The type of state being logged.
    """
    app_state_flag = True if state_type.lower().strip() == "app" else False
    log_str = "App state:\n" if app_state_flag else "Run state:\n"

    if app_state_flag:
        app_state = cast(AppState, state)
        app_key: AppStateKey
        for app_key in get_args(AppStateKey):
            if app_key == "logger":
                continue
            log_str += f"\t{app_key}: {app_state[app_key]}\n"
    else:
        run_state = cast(RunState, state)
        run_key: RunStateKey
        for run_key in get_args(RunStateKey):
            if run_key in {
                "generated_domain",
                "human_curated_domain",
                "reference_nodes",
                "param_set",
                "logger",
                "eval_data"
            }:
                continue
            log_str += f"\t{run_key}: {run_state[run_key]}\n"

    state["logger"].info(log_str)
