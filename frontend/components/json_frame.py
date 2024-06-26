import customtkinter as ctk # type: ignore

class JsonFrame(ctk.CTkFrame):

    def __init__(self, master: ctk.CTk | ctk.CTkFrame | ctk.CTkTabview):
        """Constructor.

        Parameters
        ----------
        master : CTk, CTkFrame or CTkTabview
            The parent component/widget.
        """

