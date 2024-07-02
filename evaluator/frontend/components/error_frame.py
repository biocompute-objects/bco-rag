import customtkinter as ctk  # type: ignore
from evaluator.backend.custom_types import AppState, RunState


class ErrorFrame(ctk.CTkFrame):
    """Class for the error frame."""

    def __init__(
        self, master: ctk.CTkFrame, app_state: AppState, run_state: RunState, **kwargs
    ):
        """Constructor."""
        super().__init__(master, **kwargs)
        self.state = app_state
        self.run = run_state

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_err_label = ctk.CTkLabel(
            master=self, text="Error Evaluation", font=(self.state["font"], 28, "bold")
        )
        self.main_err_label.grid(
            row=0, column=0, padx=self.state["padding"], pady=self.state["padding"]
        )

        self.inf_err_var = ctk.StringVar(value="off")
        self.inf_checkbox = ctk.CTkCheckBox(
            master=self,
            text="Inferred Knowledge Error",
            variable=self.inf_err_var,
            onvalue="on",
            offvalue="off",
        )
        self.inf_checkbox.grid(
            row=1,
            column=0,
            padx=self.state["padding"],
            pady=self.state["padding"],
            sticky="w",
        )

        self.ext_err_var = ctk.StringVar(value="off")
        self.ext_checkbox = ctk.CTkCheckBox(
            master=self,
            text="External Knowledge Error",
            variable=self.ext_err_var,
            onvalue="on",
            offvalue="off",
        )
        self.ext_checkbox.grid(
            row=2,
            column=0,
            padx=self.state["padding"],
            pady=self.state["padding"],
            sticky="w",
        )

    def update_state(self, app_state: AppState, run_state: RunState) -> None:
        """Update the state."""
        self.run = run_state
        self.state=app_state
