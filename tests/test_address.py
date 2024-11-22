import pytest
from address_endpoint import AddressEndpoint
from address_helper import generate_address_part, save_valid_addresses, process_addresses

class TestAddressEndpoint:
    @pytest.mark.parametrize("part, expected_count", [ # перебираю разные части адресов, и проверяю на количество адресов в зависимости от входного адреса
        ("region", 30),
        ("city", 20),
        ("street_address", 10),
        ("postcode", 5),
    ])
    def test_positive_scenarios(self, part, expected_count): # функция для проверки позитивного сценария
        value = generate_address_part(part) # получаю случайное значение части адреса
        status_code, addresses = AddressEndpoint.post(part, value) # отправляю значение части адреса в запросе пост

        assert status_code == 200 # проверка на статус код 200
        assert len(addresses) == expected_count # проверка, что количество адресов в списке равно заданному значению
        for address in addresses: # проверяю что все полученные адреса содержат переданное значение
            assert value in address

        save_valid_addresses(addresses) # сохраняю валидные адреса в файл

    @pytest.mark.parametrize("part, invalid_value", [ # функция для проверки негативного сценария - передаем кривые данные
        ("region", "НекорректныйРегион"),
        ("city", "НекорректныйГород"),
        ("street_address", "НекорректнаяУлица"),
        ("postcode", "12345"),
        ("postcode", "000000"),
    ])
    def test_negative_scenarios(self, part, invalid_value):
        status_code, addresses = AddressEndpoint.post(part, invalid_value)

        assert status_code == 404 # проверка на ошибку 404 при передаче кривых данных
        assert len(addresses) == 0 # проверяем что список не заполнился кривыми данными

    def test_process_addresses(self):
        """Тест обработки адресов из файла и сохранения в таблицу."""
        process_addresses("valid_addresses.txt", "sorted_addresses.csv")
