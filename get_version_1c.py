import requests
from bs4 import BeautifulSoup
from data import *


# Создаем сессию с контекстным менеджером
def get_version_1c():
    result_dict = dict()
    with requests.Session() as session:
        # Отправляем GET-запрос к сайту releases.1c.ru
        response = session.get(releases_url)

        if response.status_code == requests.codes.ok:
            soup = BeautifulSoup(response.text, "html.parser")

            form = soup.find("form", id="loginForm")
            action = form["action"]

            execution = form.find("input", attrs={"name": "execution"})["value"]

            data = {
                "username": username_1c,
                "password": password_1c,
                "execution": execution,
                "_eventId": "submit",
                "geolocation": ""
            }
            request = login_1c_url + action
            response = session.post(request, data=data)

            if response.status_code == requests.codes.ok:
                if session.cookies:
                    print("Успешная авторизация на сайте 1С")
                    # Ищем строку по тексту в ячейке
                    soup = BeautifulSoup(response.content, "html.parser")
                    rows = soup.find_all("td", class_="nameColumn")

                    for row in rows:
                        for key, value in conf_dict.items():
                            if row.get_text(strip=True) == key:
                                # Находим следующую ячейку с версией
                                version_cell = row.find_next_sibling("td", class_="versionColumn actualVersionColumn")
                                if version_cell:
                                    # Получаем текст из ячейки
                                    cell_text = version_cell.get_text().strip('\n ')

                                    # Проверяем, сколько строк в ячейке
                                    if len(cell_text.split('\n')) > 2:
                                        # Разделяем текст по строкам и берем вторую часть
                                        actual_version = compare_versions(cell_text.split()[0].strip(),
                                                                          cell_text.split()[1].strip())
                                    else:
                                        # Если тега <br> нет, используем весь текст
                                        actual_version = cell_text.strip()

                                    result_dict[key] = value + ' - ' + actual_version
                                    continue
                else:
                    print("Не удалось авторизоваться")
            else:
                print(f"Ошибка при отправке POST-запроса: {response.status_code}")
        else:
            print(f"Ошибка при отправке GET-запроса: {response.status_code}")

    return result_dict


def compare_versions(version1, version2):
    # Разбиваем строки на компоненты
    components1 = list(map(int, version1.split('.')))
    components2 = list(map(int, version2.split('.')))

    # Выполняем сравнение по каждой цифре
    for comp1, comp2 in zip(components1, components2):
        if comp1 > comp2:
            return version1
        elif comp1 < comp2:
            return version2

    # Если все компоненты совпадают до конца, возвращаем исходную версию с большим количеством компонентов
    if len(components1) > len(components2):
        return version1
    elif len(components1) < len(components2):
        return version2

    # Если все компоненты совпадают, возвращаем любую из версий (в данном случае, первую)
    return version1
