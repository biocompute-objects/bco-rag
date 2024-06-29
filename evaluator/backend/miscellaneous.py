from bcorag import misc_functions
from .custom_types import AppAttributes, AppState, StateKey
import customtkinter as ctk  # type: ignore
from typing import NoReturn, get_args


def exit_app(app_state: AppState | AppAttributes) -> NoReturn:
    """Gracefully exits the app.

    Parameters
    ----------
    app_state : AppState or AppAttributes
        The app state or attributes (if state hasn't been initialized 
        yet) containing output data to write to disk before exiting 
        (prevents lost save data).
    """
    # TODO : implement attributes writes
    misc_functions.graceful_exit(0)


def log_state(app_state: AppState) -> None:
    """Logs the app state.

    Parameters
    ----------
    app_state : AppState
        The app state.
    """
    log_str = "App state:\n"
    key: StateKey
    for key in get_args(StateKey):
        if key == "logger":
            continue
        log_str += f"\t{key}: {app_state[key]}\n"
