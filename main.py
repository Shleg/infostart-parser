import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from settings import SiteSettings


def edit_pub(pub_id: str, text: str, driver, edit_url) -> None:
    driver.get(edit_url + pub_id)
    textarea = driver.find_element(By.NAME, 'FIELDS[PREVIEW_TEXT]')
    textarea.clear()
    textarea.send_keys(text)
    save_button = driver.find_element(By.CSS_SELECTOR, 'button[name="ACTION"][value="H"]')
    save_button.click()
    WebDriverWait(driver, 10).until(EC.staleness_of(save_button))


def main():
    site = SiteSettings()
    # Начальные данные
    driver_path = 'geckodriver'
    login_url = 'https://infostart.ru/auth/?login=yes'
    edit_url = 'https://infostart.ru/public/edit/?id='
    pagination_url = 'https://infostart.ru/profile/public/?PAGEN_1='
    pattern = r'\s\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s-\s\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
    start_year = 2018

    replacement_dict = {
        '3.0.57.17 - 3.0.137.39': '3.0.57.17 - 3.0.138.24',  # Бухгалтерия предприятия
        '1.6.13.38 - 3.0.4.65': '1.6.13.38 - 3.0.4.88',  # Управление нашей фирмой
        '2.2.10.19 - 3.0.4.65': '2.2.10.19 - 3.0.4.88',  # Розница
        '3.1.17.138 - 3.1.26.11': '3.1.17.138 - 3.1.26.11',  # ЗиКГУ и ЗУП
        '3.1.8.216 - 3.1.26.11': '3.1.8.216 - 3.1.26.11',  # ЗиКГУ и ЗУП
        '2.4.5.86 - 2.5.12.64': '2.4.5.86 - 2.5.12.73',  # Комплексная автоматизация
        '2.4.7.151 - 2.5.12.64': '2.4.7.151 - 2.5.12.73',  # ERP Управление предприятием
        '11.4.1.254 - 11.5.12.64': '11.4.1.254 - 11.5.12.73'  # Управление торговлей
    }

    # Получение значений из конфигурационного файла
    username = site.username.get_secret_value()
    password = site.password.get_secret_value()

    # Создаем сессию для работы с сайтом
    session = requests.Session()

    # Выполняем GET-запрос для получения кук
    response = session.get(login_url)

    # Проверяем успешность выполнения GET-запроса
    if response.status_code == 200:
        # Отправляем POST-запрос на страницу авторизации с данными пользователя и куками
        login_data = {
            "AUTH_FORM": 'Y',
            "TYPE": 'AUTH',
            "USER_LOGIN": username,
            "USER_PASSWORD": password,
            'USER_REMEMBER': 'Y'
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/113.0.0.0 Safari/537.36",
            "Referer": login_url
        }
        response = session.post(login_url, data=login_data, headers=headers, allow_redirects=True)

        # Проверяем успешность авторизации
        if response.status_code == 200:
            # Если авторизация прошла успешно, начинаем отбор публикаций для изменения
            selected_urls = dict()

            for i in range(1, 5):
                response = session.get(pagination_url + str(i), allow_redirects=True)
                # Обрабатываем полученные данные
                if response.status_code == 200:
                    html_content = response.content
                    # Создаем объект BeautifulSoup для парсинга HTML
                    soup = BeautifulSoup(html_content, 'html.parser')

                    # Находим элементы, содержащие информацию о публикациях
                    publication_elements = soup.find_all('div', class_='publication-item')
                    # publication_elements = soup.select('div.publication-item:not(.unactive)')

                    # Обходим элементы публикаций и извлекаем информацию
                    for publication_element in publication_elements:
                        # Извлекаем нужную информацию о публикации
                        preview_text = publication_element.find('p', class_='public-preview-text-wrap').text.strip()
                        link = publication_element.find('a', class_='font-md').attrs['href']
                        date = publication_element.find('span', class_='text-nowrap').text.strip()

                        # Преобразовываем дату в объект datetime
                        publication_date = datetime.strptime(date, '%d.%m.%Y')

                        # Проверяем, что год публикации больше или равен start_year
                        if publication_date.year >= start_year and bool(re.search(pattern, preview_text)):
                            for key, value in replacement_dict.items():
                                if key in preview_text:
                                    preview_text = preview_text.replace(key, value)
                                selected_urls[link.split('/')[2]] = preview_text

                else:
                    print("Не удалось получить данные:", response.status_code)
            print(selected_urls)
            print(len(selected_urls))
            # Создаем экземпляр сервиса GeckoDriver
            service = Service(executable_path=driver_path)
            # Создать экземпляр драйвера браузера Firefox
            driver = webdriver.Firefox(service=service)

            driver.get(login_url)

            # Находим элементы для ввода логина и пароля
            username_input = driver.find_element(By.NAME, 'USER_LOGIN')
            password_input = driver.find_element(By.NAME, 'USER_PASSWORD')

            # Вводим логин и пароль
            username_input.send_keys(username)
            password_input.send_keys(password)
            login_button = driver.find_element(By.NAME, 'Login')
            login_button.click()
            WebDriverWait(driver, 10).until(EC.staleness_of(login_button))
            for key, value in selected_urls.items():
                edit_pub(key, value, driver, edit_url)
            driver.quit()

        else:
            print("Ошибка авторизации:", response.status_code)
    else:
        print("Ошибка при получении кук:", response.status_code)


if __name__ == '__main__':
    main()
