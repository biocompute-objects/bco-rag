import glob
import sys
import os
import json
import customtkinter as ctk  # type: ignore
from .components import LoginScreen, IntermediateScreen, ViewPage
from logging import Logger


class App(ctk.CTk):
    """Frontend for evaluating generated BCO domains from the BcoRag.

    Attributes
    ----------
    logger : Logger
        The frontend logger.

    """

    def __init__(
        self,
        logger: Logger,
        output_path: str = "./output",
        glob_pattern: str = "**",
        results_path: str = "./evaluation_results",
        standard_padding: int = 20,
        standard_font: str = "Helvetica",
    ):
        """Constructor.

        Parameters
        ----------
        logger : Logger
            The frontend logger.
        output_path : str (default: "./output")
            Path to directory where the BcoRag outputs are located.
        glob_pattern : str (default: "**")
            Glob pattern to search for output sub-directories/files.
        results_path : str (default: "./evaluation_results")
            Path to the evaluations directory.
        standard_padding : int (default: 20)
            Standard base padding for the frontend widgets.
        standard_font : str (default: Helvetica)
            Standard font for the frontend widgets.
        """

        super().__init__()
        self.logger = logger
        self.output_path = output_path

        directories = glob.glob(os.path.join(self.output_path, glob_pattern))
        self.directories = [
            x for x in directories if ("README" not in x) and ("human_curated" not in x)
        ]

        self.results_path = results_path
        self.results_data = json.load(
            open(os.path.join(self.results_path, "evaluations.json"), "r")
        )

        self._padding = standard_padding
        self._font = standard_font

        self.title("BCO RAG Evaluator")
        self.geometry(f"{1920}x{1080}")

        self.grid_columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.login_screen = LoginScreen(
            master=self,
            logger=self.logger,
            on_login_success=self.on_login_success,
            user_source_path=os.path.join(self.results_path, "users.json"),
            user_data_path=os.path.join(self.results_path, "user_data.json"),
            standard_padding=20,
            standard_font="Helvetica",
        )
        self._create_paper_keys()

    def on_login_success(self, user_data_entry: dict[str, dict], user_hash: str):
        """Callback function to execute on login success.

        Parameters
        ----------
        user_data_entry : dict[str, dict]
            The user evaluation entry containing the data for the user evaluations.
        user_hash : str
            The user hash string.
        """
        self.login_screen.grid_forget()
        self.intermediate_screen = IntermediateScreen(
            master=self,
            user_data_entry=user_data_entry,
            user_hash=user_hash,
            on_start=self.on_start,
            standard_padding=20,
            standard_font="Helvetica",
        )
        self.intermediate_screen.grid(
            row=0, column=0, padx=self._padding, pady=self._padding
        )

    def on_start(self, beginning: bool, user_data_entry: dict[str, dict]) -> None:
        """Callback function to execute on evaluation start.

        Parameters
        ----------
        beginning : bool
            Whether the user chose to start from the beginning or
            from last session.
        user_data_entry : dict[str, dict]
             The user's current data entry containing information on the user's evaluations.
        """
        self.intermediate_screen.grid_forget()
        self.current_directory_index = 0
        self.current_run_index = 0
        self.total_runs = self._get_total_runs()
        self._load_run(self.current_run_index, user_data_entry, beginning)

    def _load_run(
        self, run_index: int, user_data_entry: dict[str, dict], beginning: bool
    ) -> None:
        """Loads the current run info.

        Parameters
        ----------
        run_index : int
            The run index to load.
        user_data_entry : dict[str, dict]
             The user's current data entry containing information on the user's evaluations.
        beginning : bool
            Whether to skip over already evaluated generated domains.
        """
        current_run = 0

        for directory in self.directories:

            output_map = json.load(
                open(os.path.join(directory, "output_map.json"), "r")
            )

            for domain in output_map:
                for domain_param_set in output_map[domain]:
                    for domain_run in domain_param_set["entries"]["runs"]:

                        if current_run == run_index:

                            human_curated_path = os.path.join(
                                self.output_path,
                                "human_curated",
                                f"{os.path.basename(directory)}.json",
                            )
                            if not os.path.isfile(human_curated_path):
                                self.logger.error(
                                    f"Human curated file not found at filepath `{human_curated_path}`"
                                )
                                print(
                                    f"Human curated file not found at filepath `{human_curated_path}`"
                                )
                                sys.exit(1)

                            self._show_view_page(
                                user_data_entry=user_data_entry,
                                beginning=beginning,
                                generated_path=domain_run["json_file"],
                                human_curated_path=human_curated_path,
                                source_node_path=domain_run["source_node_file"],
                                param_set="",
                                run_index=run_index,
                                total_runs=self.total_runs,
                            )

                            return

                        current_run += 1

    def _show_view_page(
        self,
        user_data_entry: dict[str, dict],
        beginning: bool,
        generated_path: str,
        human_curated_path: str,
        source_node_path: str,
        param_set: str,
        run_index: int,
        total_runs: int,
    ) -> None:
        """"""
        self.view_page = ViewPage(
            master=self,
            user_data_entry=user_data_entry,
            beginning=beginning,
            logger=self.logger,
            generated_path=generated_path,
            human_curated_path=human_curated_path,
            source_node_path=source_node_path,
            param_set=param_set,
            navigate_callback=self._navigate_to_path,
            run_index=run_index,
            total_runs=total_runs,
        )

    def _navigate_to_path(
        self, run_index: int, user_data_entry: dict[str, dict], beginning: bool
    ) -> None:
        """"""
        self.view_page.grid_forget()
        self._load_run(run_index, user_data_entry, beginning)

    def _get_total_runs(self) -> int:
        """Gets the total number of runs in the output directory. Used
        for determining when to disable the previous and next buttons.

        Returns
        -------
        int
            The total number of runs.
        """
        total_runs = 0
        for directory in self.directories:
            output_map = json.load(
                open(os.path.join(directory, "output_map.json"), "r")
            )
            for domain in output_map:
                for domain_param_set in output_map[domain]:
                    total_runs += len(domain_param_set["entries"]["runs"])
        return total_runs

    def _create_paper_keys(self) -> None:
        """"""
        base_directories = {os.path.basename(x) for x in self.directories}
        for paper in base_directories:

            if paper not in self.results_data:

                self.results_data[paper] = {}

        json.dump(self.results_data, open(self.results_path, "w"), indent=4)
