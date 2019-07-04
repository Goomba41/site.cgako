#! env/bin/python3.6
# -*- coding: utf8 -*-

"""Конфигурационный файл бэкенда."""

import os

# Конфигурация
DEBUG = True
CSRF_ENABLED = True
JSON_AS_ASCII = False

# Базовая директория
BASEDIR = os.path.abspath(os.path.dirname(__file__))
CMS_USERS_AVATARS = os.path.join(BASEDIR, 'client/static/profile_avatars/')

# Соединение с БД
SQLALCHEMY_BASIC_URI = 'mysql+pymysql://user:password@localhost/'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@localhost/\
cgako_site_db'
SQLALCHEMY_TRACK_MODIFICATIONS = 'true'

# Умолчания
LIMIT = 20  # Количество записей в пагинированном json
CMS_USER_REACTIVATION = 20  # Время для реактивации почты пользователей CMS

# Аутентификация
#  SECRET_KEY = "..."  # Ключ
TOKEN_DURATION = 1  # Длительность валидности токена в днях

# Верификация почты
#  VERIFICATION_SALT = "..."  # Соль

# Настройка почтового клиента для отправки писем
MAIL_SERVER = 'smtp.yandex.ru'
MAIL_PORT = 465

MAIL_USE_TLS = False
MAIL_USE_SSL = True

MAIL_USERNAME = '...'
#  MAIL_PASSWORD = '...'
MAIL_DEFAULT_SENDER = "..."
