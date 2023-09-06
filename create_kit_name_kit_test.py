import sender_stand_request   # данные из файла с заготовками
import data                   # данные тела


#получить данные о созданном пользователе и параметре authToken
def get_new_user_token():
    # Создать нового пользователя
    user_body = data.user_body
    # получить ответ по созданному пользователю
    response_user = sender_stand_request.post_new_user(user_body)
    # Запомнить токен авторизации
    return response_user.json()["authToken"]


# функция меняет значение в параметре name из тела kit_body вкладка data
def get_kit_body(name):
    # копирование словаря с телом запроса из файла data, чтобы не потерять данные в исходном словаре
    current_body = data.kit_body.copy()
    # изменение значения в name
    current_body["name"] = name
    # возвращается новый словарь с нужным значением name
    return current_body


# Функция для позитивной проверки по вводимым символам
# Проверка успешного создания набора с измененным именем под авторизованным пользователем code = 201
def positive_assert(name):
    # в переменную kit_body сохраняется обновленное тело запроса
    kit_body = get_kit_body(name)
    # в переменную kit_response сохраняется результат запроса на создание набора под авторизованным пользователем
    kit_response = sender_stand_request.post_new_client_kit(kit_body) #get_new_user_token())
    # Проверить код ответа
    assert kit_response.status_code == 201
    # Проверить, что имя в ответе совпадает с именем в запросе
    assert kit_response.json()["name"] == kit_body["name"]


# Функция для негативной проверки по вводимым символам
# Ошибка. Набор не создан под авторизованным пользователем code = 400 при введеных/не введенных символах
def negative_assert(kit_body):
    # в переменную kit_response сохраняется результат запроса на создание набора под авторизованным пользователем
    kit_response = sender_stand_request.post_new_client_kit(kit_body) #get_new_user_token())
    # Проверить код ответа
    assert kit_response.status_code == 400
    # Проверка, что в теле ответа атрибут "code" равен 400
    assert kit_response.json()["code"] == 400

def negative_assert_code_400(kit_body):
    resp = sender_stand_request.post_new_client_kit(kit_body, get_new_user_token())
    assert resp.status_code == 400

# Тест 1. Допустимое количество символов (1)
# Параметр name состоит из 1 символа (а)
def test_create_client_kit_name_1_letter_get_success_response():
    positive_assert("а")

# Тест 2. Допустимое количество символов (511)
# Параметр name состоит из 511 символов (511 символов латиницы/кирилицы)
def test_create_client_kit_name_511_letter_get_success_response():
    positive_assert("AbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabC")

# Тест 3. Ошибка. Количество символов меньше допустимого (0)
# Параметр name состоит из 0 символов (пустая строка)
def test_create_client_kit_name_empty_get_error_response():
    kit_body = get_kit_body("")
    negative_assert(kit_body)

# Тест 4. Ошибка. Количество символов больше допустимого (512)
# Параметр name состоит из 512 символов (512 символов латиницы/кирилицы)
def test_create_client_kit_name_512_letter_get_error_response():
    kit_body = get_kit_body("AbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcD")
    negative_assert(kit_body)

# Тест 5. Разрешены английские буквы
# Параметр name состоит из английский букв (QWErty)
def test_create_client_kit_name_english_letter_get_success_response():
    positive_assert("QWErty")

# Тест 6. Разрешены русские буквы
# Параметр name состоит из русских букв (Мария)
def test_create_client_kit_name_russian_letter_get_success_response():
    positive_assert("Мария")

# Тест 7. Разрешены спецсимволы
# Параметр name состоит из спецсимволов ("№%@,)
def test_create_client_kit_name_special_simbol_get_success_response():
    positive_assert("\"№%@\",")

# Тест 8. Разрешены пробелы
# Параметр name состоит из пробелов (Человек и Ко)
def test_create_client_kit_name_has_space_get_success_response():
    positive_assert("Человек и Ко")

# Тест 9. Разрешены цифры
# Параметр name состоит из цифр (123)
def test_create_client_kit_name_has_numbers_get_success_response():
    positive_assert("123")

# Тест 10. Ошибка. Параметр не передан в запросе
# В запросе параметр name - не передан
def test_create_client_kit_no_name_get_error_response():
    # Копируется словарь с телом запроса из файла data в переменную user_body
    kit_body = data.kit_body.copy()
    # Удаление параметра name из запроса
    kit_body.pop("name")
    # Проверка полученного ответа
    negative_assert(kit_body)

# Тест 11. Ошибка. Передан другой тип параметра
# В запросе параметр name - передан числом
def test_create_client_kit_name_number_type_get_error_response():
    kit_body = get_kit_body(123)
    negative_assert(kit_body)