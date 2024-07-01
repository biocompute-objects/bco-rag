import customtkinter as ctk  # type: ignore
from typing import Callable, Optional, NoReturn
from evaluator.backend.custom_types import AppAttributes, AppState


class LoginScreen(ctk.CTkFrame):
    """Class for the login screen."""

    def __init__(
        self,
        master: ctk.CTk,
        on_login: Callable[[str, str, AppAttributes], tuple[str, Optional[AppState]]],
        on_login_success: Callable[[AppState], None],
        on_exit: Callable[[], NoReturn],
        attributes: AppAttributes,
        **kwargs
    ):
        """Constructor."""
        super().__init__(master, **kwargs)

        self.on_login = on_login
        self.on_login_success = on_login_success
        self.on_exit = on_exit
        self.attributes = attributes

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(
            row=0,
            column=0,
            padx=self.attributes["padding"] + 10,
            pady=self.attributes["padding"] + 10,
        )

        self.login_label = ctk.CTkLabel(
            master=self, text="Login", font=(self.attributes["font"], 32, "bold")
        )
        self.login_label.grid(
            row=0,
            column=0,
            columnspan=2,
            pady=(self.attributes["padding"], self.attributes["padding"] + 10),
        )

        self.first_name_entry = ctk.CTkEntry(
            master=self,
            placeholder_text="First name",
            font=(self.attributes["font"], 16),
        )
        self.first_name_entry.grid(
            row=1,
            column=0,
            padx=self.attributes["padding"],
            pady=self.attributes["padding"],
        )

        self.last_name_entry = ctk.CTkEntry(
            master=self,
            placeholder_text="Last name",
            font=(self.attributes["font"], 16),
        )
        self.last_name_entry.grid(
            row=1,
            column=1,
            padx=self.attributes["padding"],
            pady=self.attributes["padding"],
        )

        self.login_button = ctk.CTkButton(
            master=self,
            text="Login",
            command=self._login,
            font=(self.attributes["font"], 16),
        )
        self.login_button.grid(
            row=2, column=0, rowspan=2, columnspan=3, pady=self.attributes["padding"]
        )

        self.exit_button = ctk.CTkButton(
            master=self,
            text="Exit",
            command=self._exit_app,
            font=(self.attributes["font"], 16),
        )
        self.exit_button.grid(
            row=3, column=0, rowspan=2, columnspan=3, pady=self.attributes["padding"]
        )

        self.error_label = ctk.CTkLabel(
            master=self, text="", font=(self.attributes["font"], 14), text_color="red"
        )
        self.error_label.grid(
            row=4, column=0, columnspan=2, pady=(self.attributes["padding"], 0)
        )

    def _login(self) -> None:
        """Intermediate callback for the login button."""
        return_str, state = self.on_login(
            self.first_name_entry.get(), self.last_name_entry.get(), self.attributes
        )
        if state is None:
            self.error_label.configure(text=return_str)
            return
        self.on_login_success(state)

    def _exit_app(self) -> NoReturn:
        """Intermediate callback for the exit button."""
        self.on_exit()
