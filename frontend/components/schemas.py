from typing import TypedDict

### User source typing


class UserEntry(TypedDict):
    """"""

    first_name: str
    last_name: str


def create_user_entry(first_name: str, last_name: str) -> UserEntry:
    """"""
    return_data: UserEntry = {"first_name": first_name, "last_name": last_name}
    return return_data

