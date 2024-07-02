import customtkinter as ctk  # type: ignore
from evaluator.backend.custom_types import (
    EvalData,
    RunState,
    AppState,
    create_full_eval,
)
from .score_frame import ScoreFrame
from .error_frame import ErrorFrame


class TabView(ctk.CTkTabview):
    """Class for the view page tab view."""

    def __init__(
        self, master: ctk.CTkFrame, app_state: AppState, run_state: RunState, **kwargs
    ):
        """Constructor."""
        super().__init__(master, **kwargs)

        self.state = app_state
        self.run = run_state

        self.add("Compare JSON")
        self.add("Source Nodes")
        self.add("Parameter Set")
        self.add("Evaluate")

        self._create_compare_json_tab()
        self._create_source_node_tab()
        self._create_parameter_set_tab()
        self._create_evaluate_tab()

        self.update_state(app_state=self.state, run_state=self.run)

    def update_state(self, app_state: AppState, run_state: RunState) -> None:
        """Loads the run data and updates the state.

        Parameters
        ----------
        run_state : RunState
            The run to laod.
        """
        self.run = run_state
        self.state = app_state

        self.left_json_text.configure(state="normal")
        self.left_json_text.delete(0.0, "end")
        self.left_json_text.insert(0.0, self.run["human_curated_domain"])
        self.left_json_text.configure(state="disabled")

        self.right_json_text.configure(state="normal")
        self.right_json_text.delete(0.0, "end")
        self.right_json_text.insert("0.0", self.run["generated_domain"])
        self.right_json_text.configure(state="disabled")

        self.source_node_text.configure(state="normal")
        self.source_node_text.delete(0.0, "end")
        self.source_node_text.insert(0.0, self.run["reference_nodes"])
        self.source_node_text.configure(state="disabled")

        self.parameter_set_text.configure(state="normal")
        self.parameter_set_text.delete(0.0, "end")
        self.parameter_set_text.insert("0.0", self.run["param_set"])
        self.parameter_set_text.configure(state="disabled")

        self.score_frame.update_state(app_state=app_state, run_state=self.run)

    def get_results(self) -> EvalData:
        """Returns the score evaluations."""
        score_eval = self.score_frame.get_results()
        eval_data = create_full_eval(score_eval=score_eval)
        return eval_data

    def _create_evaluate_tab(self) -> None:
        """Creates the evaluate tab view."""
        self.evaluate_frame = self.tab("Evaluate")
        self.evaluate_frame.grid_columnconfigure(0, weight=0)
        self.evaluate_frame.grid_rowconfigure(0, weight=0)
        self.evaluate_frame.grid_columnconfigure(1, weight=0)
        self.evaluate_frame.grid_rowconfigure(1, weight=0)
        self.evaluate_frame.grid_columnconfigure(2, weight=2)
        self.evaluate_frame.grid_rowconfigure(2, weight=2)

        self.score_frame = ScoreFrame(
            master=self.evaluate_frame, app_state=self.state, run_state=self.run
        )
        self.score_frame.grid(
            row=0, column=0, padx=self.state["padding"], pady=self.state["padding"]
        )

        self.err_frame = ErrorFrame(
            master=self.evaluate_frame, app_state=self.state, run_state=self.run
        )
        self.err_frame.grid(
            row=0, column=1, padx=self.state["padding"], pady=self.state["padding"]
        )

    def _create_compare_json_tab(self) -> None:
        """Creates the compare JSON tab view."""
        self.compare_frame = self.tab("Compare JSON")
        self.compare_frame.grid_columnconfigure(0, weight=1)
        self.compare_frame.grid_columnconfigure(1, weight=1)
        self.compare_frame.grid_rowconfigure(0, weight=0)
        self.compare_frame.grid_rowconfigure(1, weight=1)

        self.left_label = ctk.CTkLabel(
            master=self.compare_frame,
            text="Human Curated Domain",
            font=(self.state["font"], 18, "bold"),
        )
        self.left_label.grid(
            row=0, column=0, padx=self.state["padding"], pady=0, sticky="w"
        )

        self.left_json_text = ctk.CTkTextbox(
            master=self.compare_frame, wrap="none", font=(self.state["font"], 18)
        )
        self.left_json_text.grid(
            row=1,
            column=0,
            padx=(self.state["padding"], self.state["padding"] // 2),
            pady=(0, self.state["padding"] // 2),
            sticky="nsew",
        )
        self.left_json_text.configure(state="disabled")

        self.right_label = ctk.CTkLabel(
            master=self.compare_frame,
            text="Generated Domain",
            font=(self.state["font"], 18, "bold"),
        )
        self.right_label.grid(
            row=0,
            column=1,
            padx=(self.state["padding"] // 2, self.state["padding"]),
            pady=0,
            sticky="w",
        )

        self.right_json_text = ctk.CTkTextbox(
            master=self.compare_frame, wrap="none", font=(self.state["font"], 18)
        )
        self.right_json_text.grid(
            row=1,
            column=1,
            padx=(self.state["padding"] // 2, self.state["padding"]),
            pady=(0, self.state["padding"] // 2),
            sticky="nsew",
        )
        self.right_json_text.configure(state="disabled")

    def _create_source_node_tab(self) -> None:
        """Creates the source node tab."""
        self.source_node_frame = self.tab("Source Nodes")
        self.source_node_frame.grid_columnconfigure(0, weight=1)
        self.source_node_frame.grid_rowconfigure(0, weight=1)

        self.source_node_text = ctk.CTkTextbox(
            master=self.source_node_frame, wrap="none", font=(self.state["font"], 18)
        )
        self.source_node_text.grid(
            row=0,
            column=0,
            padx=self.state["padding"],
            pady=self.state["padding"],
            sticky="nsew",
        )
        self.source_node_text.configure(state="disabled")

    def _create_parameter_set_tab(self) -> None:
        """Creates the parameter set tab."""
        self.parameter_set_frame = self.tab("Parameter Set")
        self.parameter_set_frame.grid_columnconfigure(0, weight=1)
        self.parameter_set_frame.grid_rowconfigure(0, weight=1)

        self.parameter_set_text = ctk.CTkTextbox(
            master=self.parameter_set_frame, wrap="none", font=(self.state["font"], 18)
        )
        self.parameter_set_text.grid(
            row=0,
            column=0,
            padx=self.state["padding"],
            pady=self.state["padding"],
            sticky="nsew",
        )
        self.parameter_set_text.configure(state="disabled")
