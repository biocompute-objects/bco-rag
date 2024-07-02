import customtkinter as ctk  # type: ignore
from typing import Callable, Literal, NoReturn
from evaluator.backend.custom_types import AppAttributes, AppState, RunState
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
        on_save: Callable[[AppState], None],
        on_exit: Callable[[], NoReturn],
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
            on_save=on_save,
            on_exit=on_exit,
        )

        self.tab_view = TabView(master=self, app_state=self.state, run_state=self.run)
        self.tab_view.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

    def update_state(self, app_state: AppState, run_state: RunState) -> None:
        """Updates the state."""
        self.run = run_state
        self.state = app_state
        self.sidebar.update_state(self.run)
        self.tab_view.update_state(app_state=app_state, run_state=self.run)
