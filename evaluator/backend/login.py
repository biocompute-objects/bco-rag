"""Handles the backend for the login process.
"""

from .custom_types import AppAttributes, AppState, create_app_state
from .miscellaneous import log_state
from .state import create_new_user
from hashlib import md5
from typing import Optional


def login(
    first_name: str, last_name: str, attributes: AppAttributes
) -> tuple[str, Optional[AppState]]:
    """Login entry point.

    Parameters
    ----------
    first_name : str
        First name entered by the user.
    last_name : str
        Last name entered by the user.
    attributes : AppAttributes
        The current app attributes.

    Returns
    -------
    tuple (str, AppState or None)
        A string containing the user hash on success or an
        error message on errror and the current app state
        on success or None on error.
    """
    if not first_name and not last_name:
        return "Error: First and last name are required.", None
    elif not first_name:
        return "Error: First name is required.", None
    elif not last_name:
        return "Error: Last name is required.", None

    first_name = first_name.strip().lower()
    last_name = last_name.strip().lower()

    user_hash = _generate_user_hash(first_name, last_name)

    if _check_user_existence(user_hash, attributes):
        attributes["logger"].info(f"Found existing user for {last_name}, {first_name}")
        new_user = False
    else:
        new_user = True

    app_state = create_app_state(
        attributes=attributes, user_hash=user_hash, new_user=new_user
    )
    if new_user:
        app_state = create_new_user(
            app_state=app_state, first_name=first_name, last_name=last_name
        )

    log_state(app_state, "app")

    return user_hash, app_state


def _check_user_existence(user_hash: str, attributes: AppAttributes) -> bool:
    """Chechks if the user already exists or not.

    user_hash : str
        The user's md5 hash.
    attributes : AppAttributes
        The current app state.

    Returns
    -------
    bool
        True if the user exists, False otherwise.
    """
    if user_hash in attributes["users_data"]:
        return True
    else:
        return False


def _generate_user_hash(first_name: str, last_name: str) -> str:
    """Generates the user's MD5 hash.

    Parameters
    ----------
    first_name : str
        The user's first name.
    last_name : str
        The user's last name.

    Returns
    -------
    str
        The user hash.
    """
    name_list = [first_name, last_name]
    sorted(name_list)
    name_str = "_".join(name_list)
    hash_hex = md5(name_str.encode("utf-8")).hexdigest()
    return hash_hex
