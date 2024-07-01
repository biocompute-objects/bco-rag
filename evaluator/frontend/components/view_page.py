import customtkinter as ctk  # type: ignore
from typing import Callable, Literal
from evaluator.backend.custom_types import AppState, RunState
from .sidebar import SideBar
from .tab_view import TabView


class ViewPage(ctk.CTkFrame):
    """Class for the view/evaluate page."""

    def __init__(
        self,
        master: ctk.CTk,
        app_state: AppState,
        run_state: RunState,
        navigate: Callable[[Literal[-1, 1], int, AppState], None],
        **kwargs
    ):
        """Constructor."""
        super().__init__(master, **kwargs)

        self.state = app_state
        self.run = run_state
        self.navigate = navigate

        self.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = SideBar(
            master=self,
            app_state=self.state,
            run_state=self.run,
            navigate=self.navigate,
        )

        self.tab_view = TabView(master=self, app_state=self.state, run_state=self.run)
        self.tab_view.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

    def update_state(self, run_state: RunState) -> None:
        """Updates the run state."""
        self.run = run_state
        self.sidebar.update_state(self.run)
        self.tab_view.update_state(self.run)
