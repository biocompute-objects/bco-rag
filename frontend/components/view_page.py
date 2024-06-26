import customtkinter as ctk  # type: ignore
from frontend.components.tab_view import TabView
from logging import Logger
from typing import Callable
import json
import os


class ViewPage(ctk.CTkFrame):

    def __init__(
        self,
        master: ctk.CTk,
        logger: Logger,
        user_data_entry: dict[str, dict],
        beginning: bool,
        generated_path: str,
        human_curated_path: str,
        source_node_path: str,
        param_set: str,
        navigate_callback: Callable[[int, dict[str, dict], bool, bool, int], None],
        run_index: int,
        total_runs: int,
        direction: int,
        user_data_path: str = os.path.join("./evaluations_results", "user_data.json"),
        standard_padding: int = 20,
        standard_font: str = "Helvetica",
        **kwargs,
    ):
        """"""
        super().__init__(master, **kwargs)

        self.logger = logger
        self.user_data_entry = user_data_entry
        self.beginning = beginning
        self.domain = os.path.basename(generated_path.split("-")[0])
        self.navigate_callback = navigate_callback
        self.run_index = run_index
        self.total_runs = total_runs
        self.param_set = param_set
        self._user_data_path = user_data_path
        self._padding = standard_padding
        self._font = standard_font

        self._create_sidebar()

        self.already_evaluated = False
        overwrite_flag = False
        # this is pretty messy
        if (
            os.path.basename(generated_path)
            in user_data_entry[list(user_data_entry.keys())[0]]
        ):
            self.already_evaluated = True
        # if continuing session, skip generated domains already seen
        if not self.beginning and self.already_evaluated:
            if self.run_index >= self.total_runs - 1:
                self._create_view_all_page()
            else:
                if direction == 1:
                    self._on_next()
                elif direction == -1:
                    if self.run_index - 1 < 0:
                        return
                    self._on_prev()
        elif self.beginning and self.already_evaluated:
            overwrite_flag = True

        self.human_curated_domain = json.dumps(
            {
                f"{self.domain}_domain": json.load(open(human_curated_path, "r"))[
                    f"{self.domain}_domain"
                ]
            },
            indent=4,
        )
        self.source_nodes_txt = open(source_node_path, "r").read()

        if os.path.isfile(generated_path):
            self.generated_domain = json.dumps(
                json.load(open(generated_path, "r")), indent=4
            )
        else:
            raw_txt = open(generated_path.replace(".json", ".txt")).read()
            self.generated_domain = (
                f"Failed JSON deserialization. Raw text output:\n\n{raw_txt}"
            )

        self.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._create_tab_view(overwrite_flag)

    def _create_sidebar(self):
        """"""
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=1, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(3, weight=1)

        y_padding = self._padding + 20
        y_half_padding = y_padding // 2

        self.navigate_label = ctk.CTkLabel(
            self.sidebar_frame, text="Navigate", font=(self._font, 16, "bold")
        )
        self.navigate_label.grid(
            row=0,
            column=0,
            padx=self._padding,
            pady=(y_padding, y_half_padding),
        )

        self.prev_button = ctk.CTkButton(
            master=self.sidebar_frame,
            text="Previous",
            command=self._on_prev,
            state=("normal" if self.run_index > 0 else "disabled"),
        )
        self.prev_button.grid(
            row=1,
            column=0,
            padx=self._padding,
            pady=y_half_padding,
        )

        self.next_button = ctk.CTkButton(
            master=self.sidebar_frame,
            text="Next",
            command=self._on_next,
            state=("normal" if self.run_index < self.total_runs - 1 else "disabled"),
        )
        self.next_button.grid(row=2, column=0, padx=self._padding, pady=y_half_padding)

        self.appearance_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="Appearance:",
            anchor="w",
            font=(self._font, 16, "bold"),
        )
        self.appearance_label.grid(
            row=4, column=0, padx=self._padding, pady=(y_padding, y_half_padding)
        )

        self.appearance_option_menu = ctk.CTkOptionMenu(
            self.sidebar_frame,
            values=["Light", "Dark", "System"],
            command=self._change_appearance_mode,
        )
        self.appearance_option_menu.grid(
            row=5,
            column=0,
            padx=self._padding,
            pady=y_half_padding,
        )

        self.scaling_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="UI Scaling:",
            anchor="w",
            font=(self._font, 16, "bold"),
        )
        self.scaling_label.grid(
            row=6, column=0, padx=self._padding, pady=y_half_padding
        )

        self.scaling_option_menu = ctk.CTkOptionMenu(
            self.sidebar_frame,
            values=["70%", "80%", "90%", "100%", "110%", "120%", "130%"],
            command=self._change_scaling_event,
        )
        self.scaling_option_menu.grid(
            row=7,
            column=0,
            padx=self._padding,
            pady=y_half_padding,
        )

    def _create_view_all_page(self) -> None:
        """"""
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.info_label = ctk.CTkLabel(
            master=self,
            text="You've evaluated all generated domains!",
            font=(self._font, 32, "bold"),
        )
        self.info_label.grid(row=0, column=0, padx=self._padding, pady=self._padding)

    def _change_appearance_mode(self, new_appearance_mode: str) -> None:
        """"""
        ctk.set_appearance_mode(new_appearance_mode)

    def _change_scaling_event(self, new_scaling: str) -> None:
        """"""
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    def _create_tab_view(self, overwrite_flag: bool) -> None:
        """"""
        self.tab_view = TabView(
            master=self,
            top_json=self.human_curated_domain,
            bottom_json=self.generated_domain,
            source_nodes=self.source_nodes_txt,
            param_set=self.param_set,
            overwrite_flag=overwrite_flag,
            standard_padding=self._padding,
            standard_font=self._font,
        )
        self.tab_view.grid(
            row=0, column=0, padx=self._padding, pady=self._padding, sticky="nsew"
        )

    def _on_prev(self):
        """"""
        if self.run_index > 0:
            self.navigate_callback(
                self.run_index - 1,
                self.user_data_entry,
                self.beginning,
                self.already_evaluated,
                -1,
            )

    def _on_next(self):
        """"""
        if self.run_index < self.total_runs - 1:
            self.navigate_callback(
                self.run_index + 1,
                self.user_data_entry,
                self.beginning,
                self.already_evaluated,
                1,
            )
