from data import *
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from get_version_1c import get_version_1c


def gen_pub_dict() -> dict:
    version_1c_dict = get_version_1c()
    selected_urls = dict()

    # Чтение куки из файла
    cookies = {}
    with open('cookies.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            name, value = line.strip().split('=')
            cookies[name] = value

    # Создаем сессию для работы с сайтом
    session = requests.Session()
    session.cookies.update(cookies)
    # Выполняем GET-запрос для получения кук
    response = session.get(profile_url)

    # Проверяем успешность авторизации
    if response.status_code == requests.codes.ok:

        # Если авторизация прошла успешно, начинаем отбор публикаций для изменения
        for i in range(1, 5):
            response = session.get(pagination_url + str(i))
            # Обрабатываем полученные данные
            if response.status_code == requests.codes.ok:
                html_content = response.content

                # Создаем объект BeautifulSoup для парсинга HTML
                soup = BeautifulSoup(html_content, 'html.parser')

                # Находим элементы, содержащие информацию о публикациях
                # publication_elements = soup.find_all('div', class_='publication-item')
                publication_elements = soup.select('div.publication-item:not(.unactive)')

                # Обходим элементы публикаций и извлекаем информацию
                for publication_element in publication_elements:

                    # Извлекаем нужную информацию о публикации
                    preview_text = publication_element.find('p', class_='public-preview-text-wrap').text.strip()
                    link = publication_element.find('a', class_='font-md').attrs['href']
                    date = publication_element.find('span', class_='text-nowrap').text.strip()

                    # Преобразовываем дату в объект datetime
                    publication_date = datetime.strptime(date, '%d.%m.%Y')

                    # match_object = re.search(pattern, preview_text)
                    matches = re.finditer(pattern, preview_text)

                    for match in matches:
                        # Проверяем, что год публикации больше или равен start_year
                        if publication_date.year >= start_year:

                            for value in version_1c_dict.values():
                                if value.split()[0] == match.group().split()[0] and value != match.group():
                                    preview_text = preview_text.replace(match.group(), value)
                                    selected_urls[link.split('/')[2]] = preview_text
                                    break

            else:
                print("Не удалось получить данные:", response.status_code)
    else:
        print("Ошибка при получении кук:", response.status_code)

    one_pub = session.get('https://infostart.ru/marketplace/717444/')

    if one_pub.status_code == requests.codes.ok:
        one_pub_content = one_pub.content
        one_pub_soup = BeautifulSoup(one_pub_content, 'html.parser')
        one_pub_preview_text = one_pub_soup.find('p', class_='lh-sm mb-4').text.strip()
        one_pub_link = '717444'
        one_pub_match_object = re.search(pattern, one_pub_preview_text)

        if bool(one_pub_match_object):

            for value in version_1c_dict.values():
                if value.split()[0] == one_pub_match_object.group().split()[0]:
                    one_pub_preview_text = one_pub_preview_text.replace(one_pub_match_object.group(), value)
                    selected_urls[one_pub_link] = one_pub_preview_text
                    break

    return selected_urls
