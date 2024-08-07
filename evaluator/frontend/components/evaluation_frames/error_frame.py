from .evaluation_parent import EvaluationBaseFrame
import customtkinter as ctk  # type: ignore
from evaluator.backend.custom_types import (
    AppState,
    ErrorEval,
    RunState,
    create_error_val,
    reverse_cast_checkbox,
)
from evaluator.backend import DEFAULT_SCORES

EVAL_DEFAULTS = DEFAULT_SCORES["error_eval"]


class ErrorFrame(ctk.CTkFrame, EvaluationBaseFrame):
    """Class for the error evaluation frame."""

    def __init__(
        self, master: ctk.CTkFrame, app_state: AppState, run_state: RunState, **kwargs
    ):
        """Constructor."""
        super().__init__(master, **kwargs)
        self.state = app_state
        self.run = run_state
        self.error_eval = self.run["eval_data"]["error_eval"]

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.main_err_label = ctk.CTkLabel(
            master=self, text="Error Evaluation", font=(self.state["font"], 28, "bold")
        )
        self.main_err_label.grid(
            row=0,
            columnspan=2,
            padx=self.state["padding"],
            pady=self.state["padding"],
        )

        self.inf_err_var = ctk.StringVar(
            value=reverse_cast_checkbox(
                self.error_eval.get(
                    "inferred_knowledge_error",
                    EVAL_DEFAULTS["inferred_knowledge_error"],
                )
            )
        )
        self.inf_checkbox = ctk.CTkCheckBox(
            master=self,
            text="Inferred Knowledge Error",
            variable=self.inf_err_var,
            onvalue="on",
            offvalue="off",
        )
        self.inf_checkbox.grid(
            row=2,
            column=0,
            padx=(self.state["padding"], self.state["padding"] // 4),
            pady=self.state["padding"] // 2,
            sticky="w",
        )

        self.ext_err_var = ctk.StringVar(
            value=reverse_cast_checkbox(
                self.error_eval.get(
                    "external_knowledge_error",
                    EVAL_DEFAULTS["external_knowledge_error"],
                )
            )
        )
        self.ext_checkbox = ctk.CTkCheckBox(
            master=self,
            text="External Knowledge Error",
            variable=self.ext_err_var,
            onvalue="on",
            offvalue="off",
        )
        self.ext_checkbox.grid(
            row=3,
            column=0,
            padx=(self.state["padding"], self.state["padding"] // 4),
            pady=self.state["padding"] // 4,
            sticky="w",
        )

        self.json_err_var = ctk.StringVar(
            value=reverse_cast_checkbox(
                self.error_eval.get(
                    "json_format_error", EVAL_DEFAULTS["json_format_error"]
                )
            )
        )
        self.json_checkbox = ctk.CTkCheckBox(
            master=self,
            text="JSON Formatting Error",
            variable=self.json_err_var,
            onvalue="on",
            offvalue="off",
        )
        self.json_checkbox.grid(
            row=2,
            column=1,
            padx=(self.state["padding"] // 4, self.state["padding"]),
            pady=self.state["padding"] // 2,
            sticky="w",
        )

        self.other_err_var = ctk.StringVar(
            value=reverse_cast_checkbox(
                self.error_eval.get("other_error", EVAL_DEFAULTS["other_error"])
            )
        )
        self.other_err_checkbox = ctk.CTkCheckBox(
            master=self,
            text="Other Error",
            variable=self.other_err_var,
            onvalue="on",
            offvalue="off",
        )
        self.other_err_checkbox.grid(
            row=3,
            column=1,
            padx=(self.state["padding"] // 4, self.state["padding"]),
            pady=self.state["padding"] // 4,
            sticky="w",
        )

        self.error_notes_label = ctk.CTkLabel(
            master=self, text="Notes", font=(self.state["font"], 16, "bold")
        )
        self.error_notes_label.grid(
            row=4,
            column=0,
            padx=self.state["padding"],
            pady=(self.state["padding"] // 2, self.state["padding"] // 4),
            sticky="w",
        )

        self.error_notes = ctk.CTkTextbox(
            master=self, wrap="word", font=(self.state["font"], 18)
        )
        self.error_notes.grid(
            row=5,
            columnspan=2,
            padx=self.state["padding"] // 2,
            pady=(self.state["padding"] // 4, self.state["padding"]),
            sticky="nsew",
        )

    def update_state(self, app_state: AppState, run_state: RunState) -> None:
        """Update the component state.

        Parameters
        ----------
        app_state : AppState
            The updated app state.
        run_state : RunState
            The updated run state.
        """
        self.run = run_state
        self.state = app_state
        self.error_eval = self.run["eval_data"]["error_eval"]

        self.inf_err_var = ctk.StringVar(
            value=reverse_cast_checkbox(
                self.error_eval.get(
                    "inferred_knowledge_error",
                    EVAL_DEFAULTS["inferred_knowledge_error"],
                )
            )
        )
        self.inf_checkbox.configure(variable=self.inf_err_var)

        self.ext_err_var = ctk.StringVar(
            value=reverse_cast_checkbox(
                self.error_eval.get(
                    "external_knowledge_error",
                    EVAL_DEFAULTS["external_knowledge_error"],
                )
            )
        )
        self.ext_checkbox.configure(variable=self.ext_err_var)

        self.json_err_var = ctk.StringVar(
            value=reverse_cast_checkbox(
                self.error_eval.get(
                    "json_format_error", EVAL_DEFAULTS["json_format_error"]
                )
            )
        )
        self.json_checkbox.configure(variable=self.json_err_var)

        self.other_err_var = ctk.StringVar(
            value=reverse_cast_checkbox(
                self.error_eval.get("other_error", EVAL_DEFAULTS["other_error"])
            )
        )
        self.other_err_checkbox.configure(variable=self.other_err_var)

        self.error_notes.delete(0.0, "end")
        self.error_notes.insert(
            0.0, self.error_eval.get("notes", EVAL_DEFAULTS["notes"])
        )

    def get_results(self) -> ErrorEval:
        """Returns the error evaluations.

        Returns
        -------
        ErrorEval
            The error evaluation results.
        """
        error_eval = create_error_val(
            inf_err=self.inf_err_var.get(),
            ext_err=self.ext_err_var.get(),
            json_err=self.json_err_var.get(),
            other_err=self.other_err_var.get(),
            notes=self.error_notes.get(0.0, "end"),
        )
        return error_eval
