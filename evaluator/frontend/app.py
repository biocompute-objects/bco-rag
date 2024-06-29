import customtkinter as ctk  # type: ignore
from evaluator.backend import app_start
from evaluator.backend.login import login
from evaluator.backend.custom_types import AppState
import evaluator.backend.miscellaneous as misc
from .components.login_screen import LoginScreen


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

        self.login_screen = LoginScreen(
            master=self,
            attributes=self.attributes,
            on_login=login,
            on_login_success=self.login_success,
            on_exit=misc.exit_app,
        )

    def start(self):
        """Start the app main loop."""
        self.mainloop()

    def login_success(self, state: AppState) -> None:
        """"""
        print("we here")
