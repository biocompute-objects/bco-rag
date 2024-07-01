import customtkinter as ctk  # type: ignore
from evaluator.backend import app_start, state
from evaluator.backend.login import login
from evaluator.backend.custom_types import AppState, RunState, create_run_state
import evaluator.backend.miscellaneous as misc
from .components import LoginScreen, IntermediateScreen, ViewPage
from typing import Literal


class App(ctk.CTk):
    """Frontend for evaluating generated BCO domains from
    BcoRag.
    """

    def __init__(self):
        """Constructor."""
        super().__init__()
        init_data = app_start.initialization()

        self.attributes = init_data

        self.title("BCO RAG Evaluator")
        self.geometry(f"{1920}x{1080}")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.login_screen = LoginScreen(
            master=self,
            attributes=self.attributes,
            on_login=login,
            on_login_success=self._login_success,
            on_exit=misc.exit_app,
        )

    def start(self):
        """Start the app main loop."""
        self.mainloop()

    def navigate(
        self, direction: Literal[-1, 1], run_index: int, app_state: AppState
    ) -> None:
        """Callback to execute when the user presses
        the next or previous buttons.

        Parameters
        ----------
        direction : -1 or 1
            Indicates the direction the user is navigating,
            -1 for previous, 1 for next.
        run_index : int
            The new run index being navigated to.
        app_state : AppState
            The current app state.
        """
        updated_run_state = state.load_run_state(
            run_index=run_index, total_runs=self.run["total_runs"], app_state=app_state
        )
        self.view_page.update_state(updated_run_state)

    def _login_success(self, app_state: AppState) -> None:
        """Callback to execute on login success."""
        self.login_screen.grid_forget()
        self.intermediate_screen = IntermediateScreen(
            master=self, on_start=self._on_start, app_state=app_state
        )

    def _on_start(self, app_state: AppState) -> None:
        """Callback to execute on evaluation start."""
        self.intermediate_screen.grid_forget()
        # create init run state
        init_run_state = app_start.create_init_run_state(app_state)
        self.run = init_run_state
        self.view_page = ViewPage(
            master=self,
            app_state=app_state,
            run_state=init_run_state,
            navigate=self.navigate,
            on_save=state.save_state,
            on_exit=misc.exit_app
        )
