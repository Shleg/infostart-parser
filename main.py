import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import WebDriverException

import pub_dict
from data import *


def main():
    # Создание экземпляра драйвера браузера Chrome
    options = webdriver.ChromeOptions()
    options.executable_path = driver_path
    driver = webdriver.Chrome(options=options)

    # Открытие страницы
    driver.get(login_url)

    # Ожидание решения капчи вручную
    input("Введите логин и пароль, затем нажмите Enter, после решения капчи...")

    # Находим элементы для ввода логина и пароля
    username_input = driver.find_element(By.NAME, 'USER_LOGIN')
    password_input = driver.find_element(By.NAME, 'USER_PASSWORD')

    # Вводим логин и пароль
    username_input.send_keys(username)
    password_input.send_keys(password)

    # Нажатие кнопки логина
    login_button = driver.find_element(By.NAME, 'Login')
    login_button.click()

    # Ожидание завершения авторизации
    WebDriverWait(driver, 5).until(EC.staleness_of(login_button))

    # Сохранение куки в файл
    cookies = driver.get_cookies()
    with open('cookies.txt', 'w') as f:
        for cookie in cookies:
            f.write(f"{cookie['name']}={cookie['value']}\n")

    selected_urls = pub_dict.gen_pub_dict()
    print(f'Будет обновлено {len(selected_urls)} публикаций!')

    if selected_urls:

        for key, value in selected_urls.items():
            driver.get(edit_url + key)
            textarea = driver.find_element(By.NAME, 'FIELDS[PREVIEW_TEXT]')
            textarea.clear()
            textarea.send_keys(value)

            # # Ожидание появления хотя бы одного элемента select с таймаутом в 10 секунд
            # select_elements = WebDriverWait(driver, 3).until(
            #     EC.presence_of_all_elements_located((By.NAME, "FILES[CLASS_TYPE][]"))
            # )

            # Задаем значение, которое хотим выбрать
            # value_to_select = "9329"
            #
            # # Проверяем, есть ли хотя бы один элемент
            # if select_elements:
            #     # Проходимся по каждому элементу и выбираем значение
            #     for select_element in select_elements:
            #         try:
            #             # Пытаемся выбрать значение
            #             select = Select(select_element)
            #             select.select_by_value(value_to_select)
            #         except WebDriverException as e:
            #             # Обрабатываем исключение, если не удается выбрать значение
            #             print(f"Не удалось выбрать значение в элементе select.")
            # else:
            #     print("Элементы select не найдены")

            try:
                save_button = driver.find_element(By.CSS_SELECTOR, 'button[name="ACTION"][value="Y"]')
            except NoSuchElementException:
                print("Кнопка публикации не найдена")
                try:
                    save_button = driver.find_element(By.CSS_SELECTOR, 'button[name="ACTION"][value="M"]')
                except NoSuchElementException:
                    print("Кнопка модерации не найдена")
            save_button.click()
            WebDriverWait(driver, 20).until(EC.staleness_of(save_button))

    # Закрытие браузера
    driver.quit()


if __name__ == '__main__':
    main()
