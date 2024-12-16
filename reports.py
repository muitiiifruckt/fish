import csv
from database import get_links
from PyQt6.QtWidgets import  QFileDialog

def generate_report_csv():
    links = get_links()
    if not links:
        print("Нет данных для создания отчета.")
        return


    file_name, _ = QFileDialog.getSaveFileName(
        None, "Сохранить отчет", "", "CSV Files (*.csv)"  # Диалог для сохранения файла
    )

    if not file_name:  # Если файл не выбран, выходим
        print("Файл не выбран.")
        return

    try:
        # Записываем данные в выбранный файл
        with open(file_name, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "URL", "Status", "Added On"])
            writer.writerows(links)
        return None
    except Exception as e:
        return e