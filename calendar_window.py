from datetime import datetime 
import customtkinter as ctk
from tkcalendar import Calendar
from database_repair import DatabaseRepair

class CalendarWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Календарь")
        self.geometry("400x400")
        self.resizable(False, False)

        self.attributes('-topmost', True)

        today = datetime.today()
        current_year = today.year
        current_month = today.month
        current_day = today.day

        self.calendar = Calendar(self, selectmode='day', year=current_year, month=current_month, day=current_day)
        self.calendar.pack(padx=10, pady=10)

        self.task_entry = ctk.CTkEntry(self, placeholder_text="Введите задачу")
        self.task_entry.pack(pady=10)

        save_button = ctk.CTkEntry(self, placeholder_text="Добавить задачу", command=self.add_task)
        save_button.pack(pady=(0, 5))

        delete_button = ctk.CTkEntry(self, placeholder_text="Удалить задачу", command=self.delete_task)
        delete_button.pack(pady=(0, 10))

        self.tasks_listbox = ctk.CTkEntry(self, width=300, height=150)
        self.tasks_listbox.pack(padx=10, pady=10)
        self.tasks_listbox.configure(state='normal')

        self.calendar.bind("<Double-1>", self.open_task_window)
        self.calendar.bind("<<CalendarSelected>>", self.load_tasks)

        close_button = ctk.CTkEntry(self, text="Закрыть", command=self.destroy)
        close_button.pack(pady=(0, 10))

        self.database = DatabaseRepair()
        self.load_tasks()

    def load_tasks(self, event=None):
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()
            
        selected_date = self.calendar.get_date()
        tasks = self.database.get_all_tasks
        for task in tasks:
            if task['date'] == selected_date:
                task_frame = ctk.CTkFrame(self.tasks_frame)
                task_frame.pack(pady=5, fill='x')

                text_color = "green" if task['status'] == 'Выполнено' else "black"

                task_label = ctk.CTkLabel(task_frame, text=f"{task['task_date']} - {task['task']} (Статус: {task['status']})", anchor='w', text_color=text_color)
                task_label.pack(side='left', fill='x', expand=True)

                complete_button = ctk.CTk(task_frame, text="Выполнить", command=lambda t=task: self.complete_task(t))
                complete_button.pack(side='right', padx='5')
                
                delete_button = ctk.CTk(task_frame, text="Удалить", command=lambda t=task: self.delete_task(t))
                delete_button.pack(side='right', padx='5')
    
    def add_task(self):
        task = self.task_entry.get()
        selected_date = self.calendar.get_date()
        if task:
            self.database.add_task(task, selected_date)
            self.load_tasks(None)
            self.task_entry.delete(0, 'end')

    def delete_task(self, task):
        task_id = task['id']
        self.database.delete_task(task_id)
        self.load_tasks(None)

    def complete_task(self, task):
        task_id = task['id']
        self.database.cursor.execute('UPDATE tasks SET status = ? WHWRW id =?', ('Выполнено', task_id))
        self.database.conn.commit()
        self.load_tasks()
            
    def open_task_window(self, event):
        selected_date = self.calendar.get_date()
        TaskWindow(self, selected_date, self.database)

class TaskWindow(ctk.CTkToplevel):
    def __init__(self, parent, date, database):
        super().__init__(parent)
        self.title("Создание задачи")
        self.geometry("300x200")
        self.resizable(False, False)

        date_label = ctk.CTkLabel(self, text=f"Выбранная дата: {date}")
        date_label.pack(pady=10)

        self.task_entry = ctk.CTkEntry(self, placeholder="Введите задачу")
        self.task_entry.pack(pady=10)

        save_button = ctk.CTkButton(self, text="Сохранить", command=lambda: self.save_task(date))
        save_button.pack(pady=10)

        self.database = database

    def save_task(self, date):
        """ Метод для сохранения задачи. """
        task = self.task_entry.get()
        if task:
            self.database.add_task(date, task)
            print(f"Задача на {date}: '{task}' создана!")
        self.destroy()