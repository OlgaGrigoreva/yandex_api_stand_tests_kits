import configuration # данные из конфигурации
import requests      # данные ответов
import data          # данные тела из даты


# создать нового пользователя
def post_new_user(body):
    return requests.post(configuration.URL_SERVICE + configuration.CREATE_USER_PATH,  # полный url
                         json=body,  # тут тело
                         headers=data.headers)  # здесь заголовки

response = post_new_user(data.user_body);
print(response.status_code)
print(response.json())


def post_new_client_kit(kit_body):
    # копирование заголовка из файла data, чтобы не потерять данные в исходном словаре
    headers_dict = data.headers.copy()
    # передаем параметр authToken
    headers_dict["Authorization"] = "Bearer " + "authToken";
    # возвращаем ответ созданного набора под авторизованным пользователем
    return requests.post(configuration.URL_SERVICE + configuration.CREATE_USER_KIT_PATH,  # подставялем полный url
                         json=kit_body, # тут тело
                         headers=headers_dict)  # здесь заголовки
response = post_new_client_kit(data.kit_body)
#вывести на экран результат - созданный набор под авторизованным пользователем
print(response.status_code)
print(response.json())

