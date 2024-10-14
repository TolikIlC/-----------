from typing import Tuple
import customtkinter as ctk 
from tkinter import messagebox
from database_helper import DatabaseHelper

class CompleteWindow(ctk.CTk):
    def __init__(self, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__()
        
        self.title("Окно докомплектации")
        self.geometry("600x400")
