import customtkinter as ctk
from tkinter import messagebox, Listbox, MULTIPLE
from add_consumable_window import AddConsumableWindow
from database_repair import DatabaseRepair

class ConsumblesWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Расходники")
        self.geometry("600x600")
        self.resizable(False, False)

        self.database = DatabaseRepair()

        self.header_label = ctk.CTkLabel(self, text="Управление Расходниками", font=("Arial", 20, "bold"))
        self.header_label.pack(pady=20)

        self.label_order = ctk.CTkLabel(self, text="Выберите заявку:")
        self.label_order.pack(pady=10)

        self.orders = self.database.get_all_repair_orders()
        self.orders_names = [f"{order['id']} - {order['surname']} {order['first_name']} {order['patronymic']}" for order in self.orders]

        self.orders_combobox = ctk.CTkComboBox(self, values=self.orders_names)
        self.orders_combobox.pack(pady=10, padx=10, fill='x')

        self.label_consumable = ctk.CTkLabel(self, text="Выберите расходники:")
        self.label_consumable.pack(pady=10)

        self.consumable_frame = ctk.CTkScrollableFrame(self)
        self.consumable_frame.pack(pady=10, padx=10, fill='both', expand=True)

        self.update_consumables_list()

        self.add_button = ctk.CTkButton(self, text="Добавить расходник", command=self.open_add_consumable_window)
        self.add_button.pack(pady=10)

        self.take_materials_button = ctk.CTkButton(self, text="Взять материалы", command=self.take_materials)
        self.take_materials_button.pack(pady=10)

    def open_add_consumables_window(self):
        add_window = AddConsumableWindow(self)
        add_window.grab_set()

    def take_materials(self):
        selected_consumables = []

        for child in self.consumable_frame.winfo_children():
            if isinstance(child, ctk.CTkCheckBox) and child.get():
                consumable_id = child.cget("text").split(' - ')[0]
                selected_consumables.append(int(consumable_id))

        selected_order = self.orders_combobox.get()
        if selected_order:
            order_id = int(selected_order.split(' - ')[0])
            client_name = selected_order.split(' - ')[1]

            self.database.add_materials(order_id, client_name, selected_consumables)

            for consumable_id in selected_consumables:
                self.database.decrease_consumables_quantity(consumable_id, 1)

            messagebox.showinfo("Успех", f"Материалы успешно добавлены для заявки №{order_id}.")

            self.update_consumables_list()
        else:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите заявку.")

    def update_consumables_list(self):
        for widget in self.consumable_frame.winfo_children():
            widget.destroy()

        self.consumables = self.database.get_all_repair_consumables()

        for consumable in self.consumables:
            checkbox = ctk.CTkCheckBox(self.consumable_frame, text=f"{consumable['id']} - {consumable['name']} (Количество: {consumable['quantity']})")
            checkbox.pack(anchor='w', padx=10, pady=5)