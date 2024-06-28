import customtkinter as ctk  # type: ignore


class TabView(ctk.CTkTabview):

    def __init__(
        self,
        master: ctk.CTk | ctk.CTkFrame,
        top_json: str,
        bottom_json: str,
        source_nodes: str,
        param_set: str,
        overwrite_flag: bool,
        standard_padding: int = 20,
        standard_font: str = "Helvetica",
        **kwargs
    ):
        """Constructor.

        Parameters
        ----------
        master : CTk or CTkFrame
            The parent component/widget.
        """
        super().__init__(master, **kwargs)

        self._padding = standard_padding
        self._font = standard_font

        self.add("Compare JSON")
        self.add("Source Nodes")
        self.add("Parameter Set")
        self.add("Evaluate")

        self._create_compare_json(top_json, bottom_json, overwrite_flag)
        self._create_text_file_tab(source_nodes)
        self._create_param_set_tab(param_set)
        self._create_evaluate_tab()

    def _create_evaluate_tab(self) -> None:
        """"""
        evaluate_tab = self.tab("Evaluate")

    def _create_compare_json(
        self, top_json: str, bottom_json: str, overwrite_flag: bool
    ):
        """"""
        compare_frame = self.tab("Compare JSON")
        compare_frame.grid_columnconfigure(0, weight=1)
        compare_frame.grid_rowconfigure(0, weight=0)
        compare_frame.grid_rowconfigure(1, weight=1)
        compare_frame.grid_rowconfigure(2, weight=0)
        compare_frame.grid_rowconfigure(3, weight=1)
        compare_frame.grid_rowconfigure(4, weight=0)

        top_label = ctk.CTkLabel(
            master=compare_frame,
            text="Human Curated Domain",
            font=(self._font, 14, "bold"),
        )
        top_label.grid(
            row=0,
            column=0,
            padx=self._padding,
            pady=(self._padding // 5, 0),
            sticky="w",
        )

        self.top_json_text = ctk.CTkTextbox(
            master=compare_frame, wrap="none", font=(self._font, 18)
        )
        self.top_json_text.grid(
            row=1,
            column=0,
            padx=self._padding,
            pady=(0, self._padding // 2),
            sticky="nsew",
        )
        self.top_json_text.insert("0.0", top_json)
        self.top_json_text.configure(state="disabled")

        bottom_label = ctk.CTkLabel(
            master=compare_frame, text="Generated Domain", font=(self._font, 14, "bold")
        )
        bottom_label.grid(
            row=2,
            column=0,
            padx=self._padding,
            pady=(self._padding // 5, 0),
            sticky="w",
        )

        self.bottom_json_text = ctk.CTkTextbox(
            master=compare_frame, wrap="none", font=(self._font, 18)
        )
        self.bottom_json_text.grid(
            row=3,
            column=0,
            padx=self._padding,
            pady=(0, self._padding // 2),
            sticky="nsew",
        )
        self.bottom_json_text.insert("0.0", bottom_json)
        self.bottom_json_text.configure(state="disabled")

        if overwrite_flag:
            bottom_note_label = ctk.CTkLabel(
                master=compare_frame,
                text="Note: Overwriting existing evaluation.",
                font=(self._font, 14, "bold"),
                text_color="red",
            )
            bottom_note_label.grid(
                row=4, column=0, padx=0, pady=0, sticky="w"
            )

    def _create_text_file_tab(self, text_content: str):
        """"""
        text_frame = self.tab("Source Nodes")
        text_frame.grid_columnconfigure(0, weight=1)
        text_frame.grid_rowconfigure(0, weight=1)

        self.text_file_textbox = ctk.CTkTextbox(
            master=text_frame, wrap="none", font=(self._font, 18)
        )
        self.text_file_textbox.grid(
            row=0, column=0, padx=self._padding, pady=self._padding, sticky="nsew"
        )
        self.text_file_textbox.insert("0.0", text_content)
        self.text_file_textbox.configure(state="disabled")

    def _create_param_set_tab(self, param_set: str):
        """"""
        param_set_frame = self.tab("Parameter Set")
        param_set_frame.grid_columnconfigure(0, weight=1)
        param_set_frame.grid_rowconfigure(0, weight=1)

        self.param_set_textbox = ctk.CTkTextbox(master=param_set_frame, wrap="none", font=(self._font, 19))
        self.param_set_textbox.grid(row=0, column=0, padx=self._padding, pady=self._padding, sticky="nsew")
        self.param_set_textbox.insert("0.0", param_set)
        self.param_set_textbox.configure(state="disabled")
