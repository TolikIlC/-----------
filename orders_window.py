import customtkinter as ctk
from tkinter import messagebox
from database_helper import DatabaseHelper

class OrdersWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Заказы")
        self.geometry("1200x600")

        self.db_helper = DatabaseHelper()

        self.title_label = ctk.CTkLabel(self, text="Список заказов", font=("Arial", 16))
        self.title_label.pack(pady=20)

        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.pack(padx=20, pady=20, fill="both", expand=True)

        self.table_frame = ctk.CTkFrame(self.scrollable_frame)
        self.table_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.x_scroll = ctk.CTkScrollbar(self.table_frame, orientation = "horizontal")
        self.x_scroll.pack(side="bottom", fill="x")
        self.y_scroll = ctk.CTkScrollbar(self.table_frame, orientation = "vertical")
        self.y_scroll.pack(side="right", fill="y")

        self.header_frame = ctk.CTkFrame(self.table_frame)
        self.header_frame.pack(fill="x")

        headers = ["ID заказа", "Фамилия", "Имя", "Отчество", "Телефон", "Email", "Компоненты", "Итоговая цена"]
        for header in headers:
            ctk.CTkLabel(self.header_frame, text=header, font=("Arial", 12, "bold"), width=150, anchor="w").pack(side="left", padx=5, pady=5)

        self.data_frame = ctk.CTkFrame(self.table_frame)
        self.data_frame.pack(fill="both", expand=True)

        self.load_button = ctk.CTkButton(self, text="Загрузить данные", command=self.load_data)
        self.load_button.pack(pady=10)

    def load_data(self):
        for widget in self.data_frame.winfo_children():
            widget.destroy()

        query = """
        SELECT o.id AS order_id, o.last_name, o.first_name, o.middle_name, o.phone, o.email
        FROM orders o
        """

        self.db_helper.cursor.execute(query)
        orders = self.db_helper.cursor.fetchall()

        for order in orders:
            order_id, last_name, first_name, middle_name, phone, email = order

            item_query = """
            SELECT component_name, price, quantity
            FROM order_items
            WHERE order_id = ?
            """
            self.db_helper.cursor.execute(item_query, (order_id,))
            items = self.db_helper.cursor.fetchall()

            components_str = "\n".join([f"{item[0]} - Цена: {item[1]}, Кол-во: {item[2]}" for item in items])

            total_price = sum(item[1] * item[2] for item in items)

            self.add_row(order_id, last_name, first_name, middle_name, phone, email, components_str, total_price)

    def add_row(self, order_id, last_name, first_name, middle_name, phone, email, components_str, total_price):
        row_frame = ctk.CTkFrame(self.data_frame, corner_radius=0)
        row_frame.pack(fill="x", padx=5, pady=5)

        data = [order_id, last_name, first_name, middle_name, phone, email, components_str, total_price]
        for item in data:
            ctk.CTkLabel(row_frame, text=item, width=150, anchor="w", wraplength=150).pack(side="left", padx=5, pady=2)