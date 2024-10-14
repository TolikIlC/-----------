import tkinter as tk
import customtkinter as ctk
from datetime import datetime
from database_window import DatabaseWindow
from assembly_window import AssemblyWindow
from completion_window import CompletionWindow
from orders_window import OrdersWindow
from repair_requests_window import RepairRequestWindow
from database_repair import DatabaseRepair
from edit_order_window import EditOrderWindow
from pdf_generator import generate_report
from contacts_window import ContactsWindow
from calendar_window import CalendarWindow
from statisctics_window import StatisticsWindow
from documentation_window import DocumentationWindow
import requests
from email_sender import EmailSender
import os
from dotenv import load_dotenv
import threading
from consumbles_window import ConsumblesWindow
from clients_window import ClientsWindow

class CustomWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Бас система")
        self.geometry("800x600")
        self.resizable(False, False)
        self.update_weather_interval = 20000

        self.update_weather_info()
        load_dotenv()

        self.database_repair = DatabaseRepair()

        self.time_frame = ctk.CTkFrame(self)
        self.time_frame.pack(pady=10, fill='x')

        self.time_label = ctk.CTkLabel(self.time_frame, text="", font=("Arial", 12))
        self.time_label.pack(side='bottom')

        self.calendar_icon = ctk.CTkLabel(self.time_frame, text="📅", font=("Arial", 25), cursor="hand2")
        self.calendar_icon.pack(side='bottom', padx=(10,0))

        self.calendar_icon.bind("<Enter>", self.show_task_info)
        self.calendar_icon.bind("<Enter>", self.hide_task_info)

        self.task_info_label = ctk.CTkLabel(self, width=250, height=150, corner_radius=10, fg_color="lightgray")
        self.task_info_label.place_forget()

        self.buttons_frame = ctk.CTkFrame(self)
        self.buttons_frame.pack(pady=10, fill="x")

        self.create_button("База данных", self.open_database_window).pack(side="left", padx=5)
        self.create_button("Сборка", self.open_assembly_window).pack(side="left", padx=5)
        self.create_button("Докомплектация", self.open_completion_window).pack(side="left", padx=5)
        self.create_button("Заказы", self.open_orders_window).pack(side="left", padx=5)
        self.create_button("Ремонт", self.open_repair_window).pack(side="left", padx=5)

        self.repair_frame = ctk.CTkFrame(self)
        self.repair_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.repair_scrollable_frame = ctk.CTkScrollableFrame(self.repair_frame)
        self.repair_scrollable_frame.pack(pady=5, padx=5, fill="both", expand=True)

        self.update_time()

        self.load_repair_data()

        self.theme = "light"
        ctk.set_appearance_mode(self.theme)

        self.buttons_frame = ctk.CTkFrame(self)
        self.buttons_frame.pack(pady=10, fill="x")

        self.toggle_theme_button = ctk.CTkButton(self.buttons_frame, text="Переключить тему", command=self.toggle_theme)
        self.toggle_theme_button.pack(side="left", padx=5)

        self.contacts_button = ctk.CTkButton(self.buttons_frame, text="Контакты", command=self.show_contacts)
        self.contacts_button.pack(side="left", padx=5)

        self.calendar_button = ctk.CTkButton(self.buttons_frame, text="Календарь", command=self.show_calendar)
        self.calendar_button.pack(side="left", padx=5)

        self.statistics_button = ctk.CTkButton(self.buttons_frame, text="Статистика", command=self.show_statistics)
        self.statistics_button.pack(side="left", padx=5)

        self.documentation_button = ctk.CTkButton(self.buttons_frame, text="Документация", command=self.show_documentation)
        self.documentation_button.pack(side="left", padx=5)

        self.mailing_button = ctk.CTkButton(self.buttons_frame, text="Рассылка", command=self.open_mailing_window)
        self.mailing_button.pack(side='left', padx=5)

        self.email_sender = EmailSender(
            smtp_server = os.getenv("SMTP_SERVER"),
            smtp_port = int(os.getenv("SMTP_PORT")),
            sender_email = os.getenv("SENDER_EMAIL"),
            sender_password = os.getenv("SENDER_PASSWORD")

        )

    def open_clients_window(self):
        clients_window = ClientsWindow(self)
        clients_window.mainloop()

    def open_mailing_window(self):
        subject = "Тема вашего письма"   
        body = "Текст вашего письма"
        json_file_path = os.path.join("Users", "users.json")

        threading.Thread(target=self.send_emails_thread, args=(json_file_path, subject, body)).start()

    def send_emails_thread(self, json_file_path, body, subject):
        try:
            self.email_sender.send_bulk_emails(json_file_path, subject, body)
            self.after(0, lambda: messagebox.showinfo("Успех", "Сообщения успешно отправлены!"))
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Ошибка", f"Ошибка во время рассылки: {e}"))

    def update_weather_info(self):
        try:
            response = requests.get("https://api.open-meteo.com/v1/forecast?latitude=55/7558&longitude=37.6173&current_weather=true")
            weather_data = response.json()
            
            temperature = weather_data['current_weather']['temperature']
            wind_speed = weather_data['current_weather']['wind_speed']

            self.title(f"Бас система - Темпераптура: {temperature}C, Ветер: {wind_speed} м/с")
        except Exception as e:
            print(f"Ошибка при получении данных о погоде: {e}")
            self.title("Бас система - Не удалось получить данные о погоде")
        
        self.after(self.update_weather_interval, self.update_weather_info)
    def show_task_info(self, event):
        current_date = datetime.now().strftime("%d.%m.%Y")    
        print(f"Текущая дата для проверки задач: {current_date}")

        tasks = self.database_repair.get_all_tasks()
        print(f"Все задачи в базе данных: {tasks}")

        tasks_today = [task for task in tasks if task['task_date'] == current_date]

        for widget in self.task_info_label.winfo_children():
            widget.destroy()

        self.task_info_label.configure(fg_color="transparent", width=350)
        self.task_info_label.place(x=290, y=100)
        self.task_info_label.pack_propagate(False)

        if tasks_today:
            for task in tasks_today:
                color = "green" if task['status'] == 'Выполнено' else 'black'

                task_label = ctk.CTkLabel(self.task_info_label, text=f"{task['task_date']}", text_color=color)
                task_label.pack(anchor='w', padx=5, pady=2)

            self.task_info_label.lift()
        else:
            self.task_info_label.configure(text="Нет задач")
            self.task_info_label.place(x=290, y=100)
            self.task_info_label.pack(fg_color="transparent")

        self.task_info_label.lift()

    def hide_task_info(self, event):
        self.task_info_label.place_forget()

    def create_button(self, text, command):
        """ Helper method to create buttons with common styling. """
        return ctk.CTkButton(self.buttons_frame, text=text, command=command)
    
    def update_time(self):
        now = datetime.now()
        formatted_time = now.strftime("Дата: %d.%m.%Y Время:%H:%M:%S")

        self.time_label.configure(text=formatted_time)

        self.after(1000, self.update_time)

    def open_database_window(self):
        database_window = DatabaseWindow()
        database_window.mainloop()

    def open_assembly_window(self):
        assembly_window = AssemblyWindow()
        assembly_window.mainloop()

    def open_completion_window(self):
        completion_window = CompletionWindow()
        completion_window.mainloop()

    def open_orders_window(self):
        orders_window = OrdersWindow()
        orders_window.mainloop()

    def open_repair_window(self):
        def on_repair_window_close():
            self.load_repair_data()

        repair_window = RepairRequestWindow(on_close_callback=on_repair_window_close)
        repair_window.mainloop()

    def load_repair_data(self):
        for widget in self.repair_scrollable_frame.winfo_children():
            widget.destroy()

        repair_orders = self.database_repair.get_all_repair_orders()

        for idx, order in enumerate(repair_orders, start=1):
            order_frame = ctk.CTkFrame(self.repair_scrollable_frame, border_width=0)
            order_frame.pack(fill="x", padx=10, pady=5)

            order_info = (
                f"Заявка №{idx}\n"
                f"Фамилия №{order['surname']}\n"
                f"Имя №{order['first_name']}\n"
                f"Отчество №{order['patronymic']}\n"
                f"Комплектцющие №{order['components']}\n"
                f"Описание проблемы №{order['problem_description']}\n"
                f"Телефон №{order['phone']}\n"
                f"Email №{order['email']}\n"
                f"Ожидаемая дата завершения №{order['expected_completion_date']}\n"
                f"Статус №{order['status']}\n"
            )

            info_label = ctk.CTkLabel(order_frame, text=order_info, anchor='w', justify='left')
            info_label.pack(side='left', fill='x', expand=True)

            button_frame = ctk.CTkFrame(order_frame)
            button_frame.pack(side="right")

            button_color = "#28a745" if order['status'] == 'Выполнено' else "#007bff"
            button_text = "Выполнео" if order['status'] == 'Выполнено' else "Выполнить"
            execute_button = ctk.CTkButton(button_frame, text=button_text, command=lambda o=order: self.execute_order(o),
                                           fg_color=button_color, border_width=0)
            execute_button.pack(side='top', padx=5, pady=2)

            delete_button = ctk.CTkButton(button_frame, text="Удалить", command=lambda o=order: self.delete_order(o),
                                          fg_color="#dc3545", border_width=0)
            delete_button.pack(side='top', padx=5, pady=2)

            edit_button = ctk.CTkButton(button_frame, text="Редактировать", command=lambda o=order: self.edit_order(o),
                                        fg_color="#ffc107", border_width=0)
            edit_button.pack(side='top', padx=5, pady=2)                           

            generate_button = ctk.CTkButton(button_frame, text="Формировть", command=lambda o=order: self.generate_report(o),
                                        fg_color="#007bff", border_width=0)             
            generate_button.pack(side='top', padx=5, pady=2)   
            
    def execute_order(self, order):
        self.database_repair.cursor.execute(
            "UPDATE repair_orders SET status = 'Выполнено' WHERE id = ?", (order['id'],)
        )
        self.database_repair.conn.commit()
        self.load_repair_data()

    def delete_order(self, order):
        self.database_repair.cursor.execute(
            "DELETE FROM repair_orders WHERE id = ?", (order['id'],)
        )
        self.database_repair.conn.commit()
        self.load_repair_data()

    def edit_order(self, order):
        edit_window = EditOrderWindow(order, self.database_repair, on_close_callback=self.load_repair_data)
        edit_window.mainloop()

    def generate_report(self, order):
        print(f"Формируется отчет для заявки №{order['id']}")

    def generate_report(self, order):
        pdf_filename = generate_report(order)
        print(f"Отчет для заявки №{order['id']} успешно создан {pdf_filename}")

    def toggle_theme(self):
        """ Переключение между темной и светлой темами. """
        if self.theme == "light":
            self.theme = "dark"
        else:
            self.theme = "light"

        ctk.set_appearance_mode(self.theme)

    def show_contacts(self):
        """ Метод для отоюражения окна с контактами. """
        ContactsWindow(self)

    def show_calendar(self):
        """ Метод для отоюражения окна с календарем. """
        CalendarWindow(self)

    def show_statistics(self):
        stats_window = StatisticsWindow(self)
    
    def show_documentation(self):
        documentation_window = DocumentationWindow(self)

    def filter_orders(self):
        search_query = self.search_entry.get().strip()

        if search_query.startswitch("#"):
            search_query = search_query[1:].strip()

        for widget in self.repair_scrollable_frame.winfo_childen():
            widget.destroy()

        all_orders = self.database_repair.get_all_repair_orders()

        if not search_query:
            self.load_repair_data()
            return
        
        filtered_orders = [order for order in all_orders if
            search_query.lower() in order['surname'].lower() or
            search_query.lower() in order['first_name'].lower() or
            search_query.lower() in order['patronymic'].lower() or
            search_query == str(order['id']) or
            search_query in order['phone'] or
            search_query in order['expected_completion_date']
            ]

        if filtered_orders:
            for order in filtered_orders:
                order_frame = ctk.CTkFrame(self.repair_scrollable_frame, border_width=0)
                order_frame.pack(fill="x", padx=10, pady=5)

                order_info = (
                    f"Заявка №{order['id']}\n"
                    f"Фамилия: {order['surname']}\n"
                    f"Имя: {order['first_name']}\n"
                    f"Отчество: {order['patronymic']}\n"
                    f"Комплектующие: {order['components']}\n"
                    f"Описание проблемы: {order['problem_description']}\n"
                    f"Телефон: {order['phone']}\n"
                    f"Email: {order['email']}\n"
                    f"Ожидаемая дата завершения: {order['expected_completion_date']}\n"
                    f"Статус: {order['status']}\n"
                )

                info_label = ctk.CTkLabel(order_frame, text=order_info, anchor='w', justify='left')
                info_label.pack(side='left', fill='x', expand=True)

                button_frame = ctk.CTkFrame(order_frame)
                button_frame.pack(side='right')

                button_color = "#28a745" if order['status'] == 'Выполнено' else "#007bff"
                button_text = "Выполненое" if order['status'] == 'Выполнено' else "Выполнить"
                execute_button = ctk.CTkButton(button_frame, text=button_text, command=lambda o=order: self.execute_order(o),
                                               fg_color=button_color, border_width=0, width=120)
                execute_button.pack(side='top', padx=5, pady=2)

                delete_button = ctk.CTkButton(button_frame, text="Удалить", command=lambda o=order: self.execute_order(o),
                                               fg_color="#dc3545", border_width=0, width=120)
                delete_button.pack(side='top', padx=5, pady=2)

                edit_button = ctk.CTkButton(button_frame, text="Редактировать", command=lambda o=order: self.execute_order(o),
                                               fg_color="#ffc107", border_width=0, width=120)
                edit_button.pack(side='top', padx=5, pady=2)

                generate_button = ctk.CTkButton(button_frame, text="Формировать", command=lambda o=order: self.execute_order(o),
                                               fg_color="#907bff", border_width=0, width=120)
                generate_button.pack(side='top', padx=5, pady=2)
        else:

            no_results_label = ctk.CTkLabel(self.repair_scrollable_frame, text="Нет заявок, соответствующих критериям поиска.", anchor='w', justify='left')
            no_results_label.pack(pady=5,padx=10)
        





