import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from design import Ui_MainWindow  # Импортируем ваш UI
from database import init_db, add_link, get_links, export_links, import_links
from checker import check_url_ssl, check_url_whois
from reports import generate_report_csv
from pprint import pprint
from google_save_browsing_api import check_url_safety as google_api

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Подключаем кнопки к обработчикам
        self.ui.pushButton.clicked.connect(self.check_url)
        self.ui.pushButton_2.clicked.connect(self.show_database)
        self.ui.pushButton_3.clicked.connect(self.import_database)
        self.ui.pushButton_4.clicked.connect(self.export_database)
        self.ui.pushButton_5.clicked.connect(self.generate_report)


    def check_url(self):
        try:
            # Обработчик кнопки "Проверить URL"
            url = self.ui.textEdit.toPlainText()
            is_ssl = check_url_ssl(url)
            whois_info = check_url_whois(url)
            status = "Безопасен" if is_ssl else "Подозрительный"
            google_response = google_api(url)

            # Цветной вывод для Google Safe Browsing
            google_color = "green" if "безопасно" in google_response.lower() else "red"
            self.ui.outputEdit.append(f'<font color="{google_color}">Результат сканирования с помощью GOOGLE Safe Browsing: {google_response} </font>\n')

            # Цветной вывод для проверки SSL
            ssl_color = "green" if is_ssl else "red"
            self.ui.outputEdit.append(f'<font color="{ssl_color}">Результат по проверке SSL: {status} </font>\n')

            # WHOIS информация, можно сделать ее тоже цветной
            self.ui.outputEdit.append('<font color="blue">WHOIS информация:</font>')
            self.ui.outputEdit.append(str(whois_info))
        except:
            self.ui.outputEdit.append("Неправильный ввод")

    def show_database(self):
        links = get_links()

        for link in links:
            self.ui.outputEdit.append(' '.join(map(str, link)))

    def import_database(self):
        if import_links() is None:
            self.ui.outputEdit.append("Импорт произошел")
        else:
            self.ui.outputEdit.append("Импорт не произошел")

    def export_database(self):
        if export_links() is None:
            self.ui.outputEdit.append("Экспорт произошел")
        else:
            self.ui.outputEdit.append("Экспорт не произошел")

    def generate_report(self):
        if generate_report_csv() is None:
            self.ui.outputEdit.append("Формирование отчета произошел")
        else:
            self.ui.outputEdit.append("Формирование отчета не произошел")

    
def main():
    app = QApplication(sys.argv)  # Создаем приложение
    window = MainApp()
    window.show()
    sys.exit(app.exec())  # Завершаем приложение, после его закрытия

if __name__ == "__main__":
    init_db()  # Инициализация базы данных
    main()  # Запуск приложения
