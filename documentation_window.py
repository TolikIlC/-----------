import customtkinter as ctk
from tkinter import filedialog, messagebox
import os

class DocumentationWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Документация")
        self.geometry("900x500")
        self.resizable(False, False)

        self.datasheet_folder = "Datasheet"
        self.subfolders = [ 
            "Процессоры", "Видеокарты", "Материнские платы", 
            "Оперативная память", "Жесткие диски", "Клавиатуры",
            "Мышки", "Блоки питания", "Мониторы", "Корпуса компьютеров"
        ]

        if not os.path.exists(self.datasheet_folder):
            os.makedirs(self.datasheet_folder)

        for folder in self.subfolders:
            os.makedirs(os.path.join(self.datasheet_folder, folder), exist_ok=True)

        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(pady=10)

        for index, folder in enumerate(self.subfolders):
            button = ctk.CTkButton(self.button_frame, text=f"{folder}", command=lambda f=folder: self.load_document(f))
            button.grid(row=index //3, column=index % 3, padx=10, pady=5)

        self.search_frame = ctk.CTkFrame(self)
        self.search_frame.pack(pady=10)

        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Введите название файла для поиска", width=300)
        self.search_entry.pack(side='left', padx=(10, 0), fill='x', expand=True)

        self.search_button = ctk.CTkButton(self.search_frame, text="Поиск", command=self.search_frame)
        self.search_button.pack(side='right', padx=(5,10))

        self.file_list_frame = ctk.CTkScrollableFrame(self, width=300, height=300)
        self.file_list_frame.pack(pady=10, padx=10, fill='both', expand=True)
        
        self.headers_label = ctk.CTkLabel(self.file_list_frame, text="ID    Название файла", anchor='w', font=("Arial", 12, "bold"))
        self.headers_label.pack(row=0, column=0, padx=5, pady=5, sticky='w')

        self.update_file_list()

    def load_document(self, category):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            file_name = os.path.basename(file_name)

            destination_path = os.path.join(self.datasheeet_folder, category, file_name)
            with open(file_path, 'rb') as source_file:
                with open(destination_path, 'wb') as dest_file:
                    dest_file.write(source_file.read())
                
            messagebox.showinfo("Успех", f"Документ '{file_name}' успешнор загрежен в '{category}'!")
            self.update_file_list()
        
    def update_file_list(self):
        for widget in self.file_list_frame.winfo_children():
            widget.destroy()

        all_files = []
        for folder in self.subfolders:
            path = os.path.join(self.datasheet_folder, folder)
            files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

        if all_files:
            for index, (folder, file) in enumerate(all_files, start=1):
                file_label = ctk.CTkLabel(self.file_list_frame, text=f"{index} {file} (Категория: {folder})", anchor='w')
                file_label.grid(row=index, column=0, padx=5, pady=2, sticky='w')

                delete_button = ctk.CTkLabel(self.file_list_frame, text="Удалить", command=lambda f=file, cat=folder: self.delete_file(cat, f))
                delete_button.grid(row=index, column=1, padx=5, pady=2, sticky='w')

                open_button = ctk.CTkLabel(self.file_list_frame, text="Открыть", command=lambda f=file, cat=folder: self.delete_file(cat, f))
                open_button.grid(row=index, column=2, padx=5, pady=2, sticky='w')
            else:
                empty_label = ctk.CTkLabel(self.fule_list_frame, text="Папка пуста", anchor='w')
                empty_label.grid(row=0, column=0, padx=5, pady=2)
            
        def search_files(self):
            search_query = self.search_entry.get().strip().lower()
            for widget in self.file_list_frame.winfo_children():
                widget.destroy()
                
            all_files = []
            for folder in self.subfolders:
                path = os.path.join(self.datasheet_folder, folder)
                files = (f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)))
                all_files.extend([(folder, f) for f in files])
                
            if all_files:
                for index, (folder, file) in enumerate(all_files, start=1):
                    if search_query in file.lower():
                        file_label = ctk.CTkLabel(self.file_list_frame, text=f"{index}  {file} (Категория: {folder})", anchor='w')
                        file_label.grid(row=index, column=0, padx=5, pady=2, sticky='w')

                        delete_button = ctk.CTkLabel(self.file_list_frame, text="Удалить", command=lambda f=file, cat=folder: self.delete_file(cat, f))
                        delete_button.grid(row=index, column=1, padx=5, pady=2, sticky='w')

                        open_button = ctk.CTkLabel(self.file_list_frame, text="Открыть", command=lambda f=file, cat=folder: self.delete_file(cat, f))
                        open_button.grid(row=index, column=2, padx=5, pady=2, sticky='w')
            else:
                empty_label = ctk.CTkLabel(self.fule_list_frame, text="Нет файлов, соответсвующих запросу", anchor='w')
                empty_label.grid(row=0, column=0, padx=5, pady=2)
            
        def delete_file(self, category, file_name):
            file_path = os.path.join(self.datasheet_folder, category, file_name)
            if os.path.exists(file_path):
                os.remove(file_path)
                messagebox.showinfo("Успех", f"Файл '{file_name}' не найден!")
            else:
                messagebox.showerror("Ошибка", f"Файл '{file_name}' не найден!")
            
        def open_file(self, category, file_name):
            file_path = os.path.join(self.datasheet_folder, category, file_name)
            if os.path.exists(file_path):
                os.startfile(file_path)
            else:
                messagebox.showerror("Ошибка", f"Файл '{file_name}' не найден!")