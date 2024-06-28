import customtkinter as ctk  # type: ignore


class App(ctk.CTk):
    """Frontend for evaluating generated BCO domains from
    BcoRag.
    """

    def __init__(self, standard_padding: int = 20, standard_font: str = "Helvetica"):
        """Constructor."""
        super().__init__()
