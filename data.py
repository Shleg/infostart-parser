import os
from settings import SiteSettings

# Начальные данные
site = SiteSettings()
script_directory = os.path.dirname(os.path.abspath(__file__))
driver_path = os.path.join(script_directory, 'service/chromedriver')
profile_url = 'https://infostart.ru/profile/public/'
login_url = 'https://infostart.ru/auth/?login=yes'
edit_url = 'https://infostart.ru/public/edit/?id='
pagination_url = 'https://infostart.ru/profile/public/?PAGEN_1='
publication_url = 'https://infostart.ru/1c/reports/'
pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s-\s\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
start_year = 2018
releases_url = 'https://releases.1c.ru/total'
login_1c_url = 'https://login.1c.ru'

# replacement_dict = {
#             '3.0.57.17 - 3.0.143.42': '3.0.57.17 - 3.0.145.19',  # Бухгалтерия предприятия
#             '1.6.13.38 - 3.0.5.199': '1.6.13.38 - 3.0.6.100',  # Управление нашей фирмой
#             '2.2.10.19 - 3.0.5.199': '2.2.10.19 - 3.0.5.199',  # Розница
#             '3.1.17.138 - 3.1.28.11': '3.1.17.138 - 3.1.28.35',  # ЗиКГУ и ЗУП
#             '3.1.8.216 - 3.1.28.11': '3.1.8.216 - 3.1.28.35',  # ЗиКГУ и ЗУП
#             '2.4.5.86 - 2.5.14.82': '2.4.5.86 - 2.5.15.57',  # Комплексная автоматизация
#             '2.4.7.151 - 2.5.14.82': '2.4.7.151 - 2.5.15.57',  # ERP Управление предприятием
#             '11.4.1.254 - 11.5.14.82': '11.4.1.254 - 11.5.15.57'  # Управление торговлей
#         }

# список с наименованиями версий конфигураций
conf_dict = {
    'Бухгалтерия предприятия, редакция 3.0': '3.0.57.17',
    'Управление нашей фирмой, редакция 3.0': '1.6.13.38',
    'Розница, редакция 3.0 (рекомендуется)': '2.2.10.19',
    'Зарплата и Управление Персоналом базовая, редакция 3': '3.1.17.138',
    'Зарплата и кадры государственного учреждения базовая, редакция 3': '3.1.8.216',
    'Комплексная автоматизация, редакция 2': '2.4.5.86',
    '1С:ERP Управление предприятием 2': '2.4.7.151',
    'Управление торговлей, редакция 11': '11.4.1.254'
}

# Получение значений из конфигурационного файла
username = site.username.get_secret_value()
password = site.password.get_secret_value()

username_1c = site.username_1c.get_secret_value()
password_1c = site.password_1c.get_secret_value()