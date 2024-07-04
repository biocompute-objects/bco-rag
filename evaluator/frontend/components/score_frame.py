import customtkinter as ctk  # type: ignore
from evaluator.backend.custom_types import (
    AppState,
    RunState,
    ScoreEval,
    create_score_eval,
    cast_score_eval,
)
from evaluator.backend import DEFAULT_SCORES

EVAL_DEFAULTS = DEFAULT_SCORES["score_eval"]


class ScoreFrame(ctk.CTkFrame):
    """Class for the score frame."""

    def __init__(
        self, master: ctk.CTkFrame, app_state: AppState, run_state: RunState, **kwargs
    ):
        """Constructor."""
        super().__init__(master, **kwargs)
        self.state = app_state
        self.run = run_state
        self.score_eval = run_state["eval_data"]["score_eval"]

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.main_score_label = ctk.CTkLabel(
            master=self, text="Score Evaluation", font=(self.state["font"], 28, "bold")
        )
        self.main_score_label.grid(
            row=0, columnspan=3, padx=self.state["padding"], pady=self.state["padding"]
        )

        self.score_label = ctk.CTkLabel(
            master=self, text="Score:", font=(self.state["font"], 16, "bold")
        )
        self.score_label.grid(
            row=2,
            column=0,
            padx=(self.state["padding"], self.state["padding"] // 2),
            pady=self.state["padding"] // 4,
            sticky="w",
        )

        self.score_text = ctk.CTkLabel(master=self, font=(self.state["font"], 16))
        self.score_text.grid(
            row=2,
            column=1,
            padx=(self.state["padding"] // 2, self.state["padding"]),
            pady=self.state["padding"] // 4,
            sticky="w",
        )

        self.score_version_label = ctk.CTkLabel(
            master=self, text="Score version:", font=(self.state["font"], 16, "bold")
        )
        self.score_version_label.grid(
            row=3,
            column=0,
            padx=(self.state["padding"], self.state["padding"] // 2),
            pady=self.state["padding"] // 4,
            sticky="w",
        )

        self.score_version_text = ctk.CTkLabel(
            master=self, font=(self.state["font"], 16)
        )
        self.score_version_text.grid(
            row=3,
            column=1,
            padx=(self.state["padding"] // 2, self.state["padding"]),
            pady=self.state["padding"] // 4,
            sticky="w",
        )

        self.score_eval_label = ctk.CTkLabel(
            master=self,
            text="Should the score be higher or lower?",
            font=(self.state["font"], 16, "bold"),
        )
        self.score_eval_label.grid(
            row=2,
            column=2,
            padx=self.state["padding"],
            pady=self.state["padding"] // 4,
        )

        self.score_eval_var = ctk.StringVar(value=self.score_eval["eval"])
        self.score_eval_button = ctk.CTkSegmentedButton(
            master=self,
            values=["Lower", "About right", "Higher"],
            variable=self.score_eval_var,
        )
        self.score_eval_button.grid(
            row=3,
            column=2,
            padx=self.state["padding"],
            pady=self.state["padding"] // 4,
        )

        self.score_notes_label = ctk.CTkLabel(
            master=self, text="Notes", font=(self.state["font"], 16, "bold")
        )
        self.score_notes_label.grid(
            row=6,
            column=0,
            padx=self.state["padding"],
            pady=(self.state["padding"] // 2, self.state["padding"] // 4),
            sticky="w",
        )

        self.score_notes = ctk.CTkTextbox(
            master=self, wrap="word", font=(self.state["font"], 18)
        )
        self.score_notes.grid(
            row=7,
            column=0,
            columnspan=3,
            padx=self.state["padding"] // 2,
            pady=(self.state["padding"] // 4, self.state["padding"]),
            sticky="nsew",
        )

        self.update_state(app_state=self.state, run_state=self.run)

    def update_state(self, app_state: AppState, run_state: RunState) -> None:
        """Update the run state and score frame."""
        self.run = run_state
        self.state = app_state
        self.score_eval = self.run["eval_data"]["score_eval"]

        self.score_text.configure(text=f"{self.run['score']}")
        self.score_version_text.configure(text=f"{self.run['score_version']}")

        self.score_eval_var = ctk.StringVar(
            value=self.score_eval.get("eval", EVAL_DEFAULTS["eval"])
        )
        self.score_eval_button.configure(variable=self.score_eval_var)

        self.score_notes.delete(0.0, "end")
        self.score_notes.insert(
            0.0, self.score_eval.get("notes", EVAL_DEFAULTS["notes"])
        )

    def get_results(self) -> ScoreEval:
        """Returns the score evaluations."""
        score_eval_button_val = cast_score_eval(self.score_eval_var.get())
        score_eval = create_score_eval(
            eval=score_eval_button_val, notes=self.score_notes.get(0.0, "end")
        )
        return score_eval
