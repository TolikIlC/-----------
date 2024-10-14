import customtkinter as ctk

class ContactsWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Контакты")
        self.geometry("300x200")
        self.resizable(False, False)

        self.attributes('-topmost', True)

        contacts_info = (
            "Начальство:\n"
            "Иванов Иван Иванович:\n"
            "Телефон: +7 (123) 456-78-90 \n\n"
            "Сотрудники:\n"
            "Петров Петр Петрович:\n"
            "Телефон: +7 (123) 456-78-91 \n\n"
            "Сидоров Сидор Сидорович:\n"
            "Телефон: +7 (123) 456-78-92"
        )

        contacts_label = ctk.CTkLabel(self, text=contacts_info, anchor='w', justify='left')
        contacts_label.pack(padx=10, pady=10)

        close_button = ctk.CTkButton(self, text="Закрыть", command=self.destroy)
        contacts_label.pack(pady=(0, 10))
