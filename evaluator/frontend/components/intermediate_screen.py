import customtkinter as ctk  # type: ignore
from typing import Callable
from evaluator.backend.custom_types import AppState
from evaluator.backend.state import set_resume_session


class IntermediateScreen(ctk.CTkFrame):
    """Class for the intermediate screen for the user to choose
    to start from the beginning or to continue from last session.
    """

    def __init__(
        self,
        master: ctk.CTk,
        on_start: Callable[[AppState], None],
        app_state: AppState,
        **kwargs
    ):
        """Constructor."""
        super().__init__(master, **kwargs)

        self.state = app_state
        self.on_start = on_start

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(
            row=0,
            column=0,
            padx=self.state["padding"] + 10,
            pady=self.state["padding"] + 10,
        )

        self.welcome_label = ctk.CTkLabel(
            master=self, text="", font=(self.state["font"], 32, "bold")
        )
        self.welcome_label.grid(
            row=0, column=0, padx=self.state["padding"], pady=self.state["padding"] + 10
        )

        self.start_new_button = ctk.CTkButton(
            master=self,
            text="Start From Beginning",
            command=self._start_new,
            font=(self.state["font"], 16),
        )
        self.start_new_button.grid(
            row=1, column=0, padx=self.state["padding"], pady=self.state["padding"] + 10
        )

        if self.state["new_user"]:
            welcome_text = "New User"
        else:
            welcome_text = "Welcome Back"
            self.continue_button = ctk.CTkButton(
                master=self,
                text="Continue Last Session",
                command=self._continue_last,
                font=(self.state["font"], 16),
            )
            self.continue_button.grid(
                row=2,
                column=0,
                padx=self.state["padding"],
                pady=self.state["padding"] + 10,
            )
        self.welcome_label.configure(text=welcome_text)

    def _start_new(self) -> None:
        """User chose to start a new session."""
        self.state = set_resume_session(self.state, False)
        self.on_start(self.state)

    def _continue_last(self) -> None:
        """User chose to continue from last session."""
        self.state = set_resume_session(self.state, True)
        self.on_start(self.state)
