import customtkinter as ctk
from tkinter import ttk, messagebox
from database_helper import DatabaseHelper

class AssemblyWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Окно сброса")
        self.geometry("600x400")

        self.db_helper = DatabaseHelper()

        self.title_label = ctk.CTkLabel(self, text="Сборка компьютера", font=("Arial", 16))
        self.title_label.pack(pady=20)

        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.pack(padx=20, pady=20, fill="both", expand=True)

        self.frame = ctk.CTkFrame(self.scrollable_frame)
        self.frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.selected_components = []
        self.create_component_selector("Процессор", "processors")
        self.create_component_selector("Материнская плата", "motherboards")
        self.create_component_selector("Видеокарта", "graphics_cards")
        self.create_component_selector("Оперативная память", "ram")
        self.create_component_selector("Жесткий диск", "hard_drives")
        self.create_component_selector("Клавиатура", "keyboards")
        self.create_component_selector("Мышка", "mice")
        self.create_component_selector("Монитор", "monitors")
        self.create_component_selector("Блок питания", "power_supplies")
        self.create_component_selector("Корпус компьютера", "cases")

        self.create_contact_fields()

        self.total_price_label = ctk.CTkLabel(self, text = "Общая цена: 0 рублей", font=("Arial", 14))
        self.total_price_label.pack(pady=10)

        self.assemble_button = ctk.CTkButton(self, text="Собрать", command=self.complete_order)
        self.assemble_button.pack(pady=10)

    def create_component_selector(self, component_name, table_name):
        component_label = ctk.CTkLabel(self.frame, text=f"{component_name}" + ":")
        component_label.pack(anchor="w")

        component_options = self.get_component_options(table_name)
        component_combobox = ttk.Combobox(self.frame, values=component_options)           
        component_combobox.pack(pady=5, fill="x")
        component_combobox.bind("<<ComboboxSelected>>", lambda e: self.update_total_price())

    def get_component_options(self, table_name):
       self.db_helper.corner.execute(f"SELECT name FROM {table_name}")
       components = self.db_helper.corner.fetchall()
       return [component[0] for component in components]
    
    def update_total_price(self):
       self.selected_components = []

       for widget in self.frame.winfo_children():
           if isinstance(widget, ttk.Combobox):
               selected_component = widget.get()
               if selected_component:
                   self.selected_components.append(selected_component)
                   self.check_last_unit(selected_component)
       
       total_price = 0
       for component in self.selected_components:
           for table_name in ["processors", "motherboards", "graphic_cards", "ram", "hard_drives", "power_supplies", "cases"]:
               self.db_helper.cursor.execute(f"SELECT price FROM {table_name} WHERE name = ?", (component,))
               result = self.db_helper.cursor.fetchone()
               if result:
                   total_price += result[0]
                   self.total_price_label.configure(text=f"Общая цена: {total_price} рублей")

    def check_last_unit(self, component_name):
        for table_name in ["processors", "motherboards", "graphic_cards", "ram", "hard_drives", "power_supplies", "cases"]:
            self.db_helper.cursor.execute(f"SELECT price FROM {table_name} WHERE name = ?", (component_name,))
            result = self.db_helper.cursor.fetchone()
            if result:
                quantity = result[0]
                if quantity == 1:
                    messagebox.showwarning("Внимание", f"Последняя единица товара: {component_name}")

    def create_contact_fields(self):
        contact_frame = ctk.CTkFrame(self)
        contact_frame.pack(padx=20, pady=10, fill="x")

        contact_frame.grid_rowconfigure(0, weight=1)
        contact_frame.grid_rowconfigure(1, weight=1)
        contact_frame.grid_rowconfigure(2, weight=1)
        contact_frame.grid_rowconfigure(3, weight=1)
        contact_frame.grid_rowconfigure(4, weight=1)

        self.last_name_entry = ctk.CTkEntry(contact_frame, placeholder_text="Фамилия")
        self.last_name_entry.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.last_name_entry = ctk.CTkEntry(contact_frame, placeholder_text="Имя")
        self.last_name_entry.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        self.last_name_entry = ctk.CTkEntry(contact_frame, placeholder_text="Отчество")
        self.last_name_entry.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        self.last_name_entry = ctk.CTkEntry(contact_frame, placeholder_text="Телефон")
        self.last_name_entry.grid(row=3, column=0, padx=5, pady=5, sticky="ew")
        self.last_name_entry = ctk.CTkEntry(contact_frame, placeholder_text="Электронная почта")
        self.last_name_entry.grid(row=4, column=0, padx=5, pady=5, sticky="ew")

    def complete_order(self):
        last_name = self.last_name_entry.get()
        first_name = self.first_name_entry.get()
        middle_name = self.middle_name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()

        if not self.selected_components:
            messagebox.showewarning("Предупреждение", "Выберите хотя бы один компанент.")

        order_data = []
        total_price = 0

        for component in self.selected_components:
            for table_name in ["processors", "motherboards", "graphic_cards", "ram", "hard_drives", "power_supplies", "cases"]:
                self.db_helper.cursor.execute(f"SELECT price FROM {table_name} WHERE name = ?", (component,))
                result = self.db_helper.cursor.fetchone()
                if result:
                    name, price, quantity = result
                    if quantity > 0:
                        order_data.append((name, price, 1))
                        total_price += price
                        self.db_helper.cursor.execute(f"UPDATE {table_name} SET quantity = quantity - 1 WHERE name = ?", (component,)) 
                    else:
                        messagebox.showerror("Ошибка", f"Компанент {component} не доступен.")
                        return
        self.db_helper.conn.commit()
        order_id = self.db_helper.add_order(last_name, first_name, middle_name, phone, email, total_price)
        if order_id is not None:
            for companent_name, price, quantity in order_data:
                self.db_helper.add_order(order_id, companent_name, price, quantity)
            
            self.db_helper.conn.commit()
            messagebox.showinfo("Успех", "Компоненты оформлены. Количество комплектующих обнавлено.")
        else:
            messagebox.showerror("Ошибка", "Не удалось создать заказ.")

                                             









    