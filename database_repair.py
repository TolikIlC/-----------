import sqlite3

class DatabaseRepair:
    def __init__(self):
        self.conn = sqlite3.connect('tech_repair.db')
        self.cursor = self.conn.cursor()
        self.create_repair_orders_table()

    def create_repair_orders_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS repair_orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                surname TEXT NOT NULL,
                first_name TEXT NOT NULL,
                patronymic TEXT,
                components TEXT,
                problem_description TEXT,
                phone TEXT,
                email TEXT,
                expected_completion_date TEXT,
                status TEXT DEFAULT 'В работе'
            )
        ''')
        self.conn.commit()

    def create_tasks_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                task_date TEXT NOT NULL, 
                status TEXT DEFAAULT 'В работе'       
                )
        ''')
        self.conn.commit()
        
    def add_repair_order(self, surname, first_name, patronymic, components, problem_description, phone, email, expected_completion_date, status='В работе'):
        self.cursor.execute('''
                INSERT INTO repair_orders (surname, first_name, patronymic, components, problem_description, phone, email, expected_completion_date, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (surname, first_name, patronymic, components, problem_description, phone, email, expected_completion_date, status))
        self.conn.commit()

    def add_task(self, task, task_date, status='В работе'):
        self.cursor.execute('''
            INSERT INTO tasks (task, task_date, status)
            VALUES (?, ?, ?)
        ''', (task, task_date, status))
        self.conn.commit()
    
    def get_all_repair_orders(self):
        self.cursor.execute('SELECT * FROM repair_orders')
        rows = self.cursor.fetchall()
        columns = [description[0] for description in self.cursor.description]
        return [dict(zip(columns, row)) for row in rows]
    
    def get_all_tasks(self):
        self.cursor.execute('SELECT * FROM tasks')
        rows = self.cursor.fetchall()
        columns = [description[0] for description in self.cursor.description]
        return [dict(zip(columns, row)) for row in rows]
    
    def delete_repair_order(self, order_id):
        self.cursor.execute('DELETE FROM repair_orders WHERE id=?', (order_id,))
        self.conn.commit()
        self.reset_auto_increment()

    def delete_task(self, task_id):
        self.cursor.execute('DELETE FROM tasks WHERE id=?', (task_id,))
        self.conn.commit()

    def delete_all_repair_orders(self):
        self.cursor.execute('DELETE FROM repair_orders')
        self.conn.commit()
        self.reset_auto_increment()

    def delete_all_tasks(self):
        self.cursor.execute('DELETE FROM tasks')
        self.conn.commit()

    def reset_auto_increment(self):
        self.cursor.execute('DELETE FROM sqlite_sequence WHERE name="repair_orders"')
        self.conn.commit()

    def __del__(self):
        self.conn.close()