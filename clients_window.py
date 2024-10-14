import customtkinter as ctk
import json
import os
from tkinter import messagebox

class ClientsWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Клиенты")
        self.geometry("600x400")

        self.users_file_path = os.path.join("Users", "users.json")

        self.clients_frame = ctk.CTkFrame(self)
        self.clients_frame.pack(pady=10, fill='both', expand=True)

        self.scrollable_frame = ctk.CTkScrollableFrame(self.clients_frame)
        self.scrollable_frame.pack(pady=10, fill='both', expand=True)

        self.clients_checkboxes = {}

        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(pady=10)

        self.add_button = ctk.CTkButton(self.button_frame, text="Добавить клиента", command=self.open_add_client_dialog)
        self.add_button.pack(side='left', padx=5)

        self.delete_button = ctk.CTkButton(self.button_frame, text="Удалить клиента", command=self.delete_client)

        self.load_clients()

    def load_clients(self):
        try:
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()

            with open(self.users_file_path, 'r', encoding='utf-8') as file:
                users = json.load(file)
                for user in users:
                    var = ctk.BooleanVar(value=False)
                    checkbox = ctk.CTkCheckBox(self.scrollable_frame, text=f"{user['name']} - {user['email']}", variable=var)
                    checkbox.pack(anchor='w', padx=10, pady=5)
                    self.clients_checkboxes[user['email']] = var
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при загрузке клиентов: {e}")
    
    def open_add_client_dialog(self):
        dialog = AddClientDialog(self)
        self.wait_window(dialog)

    def add_client(self, name, email):
        self.save_client(name, email)

    def delete_client(self):
        selected_emails = [email for email, var in self.clients_checkboxes.items() if var.get() == True]
        if selected_emails:
            try:
                with open(self.users_file_path, 'r', encoding='utf-8') as file:
                    users = json.load(file)
                
                users = [user for user in users if user['email'] not in selected_emails]

                with open(self.users_file_path, 'w', encoding='utf-8') as file:
                    json.dump(users, file, indent=4, ensure_ascii=False)

                self.load_clients()
                messagebox.showinfo("Успех", "Клиенты успешно обнавлены!")
            except Exception as e:
                messagebox.showerror("Ошибка", "Ошибка при удалении клиента: {e}")
        
        else:
            messagebox.showwarning("Предупреждение", "Выбирите хотя бы одного клиента для удаления.")

    def save_clients(self, name, email):
        try:
            with open(self.users_file_path, 'r', encoding='utf-8') as file:
                users = json.load(file)
            
            users.append({"name": name, "email": email})

            with open(self.users_file_path, 'w', encoding='utf-8') as file:
                json.dump(users, file, indent=4, ensure_ascii=False)

            self.load_clients()
            messagebox.showinfo("Успех", "Клиент успешно добавлен!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при сохранении клиента: {e}")

class AddClientDialog(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Добавить клиента")
        self.geometry("300x200")

        self.name_label = ctk.CTkLabel(self, text="Имя:")
        self.name_label.pack(pady=5)

        self.name_entry = ctk.CTkEntry(self)
        self.name_entry.pack(pady=5)

        self.email_label = ctk.CTkLabel(self, text="Email:")
        self.email_label.pack(pady=5)

        self.email_entry = ctk.CTkEntry(self)
        self.email_entry.pack(pady=5)

        self.add_button = ctk.CTkButton(self, text="Добавить", command=self.add_client)
        self.add_button.pack(pady=10)

        self.cancel_button = ctk.CTkButton(self, text="Отмена", command=self.destroy)
        self.cancel_button.pack(pady=5)

    def add_client(self):
        name = self.name_entry.get()
        email = self.email_entry.get()

        if name and email: 
            self.master.add_client(name, email)
            self.destroy()
        else:
            messagebox.showwarning("Предупреждение", "Пожалуйста, заполните все поля") # посхалка не многие поймут 
