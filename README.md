# Инструкция по использованию программы

## Подготовка

1. Убедитесь, что в папке `service` находится актуальная версия `chromedriver`.

Скачать можно тут: https://googlechromelabs.github.io/chrome-for-testing/
## Запуск программы

1. Откройте терминал или командную строку.
2. Перейдите в директорию программы.

    ```bash
    cd путь_к_программе
    ```

3. Запустите основной скрипт `main.py`.

    ```bash
    python main.py
    ```

## Решение капчи и продолжение выполнения

1. В открывшемся браузере решите капчу.
2. Нажмите Enter в окне выполнения скрипта.

## Автоматическое выполнение

После ввода капчи, программа автоматически выполняет следующие шаги:

1. Получает список актуальных версий с сайта 1С.
2. Подбирает публикации для редактирования.
3. Формирует словарь, где ключ - id публикации, а значение - текст публикации.

## Редактирование публикаций

1. Словарь последовательно обходится.
2. В браузере открывается каждая публикация на редактирование.
3. Текст публикации заменяется.

Примечание: Весь процесс автоматизирован, после ввода капчи вам не требуется вмешательства в работу программы.
