import os
import json
from docx import Document

class ProjectAnalyzer:
    def __init__(self, project_path):
        self.project_path = project_path
        self.analysis_results = {
            'doc_count': 0,
            'word_doc_count': 0,
            'doc_quality': 0,
            'code_quality': 0,
            'test_count': 0,
            'files_with_comments': [],
            'files_without_comments': [],
            'project_structure ': {},
            'coding_standards': 0,
            'recommendations': [],
        }

    def analyze_documentation(self): 
        doc_files = ['README.md', 'README.txt', 'API.md']
        for doc in doc_files:
        
            if os.path.exists(os.path.join(self.project_path, doc)):
                self.analysis_results['doc_count'] += 1
        

        for file in os.listdir(self.project_path):

            if file.endswith('.docx'):
                self.analysis_results['word_doc_count'] += 1
                self.analyze_word_document(os.path.join(self.project_path, file))

    def analyze_word_document(self, file_path):
        doc = Document(file_path)
        total_paragraphs = len(doc.paragraphs)

        if total_paragraphs > 0:
            self.analysis_results['doc_quality'] += total_paragraphs

    def analyze_code_quality(self):
        total_lines = 0
        code_files = [f for f in os.listdir(self.project_path) if f.endswith('.py')]

        for file in code_files:
            with open(os.path.join(self.project_path, file), 'r', encoding='utf-8') as f:
                lines = f.readlines()
                total_lines += len(lines)

                if any(line.strip().startswith('#') for line in lines):
                    self.analysis_results['files_with_comments'].append(file)
                else:
                    self.analysis_results['files_without_comments'].append(file)
        
        if total_lines > 0:
            self.analysis_results['code_quality'] = (len(self.analysis_results['files_with_comments']) / len(code_files)) * 100
     
        self.provide_code_optimization_recommendations(code_files)
     
    def analyze_tests(self):
        """Анализ наличия тестов."""
        # Получаем список файлов тестов, начинающихся с 'test_' и заканчивающихся на '.py'
        test_files = [f for f in os.listdir(self.project_path) if f.startswith('test_') and f.endswith('.py')]
        self.analysis_results['test_count'] = len(test_files)  # Устанавливаем количество тестов

    def analyze_project_structure(self):
        """Анализ структуры проекта."""
        # Обходим структуру папок и файлов
        self.analysis_results['project_structure'] = []  # Initialize as an empty list
        for root, dirs, files in os.walk(self.project_path):
            for dir in dirs:
                # Если папка еще не добавлена в структуру, добавляем её
                self.analysis_results['project_structure'].append(dir)
            # Добавляем файлы в структуру, организуя по папкам
            for file in files:
                self.analysis_results['project_structure'].append(os.path.join(root, file))

    def analyze_coding_standards(self):
        """Проверка стандартов кодирования."""
        # Получаем список файлов Python
        code_files = [f for f in os.listdir(self.project_path) if f.endswith('.py')]
        standard_violations = 0  # Инициализируем счетчик нарушений стандартов

        for file in code_files:
            # Открываем файл Python
            with open(os.path.join(self.project_path, file), 'r', encoding='utf-8') as f:
                lines = f.readlines()  # Читаем все строки файла
                for line in lines:
                    # Проверяем на длину строки (например, более 79 символов)
                    if len(line) > 79:
                        standard_violations += 1  # Увеличиваем счетчик нарушений

        self.analysis_results['coding_standards'] = standard_violations  # Записываем количество нарушений

    def provide_code_optimization_recommendations(self, code_files):
        """Предоставление рекомендаций по оптимизации кода."""
        for file in code_files:
            # Открываем файл Python
            with open(os.path.join(self.project_path, file), 'r', encoding='utf-8') as f:
                lines = f.readlines()  # Читаем все строки файла
                long_functions = []  # Список длинных функций
                global_var_usage = []  # Список использований глобальных переменных
            
                for line in lines:
                    # Найдем длинные функции
                    if line.strip().startswith('def'):
                        function_count = 1  # Увеличиваем счетчик функций
                    if len(line.strip()) > 80:  # Проверяем длину функции
                        long_functions.append(line.strip())  # Добавляем длинную функцию в список
            
                # Проверка на использование глобальных переменных
                if 'global' in line:
                    global_var_usage.append(line.strip())  # Добавляем использование глобальной переменной в список
            
                # Рекомендации по длинным функциям
                if long_functions:
                    self.analysis_results['recommendations'].append(
                        f"В файле {file} есть длинные функции: {', '.join(long_functions)}. Рассмотрите возможность их упрощения."
                    )

                # Рекомендации по использованию глобальных переменных
                if global_var_usage:
                    self.analysis_results['recommendations'].append(
                        f"В файле {file} используются глобальные переменные: {', '.join(global_var_usage)}. Избегайте их использования, если возможно."
                    )
    
    def generate_report(self):
        """Генерация отчета."""
        report = {
            "Документация (текстовые файлы)": self.analysis_results['doc_count'],
            "Документация (Word)": self.analysis_results['word_doc_count'],
            "Качество документации (количество абзацев)": self.analysis_results['doc_quality'],
            "Качество кода (в %)": self.analysis_results['code_quality'],
            "Количество тестов": self.analysis_results['test_count'],
            "Файлы с комментариями": self.analysis_results.get('files_with_comments', "N/A"),
            "Файлы без комментариев": self.analysis_results.get('files_without_comments', "N/A"),
            "Структура проекта": self.analysis_results['project_structure'],
            "Нарушения стандартов кодирования": self.analysis_results['coding_standards'],
            "Рекомендации по оптимизации кода": self.analysis_results.get('recommendations', "N/A")
        }
        return json.dumps(report, ensure_ascii=False, indent=4)  # Возвращаем отчет в формате JSON


def main():
    project_path = input("Введите путь к проекту: ")  # Запрашиваем путь к проекту у пользователя
    analyzer = ProjectAnalyzer(project_path)  # Создаём экземпляр анализатора проекта

    analyzer.analyze_documentation()  # Анализируем документацию
    analyzer.analyze_code_quality()  # Анализируем качество кода
    analyzer.analyze_tests()  # Анализируем наличие тестов
    analyzer.analyze_project_structure()  # Анализируем структуру проекта
    analyzer.analyze_coding_standards()  # Проверяем стандарты кодирования

    report = analyzer.generate_report()  # Генерируем отчет
    print("Отчет по проекту:")  # Выводим заголовок отчета
    print(report)  # Выводим отчет


if __name__ == "__main__":
    main()  # Запускаем главную функцию