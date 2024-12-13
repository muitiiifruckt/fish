from database import init_db, add_link, get_links, export_links, import_links
from checker import check_url_ssl, check_url_whois
from reports import generate_report_csv
from pprint import pprint
from google_save_browsing_api import check_url_safety as google_api


def main():
    print("Добро пожаловать в систему предотвращения фишинговых атак!")
    while True:
        print("\nМеню:")
        print("1. Проверить URL")
        print("2. Показать базу данных")
        print("3. Сформировать отчет")
        print("4. Экспорт базы данных")
        print("5. Импорт базы данных")
        print("6. Выход")

        choice = input("Выберите опцию: ")
        print()
        try:
            if choice == '1':
                try:
                    url = input("Введите URL для проверки: ")
                    is_ssl = check_url_ssl(url)
                    whois_info = check_url_whois(url)
                    status = "Безопасен" if is_ssl else "Подозрительный"
                    google_response = google_api(url)
                    print(f"Результат сканирования с помощью GOOGLE Save Browsing:{google_response}")
                    print(f"Результат: {status}")
                    print(f"WHOIS информация:")
                    pprint(whois_info)
                    add_link(url, status)
                except :
                    print(f"Неправильный ввод ")
            elif choice == '2':
                links = get_links()
                for link in links:
                    print(link)
            elif choice == '3':
                generate_report_csv()
            elif choice == '4':
                file_name = input("Введите имя файла для экспорта (по умолчанию: database.csv): ") or "database.csv"
                export_links(file_name)
            elif choice == '5':
                file_name = input("Введите имя файла для импорта: ")
                import_links(file_name)
            elif choice == '6':
                print("Выход из программы. До свидания!")
                break
            else:
                print("Неверный выбор, попробуйте снова.")
        except :
            print(f"Ошибка, попробуйте еще")

if __name__ == "__main__":
    init_db()
    main()
