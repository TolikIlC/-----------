import customtkinter as ctk
from tkinter import messagebox
from database_helper import DatabaseHelper

class CompletionWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Окно документации")
        self.geometry("600x400")

        self.db_helper = DatabaseHelper()

        self.title_label = ctk.CTkLabel(self, text="Документация", font=("Arial", 16))
        self.title_label.pack(pady=20)

        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.pack(padx=20, pady=20, fill="both", expand=True)

        self.frame = ctk.CTkFrame(self.scrollable_frame)
        self.frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.component_quantities = {}

        self.display_components = {}

        self.save_button = ctk.CTkButton(self, text="Готово", command=self.save_changes)
        self.save_button.pack(pady=10)

    def display_comments(self):
        component_tables = {
        "Процессоры": "processors",
        "Материнские платы": "motherboards",
        "Видеокарты": "graphics_cards",
        "Оперативная память": "ram",
        "Жесткие диски": "hard_drives",
        "Блоки питания": "power_supplies",
        "Корпусы компьютера": "cases"
        }

        self.component_frames = {}

        for category, table_name in component_tables.items():
            ctk.CTkLabel(self.frame, text=category, font=("Arial", 14, "bold")).pack(anchor="w", pady=(10, 5))

            self.db_helper.cursor.execute(f"SELECT name, specs, price, quantity FROM {table_name}")
            components = self.db_helper.cursor.fetchall()

            for component in components:
                name, specs, price, quantity = component
                component_info = f"{name}: {specs},{price} рублей, Количество: {quantity}"

                component_frame = ctk.CTkFrame(self.frame)
                component_frame.pack(pady=5, fill="x")

                component_label = ctk.CTkLabel(component_frame, text=component_info, font=("Arial", 12))
                component_label.pack(side="left", padx=5)
                
                increase_button = ctk.CTkButton(component_frame, text="+", command=lambda name=name, label=component_label: self.increase_quantity(name, label), width=40, height=40)
                increase_button.pack(side="right", padx=5)

                decrease_button = ctk.CTkButton(component_frame, text="-", command=lambda name=name, label=component_label: self.decrease_quantity(name, label), width=40, height=40)
                decrease_button.pack(side="right", padx=5)

                self.component_quantities[name] = quantity
                self.component_frames[name] = component_label

    def increase_quantity(self, component_name, component_label):
        if component_name in self.component_quantities:
            self.component_quantities[component_name] += 1
            self.update_component_label(component_name, component_label)

    def increase_quantity(self, component_name, component_label):
        if component_name in self.component_quantities:
            if self.component_quantities[component_name] > 0:
                self.component_quantities[component_name] -= 1
                self.update_component_label(component_name, component_label)

    def update_component_label(self, component_name, component_label):
        new_quantity = self.component_quantities[component_name]
        table_name = self.get_table_name(component_name)
        component_label.configure(text=f"{component_name}: {self.get_specs(table_name, component_name)}, {self.get_price(table_name, component_name)} рублей, Количество: {new_quantity}")

    def get_table_name(self,  component_name):
        component_tables = {
            "Процессоры": "processors",
            "Материнские платы": "motherboards",
            "Видеокарты": "graphics_cards",
            "Оперативная память": "ram",
            "Жесткие диски": "hard_drives",
            "Блоки питания": "power_supplies",
            "Корпусы компьютера": "cases"
        }
        for table_name, name in component_tables.items():
            self.db_helper.cursor.execute(f"SELECT name FROM {name} WHERE name = ?", (component_name,))
            if self.db_helper.cursor.fetchone():
                return name
            return None

    def get_specs(self, table_name, component_name):
        self.db_helper.cursor.execute(f"SELECT specs FROM {table_name} WHERE name = ?", (component_name,))
        specs = self.db_helper_cursor.fetchone()
        return specs[0] if specs else "Неизвестно"
    
    def get_price(self, table_name, component_name):
        self.db_helper.cursor.execute(f"SELECT specs FROM {table_name} WHERE name = ?", (component_name,))
        price = self.db_helper_cursor.fetchone()
        return price[0] if price else "Неизвестно"
    
    def save_changes(self):
        for component_name, new_quantity in self.component_quantites.items():
            table_name = self.get_table_name(component_name)
            if table_name:
                self.db_helper.cursor.execute(f"UPDATE {table_name} SET quantity = ? WHERE name = ?", (new_quantity, component_name))

            self.db_helper.conn.commit()
            messagebox.showinfo("Успех", "Изменения успешно сохранены.")
        
