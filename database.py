import sqlite3
import csv

from PyQt6.QtWidgets import QFileDialog

def import_links():
    try:
        # Открытие файлового менеджера для выбора файла
        file_name, _ = QFileDialog.getOpenFileName(
            None, "Выберите файл", "", "CSV Files (*.csv)"  # Диалог для выбора файла
        )
        
        if not file_name:  # Если файл не выбран, выходим
            return
        conn = sqlite3.connect('phishing_links.db')
        cursor = conn.cursor()
        
        with open(file_name, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)  # Пропустить заголовок
            for row in reader:
                cursor.execute(
                    'INSERT INTO phishing_links (url, status) VALUES (?, ?)',
                    (row[1], row[2])
                )
        conn.commit()
        conn.close()
        return None
    except Exception as e:
        return e

def export_links():
    try:
        # Открытие файлового менеджера для выбора места сохранения файла
        file_name, _ = QFileDialog.getSaveFileName(
            None, "Сохранить файл", "", "CSV Files (*.csv)"  # Диалог для сохранения файла
        )

        if not file_name:  # Если файл не выбран, выходим
            return

        # Получаем данные из базы данных
        conn = sqlite3.connect('phishing_links.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM phishing_links")
        links = cursor.fetchall()
        conn.close()
        # Записываем данные в выбранный файл
        with open(file_name, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "URL", "Status", "Added On"])
            writer.writerows(links)
        return None
    except Exception as e:
        return e

def init_db():
    conn = sqlite3.connect('phishing_links.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS phishing_links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            status TEXT NOT NULL,
            added_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def add_link(url, status):
    conn = sqlite3.connect('phishing_links.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO phishing_links (url, status) VALUES (?, ?)', (url, status))
    conn.commit()
    conn.close()

def get_links():
    conn = sqlite3.connect('phishing_links.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM phishing_links')
    links = cursor.fetchall()
    conn.close()
    return links

# Initialize the database
if __name__ == "__main__":
    init_db()
