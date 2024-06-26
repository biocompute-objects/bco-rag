import customtkinter as ctk  # type: ignore
from logging import Logger
from hashlib import md5
from .schemas import (
    create_user_entry,
    UserEntry,
)
import json
from typing import Callable
import os


class LoginScreen(ctk.CTkFrame):
    """Class for the login scree.

    Attributes
    ----------
    logger : Logger
        The frontend logger.
    _on_login_success : Callable
        The callback function for the successful login attempt.
    _padding : int
        The base padding for the widgets.
    _font : str
        Standard font for the login screen widgets.
    _user_source_path : str
        File path to the users file containing all the current users.
    _user_data_path : str
        File path to the users data file containing all the up to date
        data on user evaluations.
    Widgets**

    Note: Does not include the widget attributes.
    """

    def __init__(
        self,
        master: ctk.CTk | ctk.CTkFrame,
        logger: Logger,
        on_login_success: Callable,
        user_source_path: str = os.path.join("./evaluation_results", "users.json"),
        user_data_path: str = os.path.join("./evaluation_results", "user_data.json"),
        standard_padding: int = 20,
        standard_font: str = "Helvetica",
        **kwargs,
    ):
        """Constructor.

        Parameters
        ----------
        master : CTk or CTkFrame
            The parent component/widget.
        logger : Logger
            The frontend logger.
        on_login_success : Callable
            Callback function to be called when login is successful.
        user_source : str (default: "./evaluation_results/users.json")
            The user file for checking logins.
        user_data : str (default: "./evaluation_results/users_data.json")
            The user data file for checking starting point.
        standard_padding : int (default: 20)
            Standard padding for the login screen grid.
        standard_font : str (default: "Helvetica")
            Standard font for the login screen components.
        """
        super().__init__(master, **kwargs)

        self.logger = logger
        self._on_login_success = on_login_success
        self._padding = standard_padding
        self._font = standard_font
        self._user_source_path = user_source_path
        self._user_data_path = user_data_path

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, padx=self._padding + 10, pady=self._padding + 10)

        self.login_label = ctk.CTkLabel(
            master=self, text="Login", font=(self._font, 32, "bold")
        )
        self.login_label.grid(
            row=0, column=0, columnspan=2, pady=(self._padding, self._padding + 10)
        )

        self.first_name_entry = ctk.CTkEntry(
            master=self, placeholder_text="First name", font=(self._font, 16)
        )
        self.first_name_entry.grid(
            row=1, column=0, padx=self._padding, pady=self._padding
        )

        self.last_name_entry = ctk.CTkEntry(
            master=self, placeholder_text="Last name", font=(self._font, 16)
        )
        self.last_name_entry.grid(
            row=1, column=1, padx=self._padding, pady=self._padding
        )

        self.login_button = ctk.CTkButton(
            master=self, text="Login", command=self.login, font=(self._font, 16)
        )
        self.login_button.grid(
            row=2, column=0, rowspan=2, columnspan=3, pady=self._padding
        )

        self.exit_button = ctk.CTkButton(
            master=self, text="Exit", command=self.exit_app, font=(self._font, 16)
        )
        self.exit_button.grid(
            row=3, column=0, rowspan=2, columnspan=3, pady=self._padding
        )

        self.error_label = ctk.CTkLabel(
            master=self, text="", font=(self._font, 14), text_color="red"
        )
        self.error_label.grid(row=4, column=0, columnspan=2, pady=(self._padding, 0))

    def login(self) -> None:
        """Callback for the login button."""

        first_name = self.first_name_entry.get().lower().strip()
        last_name = self.last_name_entry.get().lower().strip()

        if not first_name and not last_name:
            self.error_label.configure(text="Error: First and last name are required.")
            self.logger.error("Empty first and last name login attempt.")
        elif not first_name:
            self.error_label.configure(text="Error: First name is required.")
            self.logger.error("Empty first name login attempt.")
        elif not last_name:
            self.error_label.configure(text="Error: Last name is required.")
            self.logger.error("Empty last name login attempt.")

        user_hash = self._generate_user_hash(first_name, last_name)
        users_file: dict = json.load(open(self._user_source_path, "r"))
        users_data: dict = json.load(open(self._user_data_path, "r"))

        # user already exists
        if self._check_user_existence(user_hash, users_file):
            self.logger.info(f"Found existing user for {last_name}, {first_name}")
            user_data_entry = {user_hash: users_data[user_hash]}
        # new user
        else:
            self.logger.info(f"New user for {last_name}, {first_name}")
            user_entry = self._create_new_user(user_hash, first_name, last_name)
            users_file.update(user_entry)
            json.dump(users_file, open(self._user_source_path, "w"), indent=4)
            user_data_entry = self._create_user_data(user_hash)
            users_data.update(user_data_entry)
            json.dump(users_data, open(self._user_data_path, "w"), indent=4)

        self._on_login_success(user_data_entry, user_hash)

    def _create_new_user(
        self, user_hash: str, first_name: str, last_name: str
    ) -> dict[str, UserEntry]:
        """Creates a new user entry for the users_file.

        Parameters
        ----------
        user_hash : str
            The user's unique hash string.
        first_name : str
            The user's first name.
        last_name : str
            The user's last name.

        Returns
        -------
        dict[str, UserEntry]
            The new user entry.
        """
        user_entry = {user_hash: create_user_entry(first_name, last_name)}
        return user_entry

    def _create_user_data(self, hash_str: str) -> dict[str, dict]:
        """Creates a new entry for the user in the data file.

        Parameters
        ----------
        hash_str : str
            The user's unique hash string.

        Returns
        -------
        dict[str, dict]
            The empty evaluation entry for the user.
        """
        return {hash_str: {}}

    def _check_user_existence(self, user_hash: str, users_file: dict) -> bool:
        """Checks if the user's unique hash exists in the users file.

        Parameters
        ----------
        user_hash : str
            The user's unique hash.
        users_file : dict
            The data from the user's file.

        Returns
        -------
        bool
            True if the user exists, False otherwise.
        """
        if user_hash in users_file:
            return True
        else:
            return False

    def _generate_user_hash(self, first_name: str, last_name: str) -> str:
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

    def exit_app(self):
        """Exit the app."""

        self.master.destroy()
