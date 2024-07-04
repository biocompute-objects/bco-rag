import customtkinter as ctk  # type: ignore
from evaluator.backend.custom_types import (
    AppState,
    MiscEval,
    RunState,
    create_misc_eval,
)
from evaluator.backend import DEFAULT_SCORES

EVAL_DEFAULTS = DEFAULT_SCORES["misc_eval"]


class MiscFrame(ctk.CTkFrame):
    """Class for the miscellaneous frame."""

    def __init__(
        self, master: ctk.CTkFrame, app_state: AppState, run_state: RunState, **kwargs
    ):
        """Constructor."""
        super().__init__(master, **kwargs)
        self.state = app_state
        self.run = run_state
        self.misc_eval = self.run["eval_data"]["misc_eval"]

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=20)
        self.grid_rowconfigure(8, weight=1)

        self.main_misc_label = ctk.CTkLabel(
            master=self,
            text="Miscellaneous Evaluation",
            font=(self.state["font"], 28, "bold"),
        )
        self.main_misc_label.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=self.state["padding"],
            pady=self.state["padding"],
            sticky="n",
        )

        self.human_domain_rating_label = ctk.CTkLabel(
            master=self,
            text="What would you rate the human curated domain?",
            font=(self.state["font"], 16, "bold"),
        )
        self.human_domain_rating_label.grid(
            row=2,
            column=0,
            padx=(self.state["padding"], 0),
            pady=(self.state["padding"] // 2, self.state["padding"] // 4),
            sticky="w",
        )

        self.human_domain_rating_var = ctk.IntVar(
            value=self.misc_eval.get(
                "human_domain_rating", EVAL_DEFAULTS["human_domain_rating"]
            )
        )
        self.human_domain_rating_button = ctk.CTkSegmentedButton(
            master=self, values=[-1, 0, 1, 2], variable=self.human_domain_rating_var
        )
        self.human_domain_rating_button.grid(
            row=3,
            column=0,
            padx=(self.state["padding"], 0),
            pady=(self.state["padding"] // 4, self.state["padding"] // 2),
            sticky="w",
        )

        self.evaluator_conf_label = ctk.CTkLabel(
            master=self,
            text="What is your confidence in your evaluation?",
            font=(self.state["font"], 16, "bold"),
        )
        self.evaluator_conf_label.grid(
            row=4,
            column=0,
            padx=(self.state["padding"], 0),
            pady=(self.state["padding"] // 2, self.state["padding"] // 4),
            sticky="w",
        )

        self.evaluator_conf_var = ctk.IntVar(
            value=self.misc_eval.get(
                "evaluator_confidence_rating",
                EVAL_DEFAULTS["evaluator_confidence_rating"],
            )
        )
        self.evaluator_conf_button = ctk.CTkSegmentedButton(
            master=self, values=[-1, 0, 1, 2], variable=self.evaluator_conf_var
        )
        self.evaluator_conf_button.grid(
            row=5,
            column=0,
            padx=(self.state["padding"], 0),
            pady=(self.state["padding"] // 4, self.state["padding"] // 2),
            sticky="w",
        )

        self.evaluator_fam_label = ctk.CTkLabel(
            master=self,
            text="What is your familiarity with the paper content?",
            font=(self.state["font"], 16, "bold"),
        )
        self.evaluator_fam_label.grid(
            row=6,
            column=0,
            padx=(self.state["padding"], 0),
            pady=(self.state["padding"] // 2, self.state["padding"] // 4),
            sticky="w",
        )

        self.evaluator_fam_var = ctk.IntVar(
            value=self.misc_eval.get(
                "evaluator_familiarity_level",
                EVAL_DEFAULTS["evaluator_familiarity_level"],
            )
        )
        self.evaluator_fam_button = ctk.CTkSegmentedButton(
            master=self, values=[-1, 0, 1, 2], variable=self.evaluator_conf_var
        )
        self.evaluator_fam_button.grid(
            row=7,
            column=0,
            padx=(self.state["padding"], 0),
            pady=(self.state["padding"] // 4, self.state["padding"] // 2),
            sticky="w",
        )

        self.misc_notes_label = ctk.CTkLabel(
            master=self, text="Notes", font=(self.state["font"], 16, "bold")
        )
        self.misc_notes_label.grid(
            row=2,
            column=1,
            padx=(0, self.state["padding"] // 4),
            pady=(self.state["padding"] // 2, self.state["padding"] // 4),
            sticky="w",
        )

        self.misc_notes = ctk.CTkTextbox(
            master=self, wrap="word", font=(self.state["font"], 18)
        )
        self.misc_notes.grid(
            row=3,
            rowspan=6,
            column=1,
            padx=(0, self.state["padding"] // 2),
            pady=(self.state["padding"] // 4, self.state["padding"]),
            sticky="nsew",
        )

    def update_state(self, app_state: AppState, run_state: RunState) -> None:
        """Update the state."""
        self.run = run_state
        self.state = app_state
        self.misc_eval = self.run["eval_data"]["misc_eval"]

        self.human_domain_rating_var = ctk.IntVar(
            value=self.misc_eval.get(
                "human_domain_rating", EVAL_DEFAULTS["human_domain_rating"]
            )
        )
        self.human_domain_rating_button.configure(variable=self.human_domain_rating_var)

        self.evaluator_conf_var = ctk.IntVar(
            value=self.misc_eval.get(
                "evaluator_confidence_rating",
                EVAL_DEFAULTS["evaluator_confidence_rating"],
            )
        )
        self.evaluator_conf_button.configure(variable=self.evaluator_conf_var)

        self.evaluator_fam_var = ctk.IntVar(
            value=self.misc_eval.get(
                "evaluator_familiarity_level",
                EVAL_DEFAULTS["evaluator_familiarity_level"],
            )
        )
        self.evaluator_fam_button.configure(variable=self.evaluator_fam_var)

        self.misc_notes.delete(0.0, "end")
        self.misc_notes.insert(0.0, self.misc_eval.get("notes", EVAL_DEFAULTS["notes"]))

    def get_results(self) -> MiscEval:
        """Returns the miscellaneous evaluations."""
        human_domain_rating = self.human_domain_rating_var.get()
        evaluator_conf_rating = self.evaluator_conf_var.get()
        evaluator_familiarity_level = self.evaluator_fam_var.get()
        misc_eval = create_misc_eval(
            human_domain_rating=human_domain_rating,
            evaluator_confidence_rating=evaluator_conf_rating,
            evaluator_familiarity_level=evaluator_familiarity_level,
            notes=self.misc_notes.get(0.0, "end"),
        )
        return misc_eval
