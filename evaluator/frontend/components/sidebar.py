import customtkinter as ctk  # type: ignore
from evaluator.backend.custom_types import AppState, RunState
from typing import Callable, Literal


class SideBar(ctk.CTkFrame):
    """Class for the navigation sidebar."""

    def __init__(
        self,
        master: ctk.CTkFrame,
        app_state: AppState,
        run_state: RunState,
        navigate: Callable[[Literal[-1, 1], int, AppState], None],
        **kwargs,
    ):
        """Constructor."""
        super().__init__(master, **kwargs)

        self.state = app_state
        self.run = run_state
        self.navigate = navigate

        self.sidebar_frame = ctk.CTkFrame(master=master, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=1, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(3, weight=1)

        padding = self.state["padding"]
        half_padding = padding // 2

        self.navigate_label = ctk.CTkLabel(
            master=self.sidebar_frame,
            text="Navigate",
            font=(self.state["font"], 16, "bold"),
        )
        self.navigate_label.grid(
            row=0, column=0, padx=padding, pady=(padding, half_padding)
        )

        self.prev_button = ctk.CTkButton(
            master=self.sidebar_frame,
            text="Previous",
            command=self._previous,
            state=("normal" if self.run["run_index"] > 0 else "disabled"),
        )
        self.prev_button.grid(row=1, column=0, padx=padding, pady=half_padding)

        self.next_button = ctk.CTkButton(
            master=self.sidebar_frame,
            text="Next",
            command=self._next,
            state=(
                "normal"
                if self.run["run_index"] < self.run["total_runs"] - 1
                else "disabled"
            ),
        )
        self.next_button.grid(row=2, column=0, padx=padding, pady=half_padding)

        # TODO implement run index counter label
        # TODO implement save button
        # TODO implement exit button

        self.appearance_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="Appearance",
            font=(self.state["font"], 16, "bold"),
        )
        self.appearance_label.grid(
            row=4, column=0, padx=padding, pady=(padding, half_padding)
        )

        self.appearance_option_menu = ctk.CTkOptionMenu(
            self.sidebar_frame,
            values=["System", "Light", "Dark"],
            command=self._change_appearance_mode,
        )
        self.appearance_option_menu.grid(
            row=5, column=0, padx=padding, pady=half_padding
        )

        self.scaling_label = ctk.CTkLabel(
            master=self.sidebar_frame,
            text="UI Scaling",
            font=(self.state["font"], 16, "bold"),
        )
        self.scaling_label.grid(row=6, column=0, padx=padding, pady=half_padding)

        self.scaling_option_menu = ctk.CTkOptionMenu(
            master=self.sidebar_frame,
            values=["70%", "80%", "90%", "100%", "110%", "120%", "130%"],
            command=self._change_scaling_value,
        )
        self.scaling_option_menu.grid(
            row=7, column=0, padx=padding, pady=(half_padding, padding)
        )

    def update_state(self, run_state: RunState) -> None:
        """Updates the run state for consistency."""
        self.run = run_state

    def _previous(self) -> None:
        """Callback for the previous button press."""
        new_run_index = self.run["run_index"] - 1
        if new_run_index == 0:
            self.prev_button.configure(state="disabled")
        else:
            self.prev_button.configure(state="normal")
        self.next_button.configure(state="normal")
        self.navigate(-1, new_run_index, self.state)

    def _next(self) -> None:
        """Callback for the next button press."""
        new_run_index = self.run["run_index"] + 1
        if new_run_index > self.run["total_runs"] - 1:
            self.next_button.configure(state="disabled")
        else:
            self.next_button.configure(state="normal")
        self.prev_button.configure(state="normal")
        self.navigate(1, new_run_index, self.state)

    def _change_appearance_mode(self, new_appearance_mode: str) -> None:
        """Changes the UI color mode."""
        ctk.set_appearance_mode(new_appearance_mode)

    def _change_scaling_value(self, new_scaling: str) -> None:
        """Changes the UI scaling."""
        new_scaling_val = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_val)
