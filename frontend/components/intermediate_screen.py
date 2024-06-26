import customtkinter as ctk  # type: ignore
from typing import Callable


class IntermediateScreen(ctk.CTkFrame):
    """Class for the intermediate screen for the user to choose to start from the
    beginning or to continue where left off.

    Attributes
    ----------
    user_data_entry : dict[str, dict]
        The user's current data entry containing information on the user's evaluations.
    user_hash : str
        The user's unique hash.
    on_start : Callable
        The callback function for the evaluation start.
    _padding : int
        The base padding for the widgets.
    _font : str
        Standard font for the login screen widgets.
    Widgets**

    Note: Does not include the widget attributes.
    """

    def __init__(
        self,
        master: ctk.CTk,
        user_data_entry: dict[str, dict],
        user_hash: str,
        on_start: Callable,
        standard_padding: int = 20,
        standard_font: str = "Helvetica",
        **kwargs
    ):
        """Constructor.

        Parameters
        ----------
        master : ctk.CTk
        """
        super().__init__(master, **kwargs)

        self.user_data_entry = user_data_entry
        self.user_hash = user_hash
        self.on_start = on_start

        self._padding = standard_padding
        self._font = standard_font

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(
            row=0,
            column=0,
            padx=self._padding + 10,
            pady=self._padding + 10,
        )

        button_row = 1
        if self.user_data_entry[user_hash] == {}:

            self.info_label = ctk.CTkLabel(
                master=self, text="New User", font=(self._font, 24, "bold")
            )
            self.info_label.grid(
                row=0, column=0, padx=self._padding, pady=self._padding + 10
            )

        else:

            self.info_label = ctk.CTkLabel(
                master=self, text="Welcome Back!", font=(self._font, 24, "bold")
            )
            self.info_label.grid(
                row=0, column=0, padx=self._padding, pady=self._padding + 10
            )

            self.continue_button = ctk.CTkButton(
                master=self,
                text="Continue from last session",
                command=self.continue_last,
                font=(self._font, 16),
            )
            self.continue_button.grid(
                row=button_row, column=0, padx=self._padding, pady=self._padding + 10
            )
            button_row += 1

        self.start_new_button = ctk.CTkButton(
            master=self,
            text="Start from Beginning",
            command=self.start_new,
            font=(self._font, 16),
        )
        self.start_new_button.grid(
            row=button_row, column=0, padx=self._padding, pady=self._padding + 10
        )

    def start_new(self):
        """Starts from the beginning, potentially overwriting previous evaluations."""
        self.on_start(True, self.user_data_entry)

    def continue_last(self):
        """Only perform new evaluations."""
        self.on_start(False, self.user_data_entry)
