import customtkinter as ctk

class EditOrderWindow(ctk.CTk):
    def __init__(self, order, database_repair, on_close_callback):
        super().__init__()
        self.title("Редактировать заявку")
        self.geometry("400x400")

        self.order = order
        self.database_repair = database_repair
        self.on_close_callback = on_close_callback

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)

        ctk.CTkLabel(self, text="Фамилия").grid(row=0, column=0, padx=10, pady=5, sticky='e')
        self.surname_entry = ctk.CTkEntry(self, placeholder_text="Фамилия")
        self.surname_entry.insert(0, order['surname'])
        self.surname_entry.grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(self, text="Имя").grid(row=1, column=0, padx=10, pady=5, sticky='e')
        self.surname_entry = ctk.CTkEntry(self, placeholder_text="Имя")
        self.surname_entry.insert(0, order['first_name'])
        self.surname_entry.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkLabel(self, text="Отчество").grid(row=2, column=0, padx=10, pady=5, sticky='e')
        self.surname_entry = ctk.CTkEntry(self, placeholder_text="Отчество")
        self.surname_entry.insert(0, order['patronymic'])
        self.surname_entry.grid(row=2, column=1, padx=10, pady=5)

        ctk.CTkLabel(self, text="Комплектующие").grid(row=3, column=0, padx=10, pady=5, sticky='e')
        self.surname_entry = ctk.CTkEntry(self, values=["Материнская капитал", "Процессор", "Оперативаня память", "Жесткий диск", "Видеокарта"])
        self.surname_entry.insert(0, order['components'])
        self.surname_entry.grid(row=3, column=1, padx=10, pady=5)

        ctk.CTkLabel(self, text="Описание проблемы").grid(row=4, column=0, padx=10, pady=5, sticky='e')
        self.surname_entry = ctk.CTkEntry(self, placeholder_text="Описание проблемы")
        self.surname_entry.insert(0, order['problem_description'])
        self.surname_entry.grid(row=4, column=1, padx=10, pady=5)

        ctk.CTkLabel(self, text="Телефон").grid(row=5, column=0, padx=10, pady=5, sticky='e')
        self.surname_entry = ctk.CTkEntry(self, placeholder_text="Телефон")
        self.surname_entry.insert(0, order['phone'])
        self.surname_entry.grid(row=5, column=1, padx=10, pady=5)

        ctk.CTkLabel(self, text="Email").grid(row=6, column=0, padx=10, pady=5, sticky='e')
        self.surname_entry = ctk.CTkEntry(self, placeholder_text="Email")
        self.surname_entry.insert(0, order['email'])
        self.surname_entry.grid(row=6, column=1, padx=10, pady=5)

        ctk.CTkLabel(self, text="Ожидаемая дата завершения").grid(row=7, column=0, padx=10, pady=5, sticky='e')
        self.surname_entry = ctk.CTkEntry(self, placeholder_text="Ожидаемая дата завершения")
        self.surname_entry.insert(0, order['expected_completion_date'])
        self.surname_entry.grid(row=7, column=1, padx=10, pady=5)

        save_button = ctk.CTkButton(self, text="Сохранить", command=self.save_order)
        save_button.grid(row=8, column=0, columnspan=2, pady=10)

    def save_order(self):
        self.database_repair.cursor.execute('''
        UPDATE repair_orders SET surname=?, first_name=?, patronymic=?, components=?,
        problem_decscription=?, phone=?, email=?, expected_completion_date=?
        WHERE id=?
        ''',(
            self.surname_entry.get(),
            self.first_name_entry.get(),
            self.components_combobox.get(),
            self.problem_description_entry.get(),
            self.phone_entry.get(),
            self.email_entry.get(),
            self.expected_completion_date_entry.get(),
            self.order['id']
        ))
        self.database_repair.conn.commit()
        self.on_close_callback()
        self.destroy()