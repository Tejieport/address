from faker import Faker

faker = Faker("ru_RU")

class AddressEndpoint:
    @staticmethod
    def post(address_part, value, base_url="http://address.ru/"):
        """
        Метод для обработки запросов к базе данных.
        :param address_part: Часть адреса (region, city, street_address, postcode)
        :param value: Значение части адреса
        :param base_url: URL базы данных (по умолчанию фиктивный адрес http://address.ru/)
        :return: Статус-код и список предложений адресов
        """
        # прописываю валидные значения частей адресов
        valid_regions = ["респ.", "АО", "обл.", "край"]
        valid_cities = ["п.", "с.", "клх", "д.", "к.", "ст.", "г."]
        valid_streets = ["пер.", "ш.", "пр.", "алл.", "наб.", "ул.", "бул."]

        # Проверка на валидность значения
        if address_part == "region" and not any(region in value for region in valid_regions):
            return 404, []
        elif address_part == "city" and not any(city in value for city in valid_cities):
            return 404, []
        elif address_part == "street_address" and not any(street in value for street in valid_streets):
            return 404, []
        elif address_part == "postcode" and (len(value) != 6 or value == "000000" or not value.isdigit()):
            return 404, []

        # Генерация списка адресов
        count = {"region": 30, "city": 20, "street_address": 10, "postcode": 5}.get(address_part, 0) # считаю сколько будет адресов выводиться в зависимости от типа адреса в запросе
        suggestions = [ # создаю список через перебор значений адресов
            f"{faker.region()}, {faker.city()}, {faker.street_address()}, {value}" # для индекса здесь указан не фейковый, а тот что передается в запросе, так как данные криво отображаются у индекса
            for _ in range(count)
        ]

        # Проверка для "postcode" - дополнительная, так как индексы формируются иногда криво не в тех местах
        if address_part == "postcode":
            for address in suggestions:
                postcode_from_address = address.split(",")[-1].strip() # Почтовый индекс извлекается из последней части строки
                if value != postcode_from_address:
                    return 404, []

        return 200, suggestions # возврат статус кода и списка адресов
