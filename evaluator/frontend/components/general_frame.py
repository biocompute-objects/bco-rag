import customtkinter as ctk  # type: ignore
from evaluator.backend.custom_types import (
    AppState,
    RunState,
    GeneralEval,
    create_general_eval,
)
from evaluator.backend import DEFAULT_SCORES

EVAL_DEFAULTS = DEFAULT_SCORES["general_eval"]


class GeneralFrame(ctk.CTkFrame):
    """Class for the general frame."""

    def __init__(
        self, master: ctk.CTkFrame, app_state: AppState, run_state: RunState, **kwargs
    ):
        """Constructor."""
        super().__init__(master, **kwargs)
        self.state = app_state
        self.run = run_state
        self.general_eval = self.run["eval_data"]["general_eval"]

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.main_gen_label = ctk.CTkLabel(
            master=self,
            text="General Evaluation",
            font=(self.state["font"], 28, "bold"),
        )
        self.main_gen_label.grid(
            row=0, columnspan=2, padx=self.state["padding"], pady=self.state["padding"]
        )

        self.relevancy_label = ctk.CTkLabel(
            master=self,
            text="How relevant is the domain content?",
            font=(self.state["font"], 16, "bold"),
        )
        self.relevancy_label.grid(
            row=2,
            column=0,
            padx=(self.state["padding"], self.state["padding"] // 4),
            pady=(self.state["padding"] // 2, self.state["padding"] // 4),
            sticky="w",
        )

        self.relevancy_var = ctk.IntVar(
            value=self.general_eval.get("relevancy", EVAL_DEFAULTS["relevancy"])
        )
        self.relevancy_button = ctk.CTkSegmentedButton(
            master=self, values=[-1, 0, 1, 2], variable=self.relevancy_var
        )
        self.relevancy_button.grid(
            row=2,
            column=1,
            padx=(self.state["padding"] // 4, self.state["padding"]),
            pady=(self.state["padding"] // 2, self.state["padding"] // 4),
            sticky="w",
        )

        self.readability_label = ctk.CTkLabel(
            master=self,
            text="How readable is the domain content?",
            font=(self.state["font"], 16, "bold"),
        )
        self.readability_label.grid(
            row=3,
            column=0,
            padx=(self.state["padding"], self.state["padding"] // 4),
            pady=self.state["padding"] // 4,
            sticky="w",
        )

        self.readability_var = ctk.IntVar(
            value=self.general_eval.get("readability", EVAL_DEFAULTS["readability"])
        )
        self.readability_button = ctk.CTkSegmentedButton(
            master=self, values=[-1, 0, 1, 2], variable=self.readability_var
        )
        self.readability_button.grid(
            row=3,
            column=1,
            padx=(self.state["padding"] // 4, self.state["padding"]),
            pady=self.state["padding"] // 4,
            sticky="w",
        )

        self.reproducibility_label = ctk.CTkLabel(
            master=self,
            text="How reproducible is the domain content?",
            font=(self.state["font"], 16, "bold"),
        )
        self.reproducibility_label.grid(
            row=4,
            column=0,
            padx=(self.state["padding"], self.state["padding"] // 4),
            pady=self.state["padding"] // 4,
            sticky="w",
        )

        self.reproducibility_var = ctk.IntVar(
            value=self.general_eval.get(
                "reproducibility", EVAL_DEFAULTS["reproducibility"]
            )
        )
        self.reproducibility_button = ctk.CTkSegmentedButton(
            master=self, values=[-1, 0, 1, 2], variable=self.reproducibility_var
        )
        self.reproducibility_button.grid(
            row=4,
            column=1,
            padx=(self.state["padding"] // 4, self.state["padding"]),
            pady=self.state["padding"] // 4,
            sticky="w",
        )

        self.conf_label = ctk.CTkLabel(
            master=self,
            text="What is your confidence rating for the domain?",
            font=(self.state["font"], 16, "bold"),
        )
        self.conf_label.grid(
            row=5,
            column=0,
            padx=(self.state["padding"], self.state["padding"] // 4),
            pady=self.state["padding"] // 4,
            sticky="w",
        )

        self.conf_var = ctk.IntVar(
            value=self.general_eval.get(
                "confidence_rating", EVAL_DEFAULTS["confidence_rating"]
            )
        )
        self.conf_button = ctk.CTkSegmentedButton(
            master=self, values=[-1, 0, 1, 2], variable=self.conf_var
        )
        self.conf_button.grid(
            row=5,
            column=1,
            padx=(self.state["padding"] // 4, self.state["padding"]),
            pady=self.state["padding"] // 4,
            sticky="w",
        )

        self.general_notes_label = ctk.CTkLabel(
            master=self, text="Notes", font=(self.state["font"], 16, "bold")
        )
        self.general_notes_label.grid(
            row=6,
            column=0,
            padx=self.state["padding"],
            pady=(self.state["padding"] // 2, self.state["padding"] // 4),
            sticky="w",
        )

        self.general_notes = ctk.CTkTextbox(
            master=self, wrap="word", font=(self.state["font"], 18)
        )
        self.general_notes.grid(
            row=7,
            columnspan=2,
            padx=self.state["padding"] // 2,
            pady=(self.state["padding"] // 4, self.state["padding"]),
            sticky="nsew",
        )

    def update_state(self, app_state: AppState, run_state: RunState) -> None:
        """Update the state."""
        self.run = run_state
        self.state = app_state
        self.general_eval = self.run["eval_data"]["general_eval"]

        self.relevancy_var = ctk.IntVar(
            value=self.general_eval.get("relevancy", EVAL_DEFAULTS["relevancy"])
        )
        self.relevancy_button.configure(variable=self.relevancy_var)

        self.readability_var = ctk.IntVar(
            value=self.general_eval.get("readability", EVAL_DEFAULTS["readability"])
        )
        self.readability_button.configure(variable=self.readability_var)

        self.reproducibility_var = ctk.IntVar(
            value=self.general_eval.get(
                "reproducibility", EVAL_DEFAULTS["reproducibility"]
            )
        )
        self.reproducibility_button.configure(variable=self.reproducibility_var)

        self.conf_var = ctk.IntVar(
            value=self.general_eval.get(
                "confidence_rating", EVAL_DEFAULTS["confidence_rating"]
            )
        )
        self.conf_button.configure(variable=self.conf_var)

        self.general_notes.delete(0.0, "end")
        self.general_notes.insert(
            0.0, self.general_eval.get("notes", EVAL_DEFAULTS["notes"])
        )

    def get_results(self) -> GeneralEval:
        """Returns the general evaluations."""
        relevancy_val = self.relevancy_var.get()
        readability_var = self.readability_var.get()
        reproducibility_var = self.reproducibility_var.get()
        conf_var = self.conf_var.get()
        general_val = create_general_eval(
            relevancy=relevancy_val,
            readability=readability_var,
            reproducibility=reproducibility_var,
            confidence_rating=conf_var,
            notes=self.general_notes.get(0.0, "end"),
        )
        return general_val
