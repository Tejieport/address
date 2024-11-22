from faker import Faker
import csv
import os
import chardet

faker = Faker("ru_RU")

def generate_random_address(): # создал функцию для генерации полного адреса
    return {
        "region": faker.region(),
        "city": faker.city(),
        "street_address": faker.street_address(),
        "postcode": faker.postcode(),
    }

def generate_address_part(part): # создал функцию для генерации части адреса
    if part == "region":
        return faker.region()
    elif part == "city":
        return faker.city()
    elif part == "street_address":
        return faker.street_address()
    elif part == "postcode":
        return faker.postcode()
    else:
        raise ValueError(f"Unknown address part: {part}")

def save_valid_addresses(addresses, file_path="valid_addresses.txt"):  # Функция для сохранения валидных адресов в файл
    if not addresses: # если адрес пустой или ложный список, то функция не выполняется
        return

    with open(file_path, "a", encoding="utf-8") as file: # открытие и запись строк в файл через перебор
        file.writelines(f"{address}\n" for address in addresses)

    try: # Определение кодировки файла
        with open(file_path, "rb") as file: # открытие файла в бинарном режиме - rb
            raw_data = file.read() # чтение файла в память как бинарные данные
            result = chardet.detect(raw_data) # при помощи библиотеки chardet определяем кодировку файла
            encoding = result['encoding'] # возвращаем предполагаемую кодировку

            if encoding.lower() != 'utf-8': # проверяем - совпадает ли кодировка с utf-8, если нет то:
                with open(file_path, "r", encoding=encoding) as source_file: # открываем файл в режиме чтения в возвращенной кодировке
                    content = source_file.read() # Читаем весь файл в переменную content

                with open(file_path, "w", encoding="utf-8") as target_file: # Перезаписываем файл в кодировке UTF-8:
                    target_file.write(content)

    except Exception as e:
        print(f"Error during file encoding detection: {e}")

def process_addresses(file_path="valid_addresses.txt", output_file="sorted_addresses.csv", upload_url="http://homebase.ru/sorted_addresses.csv"):
    """
    Данная функция формирует таблицу с адресами, сортирует их и сохраняет в формате CSV.
    :param file_path: Путь к исходному файлу с валидными адресами.
    :param output_file: Путь для сохранения таблицы.
    """
    import re # модуль для работы с регулярными выражениями - для проверки корректности почтового индекса

    if not os.path.exists(file_path): # проверка, существует ли файл по указанному пути
        print(f"Файл {file_path} не найден.")
        return # если файл не существует, функция завершает выполнение

    # Читаем адреса из файла
    with open(file_path, "r", encoding="utf-8") as file:
        addresses = file.readlines() # читаем все строки из файла и сохраняем их в список

    if not addresses: # повторная проверка на пустой адрес
        print("Файл valid_addresses.txt пуст.")
        return

    # Разбиваем адреса и фильтруем корректные строки
    parsed_addresses = [] # в данную переменную будет сохраняться список корректных адресов
    for address in addresses:
        # Удаляем лишние пробелы и проверяем общий формат
        address = address.strip() # удаляем все начальные и конечные пробелы из строки.
        parts = [part.strip() for part in address.split(",")] # разделяем строку на части по запятой и удаляем лишние пробелы из каждой части

        # Проверяем наличие минимум 4 частей в адресе (region, city, street_address, postcode)
        if len(parts) < 4:
            print(f"Пропускаю адрес из-за недостаточного количества частей: {address}")
            continue

        # Извлекаем ключевые части: region, city, street_address, postcode
        region = parts[0]
        city = parts[1]
        street_address = ", ".join(parts[2:-1])  # Собираем улицу и номер дома, все части между городом и почтовым индексом (собираются в строку через запятую)
        postcode = parts[-1]

        # Проверяем, что почтовый индекс состоит из 6 цифр
        if not re.match(r"^\d{6}$", postcode): # ^\d{6}$ означает: начало строки ^, затем ровно 6 цифр \d{6}, и конец строки $.
            print(f"Пропускаю адрес из-за некорректного почтового индекса: {address}")
            continue

        parsed_addresses.append({ # при прохождении всех проверок адрес сохраняется в список
            "region": region,
            "city": city,
            "street_address": street_address,
            "postcode": postcode,
        })

    if not parsed_addresses: # проверка на отсутствие корректных адресов
        print("Нет корректных адресов для обработки.")
        return

    # Сортировка адресов
    parsed_addresses.sort( # Адреса сортируются с помощью метода sort()
        key=lambda x: (x["region"], x["city"], x["street_address"], x["postcode"])
    )

    # Сохраняем в CSV
    with open(output_file, "w", encoding="utf-8", newline="") as csv_file: # Открываем файл для записи в формате CSV, newline="" — предотвращает добавление лишних пустых строк
        writer = csv.DictWriter(csv_file, fieldnames=["region", "city", "street_address", "postcode"]) # Используется csv.DictWriter, который позволяет записывать список словарей в CSV файл
        writer.writeheader() # записывает заголовки столбцов в CSV файл
        writer.writerows(parsed_addresses) # аписывает все адреса из списка

    # Вывод сообщения с указанием, где якобы доступен файл
    print(f"Сортированные адреса сохранены в {output_file}.")
    print(f"Файл доступен для загрузки по адресу: {upload_url}")
