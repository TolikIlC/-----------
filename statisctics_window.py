import customtkinter as ctk
from database_repair import DatabaseRepair
from datetime import datetime

class StatisticsWindow(ctk.CTkToplevel):
    def __init__(self,parent):
        super().__init__(parent)
        self.title("Статистика")
        self.geometry("900x600")
        self.resizable(False, False)

        self.attributes('-topmost', True)

        self.database = DatabaseRepair()

        self.title_label = ctk.CTkLabel(self, text="Статистика по заявкам", font=("Arial", 18, "bold"))
        self.title_label.pack(pady=10)

        self.table_frame = ctk.CTkScrollableFrame(self, width=860, height=300)
        self.table_frame.pack(padx=10, pady=10, fill='both', expand=True)

        headers = ["ID", "Фамилия", "Имя", "Отчество", "Телефон", "Email", "Статус", "Дата создания", "Дата выполнения",  "Время выполнения"]
        for idx, header in enumerate(headers):
            label = ctk.CTkLabel(self.table_frame, text=header, font=("Arial", 12, "bold"), anchor='w')
            label.grid(row=0, column=idx, padx=5, pady=5, sticky='ew')
        
        self.load_data()

        self.component_count_frame = ctk.CTkScrollableFrame(self, width=860, height=200)
        self.component_count_frame.pack(padx=10, pady=10, fill='both', expand=True)

        component_headers = ["Комплектующие", "Количество выполненных заявок"]
        for idx, header in enumerate(component_headers):
            label = ctk.CTkLabel(self.component_count_frame, text=header, fonts=("Arial", 12, "bold"), anchor='w')
            label.grid(row=0, column=idx, padx=5, pady=5, sticky='ew')

        self.load_component_counts()

        self.close_button = ctk.CTkButton(self, text="Закрыть", command=self.destroy)
        self.close_button.pack(pady=10)

    def load_data(self):
        repair_orders = self.database.get_all_repair_orders()

        for i, order in enumerate(repair_orders, start=1):
            text_color = "green" if order ['status'] == 'Выполнено' else "black"

            ctk.CTkLabel(self.table_frame, text=str(order['id']), anchor='w', text_color=text_color).grid(row=i, column=0, padx=5, pday=2)
            ctk.CTkLabel(self.table_frame, text=order['surname'], anchor='w', text_color=text_color).grid(row=i, column=1, padx=5, pday=2)
            ctk.CTkLabel(self.table_frame, text=order['first_name'], anchor='w', text_color=text_color).grid(row=i, column=2, padx=5, pday=2)
            ctk.CTkLabel(self.table_frame, text=order['patronymic'], anchor='w', text_color=text_color).grid(row=i, column=3, padx=5, pday=2)
            ctk.CTkLabel(self.table_frame, text=order['phone'], anchor='w', text_color=text_color).grid(row=i, column=4, padx=5, pday=2)
            ctk.CTkLabel(self.table_frame, text=order['email'], anchor='w', text_color=text_color).grid(row=i, column=5, padx=5, pday=2)
            ctk.CTkLabel(self.table_frame, text=order['status'], anchor='w', text_color=text_color).grid(row=i, column=6, padx=5, pday=2)

            created_date = datetime.strftime(order['created_date'], '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%Y') if order ['created_date'] else "Не указано"
            completed_date = datetime.strftime(order['completed_date'], '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%Y') if order ['completed_date'] else "Не завершено"

            ctk.CTkLabel(self.table_frame, text=created_date, anchor='w', text_color=text_color).grid(row=i, column=7, padx=5, pady=2)
            ctk.CTkLabel(self.table_frame, text=completed_date, anchor='w', text_color=text_color).grid(row=i, column=8, padx=5, pady=2)

            if order ['completed_date']:
                time_spent = datetime.strftime(order['completed_date'], '%Y-%m-%d %H:%M:%S') - datetime.strftime(order['created_date'], '%Y-%m-%d %H:%M:%S')
                time_spent_days =  time_spent.days
                time_spent_hours, remainder = divmod(time_spent_seconds, 3600)
                time_spent_minutes, time_spent_seconds = divmod (remainder, 60)
                time_spent_str = f"{time_spent_days} дн {time_spent_hours} ч {time_spent_minutes} мин"
            else:
                time_spent_str = "Не завершено"

            ctk.CTkLabel(self.table_frame, text=time_spent_str, anchor='w', text_color=text_color).grid(row=i, column=9, padx=5, pady=2)

        def load_components_counts(self):
            completed_orders = [order for order in self.database.get_all_repair_orders() if order['status'] == 'Выполнено']

            component_counts = {}
            for order in completed_orders:
                components = order['components'].split(', ')
                for component in components:
                    if component in component_counts:
                        component_counts[component] += 1
                    else:
                        component_counts[component] = 1
            
            for i, (component, count) in enumerate(component_counts.items(), start=1):
                ctk.CTkLabel(self.component_counts_frame, text=component, anchor='w').grid(row=i, column=0, padx=5, pady=2)
                ctk.CTkLabel(self.component_counts_frame, text=str(count), anchor='w').grid(row=i, column=1, padx=5, pady=2)