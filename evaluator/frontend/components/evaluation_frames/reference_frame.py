from .evaluation_parent import EvaluationBaseFrame
import customtkinter as ctk  # type: ignore
from evaluator.backend.custom_types import (
    AppState,
    RunState,
    RefereceEval,
    create_reference_eval,
    reverse_cast_checkbox,
)
from evaluator.backend import DEFAULT_SCORES

EVAL_DEFAULTS = DEFAULT_SCORES["reference_eval"]


class ReferenceFrame(ctk.CTkFrame, EvaluationBaseFrame):
    """Class for the reference evaluation frame."""

    def __init__(
        self, master: ctk.CTkFrame, app_state: AppState, run_state: RunState, **kwargs
    ):
        """Constructor."""
        super().__init__(master, **kwargs)
        self.state = app_state
        self.run = run_state
        self.reference_eval = self.run["eval_data"]["reference_eval"]

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.main_ref_label = ctk.CTkLabel(
            master=self,
            text="Reference Evaluation",
            font=(self.state["font"], 28, "bold"),
        )
        self.main_ref_label.grid(
            row=0, columnspan=2, padx=self.state["padding"], pady=self.state["padding"]
        )

        self.ref_eval_label = ctk.CTkLabel(
            master=self,
            text="How relevant are the reference nodes?",
            font=(self.state["font"], 16, "bold"),
        )
        self.ref_eval_label.grid(
            row=2,
            column=0,
            padx=(self.state["padding"], self.state["padding"] // 4),
            pady=(self.state["padding"] // 2, self.state["padding"] // 4),
            sticky="w",
        )

        self.ref_eval_var = ctk.IntVar(
            value=self.reference_eval.get(
                "reference_relevancy", EVAL_DEFAULTS["reference_relevancy"]
            )
        )
        self.ref_eval_button = ctk.CTkSegmentedButton(
            master=self, values=[-1, 0, 1, 2], variable=self.ref_eval_var
        )
        self.ref_eval_button.grid(
            row=2,
            column=1,
            padx=(self.state["padding"] // 4, self.state["padding"]),
            pady=self.state["padding"] // 4,
        )

        self.top_ref_var = ctk.StringVar(
            value=reverse_cast_checkbox(
                self.reference_eval.get(
                    "top_reference_retrieval", EVAL_DEFAULTS["top_reference_retrieval"]
                )
            )
        )
        self.top_ref_checkbox = ctk.CTkCheckBox(
            master=self,
            text="Top reference is most relevant?",
            variable=self.top_ref_var,
            onvalue="on",
            offvalue="off",
        )
        self.top_ref_checkbox.grid(
            row=3,
            column=0,
            padx=self.state["padding"],
            pady=self.state["padding"] // 4,
            sticky="w",
        )

        self.ref_notes_label = ctk.CTkLabel(
            master=self, text="Notes", font=(self.state["font"], 16, "bold")
        )
        self.ref_notes_label.grid(
            row=4,
            column=0,
            padx=self.state["padding"],
            pady=(self.state["padding"] // 2, self.state["padding"] // 4),
            sticky="w",
        )

        self.ref_notes = ctk.CTkTextbox(
            master=self, wrap="word", font=(self.state["font"], 18)
        )
        self.ref_notes.grid(
            row=5,
            columnspan=2,
            padx=self.state["padding"] // 2,
            pady=(self.state["padding"] // 4, self.state["padding"]),
            sticky="nsew",
        )

    def update_state(self, app_state: AppState, run_state: RunState) -> None:
        """Update the state.

        Parameters
        ----------
        app_state : AppState
            The updated app state.
        run_state : RunState
            The updated run state.
        """
        self.run = run_state
        self.state = app_state
        self.reference_eval = self.run["eval_data"]["reference_eval"]

        self.ref_eval_var = ctk.IntVar(
            value=self.reference_eval.get(
                "reference_relevancy", EVAL_DEFAULTS["reference_relevancy"]
            )
        )
        self.ref_eval_button.configure(variable=self.ref_eval_var)

        self.top_ref_var = ctk.StringVar(
            value=reverse_cast_checkbox(
                self.reference_eval.get(
                    "top_reference_retrieval", EVAL_DEFAULTS["top_reference_retrieval"]
                )
            )
        )
        self.top_ref_checkbox.configure(variable=self.top_ref_var)

        self.ref_notes.delete(0.0, "end")
        self.ref_notes.insert(
            0.0, self.reference_eval.get("notes", EVAL_DEFAULTS["notes"])
        )

    def get_results(self) -> RefereceEval:
        """Returns the reference evaluations.

        Returns
        -------
        ReferenceEval
            The reference evaluation results.
        """
        ref_eval_score = self.ref_eval_var.get()
        top_ref_val = self.top_ref_var.get()
        notes = self.ref_notes.get(0.0, "end")
        ref_eval = create_reference_eval(
            reference_relevancy=ref_eval_score,
            top_reference_retrieval=top_ref_val,
            notes=notes,
        )
        return ref_eval
