#! env/bin/python3.6
# -*- coding: utf8 -*-

"""Модели данных БД."""

import re
import dateutil.parser

from jsonschema import validators, Draft7Validator
from jsonschema.exceptions import ValidationError
from validate_email import validate_email

# ------------------------------------------------------------
# Схемы
# ------------------------------------------------------------

#  Профиль пользователя CMS

#  Есть проблемы при валидации списка почт:
#  при запросе к API value должно быть обязательно,
#  но эта валидация не проходит
schema_profile_data = {
    "type": "object",
    "properties": {
        "login": {
                    "type": "string",
                    "pattern": r"\b[a-zA-Z0-9]{4,20}\b",
                    "minLength": 1
                 },
        "name": {
                    "type": "string",
                    "pattern": r'\b[а-яА-Я]{4,20}\b',
                    "minLength": 1
                 },
        "surname": {
                    "type": "string",
                    "pattern": r'\b[а-яА-Я]{4,20}\b',
                    "minLength": 1
                 },
        "patronymic": {
                    "type": "string",
                    "pattern": r'\b[а-яА-Я]{4,20}\b',
                    "minLength": 1
                 },
        "email": {
                    "type": "array",
                    "maxItems": 3,
                    "minItems": 3,
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        'properties': {
                            "value": {
                                "type": "string",
                            },
                            "type": {
                                "type": "string",
                                'enum': ["primary", "work", "personal"],
                            },
                            "activeUntil": {
                                "type": "string",
                                'is_date': True,
                            },
                            "verified": {
                                "type": "boolean",
                            },
                        },
                        "required": [
                            "verified",
                            "type",
                            "value",
                            "activeUntil"
                            ],
                        "if": {
                            "properties": {
                              "type": {"const": "primary"}
                            },
                            "required": ["type", "value"],
                          },
                        "then": {"is_email_primary": ["value"]},
                        "else": {"is_email": ["value"]}
                    },
                 },
        "phone": {
                    "type": "string",
                    "pattern": r'(^\+7\s\d{3,3}\s\d{3,3}\s\d{2,2}\s\d{2,2}$)',
                    "minLength": 1
                 },
        "birth_date": {
                    "type": "string",
                    'is_date': True,
                    "minLength": 1
                      },
        "about_me": {
                    "type": ["string", "null"],
                    "pattern": r'(^.{0,140}$)'
                    },
        "password": {
                    "type": "string",
                    "is_valid": True,
                    "minLength": 8
                    },
    },
    "required": ["login", "email", "phone"],
    "additionalProperties": False
}

schema_profile_password = {
    "type": "object",
    "properties": {
        "login": {
                    "type": "string",
                    "pattern": r"\b[a-zA-Z0-9]{4,20}\b",
                    "minLength": 1
                 },
        "passwordOld": {
                    "type": "string",
                    "minLength": 1
                 },
        "passwordNew": {
                    "type": "string",
                    "is_valid": True,
                    "minLength": 8
                    },
    },
    "required": ["login", "passwordNew", "passwordOld"],
    "additionalProperties": False
}

#  Пользователь CMS

schema_user_data = {
    "type": "object",
    "properties": {
        "login": {
                    "type": "string",
                    "pattern": r"\b[a-zA-Z0-9]{4,20}\b",
                    "minLength": 1
                 },
        "name": {
                    "type": "string",
                    "pattern": r'\b[а-яА-Я]{4,20}\b',
                    "minLength": 1
                 },
        "surname": {
                    "type": "string",
                    "pattern": r'\b[а-яА-Я]{4,20}\b',
                    "minLength": 1
                 },
        "patronymic": {
                    "type": "string",
                    "pattern": r'\b[а-яА-Я]{4,20}\b',
                    "minLength": 1
                 },
        "email": {
                    "type": "array",
                    "maxItems": 3,
                    "minItems": 3,
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        'properties': {
                            "value": {
                                "type": "string",
                            },
                            "type": {
                                "type": "string",
                                'enum': ["primary", "work", "personal"],
                            },
                        },
                        "required": [
                            "type",
                            "value",
                            ],
                        "if": {
                            "properties": {
                              "type": {"const": "primary"}
                            },
                            "required": ["type", "value"],
                          },
                        "then": {"is_email_primary": ["value"]},
                        "else": {"is_email": ["value"]}
                    },
                 },
        "phone": {
                    "type": "string",
                    "pattern": r'(^\+7\s\d{3,3}\s\d{3,3}\s\d{2,2}\s\d{2,2}$)',
                    "minLength": 1
                 },
        "birth_date": {
                    "type": "string",
                    'is_date': True,
                    "minLength": 1
                      },
        "about_me": {
                    "type": ["string", "null"],
                    "pattern": r'(^.{0,140}$)'
                    },
        "password": {
                    "type": "string",
                    "is_valid": True,
                    "minLength": 8
                    },
    },
    "required": ["login", "email", "phone", "password",
                 "birth_date", "name", "surname", "patronymic"],
    "additionalProperties": False
}

# ------------------------------------------------------------
# Кастомные валидаторы
# ------------------------------------------------------------


def is_email_primary(validator, value, instance, schema_profile_data):
    if not isinstance(instance['value'], str):
        yield ValidationError("%r not string" % instance['value'])
    if re.search(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
                 instance['value']) is None:
        yield ValidationError(
            "%r не в формате почты или пустая строка" % (instance['value']))
    elif (validate_email(instance['value'], verify=True) is None or
          not validate_email(instance['value'], verify=True)):
        yield ValidationError(
            "%r адрес почты не существует в сети!" % (instance['value']))


def is_email(validator, value, instance, schema_profile_data):
    if not isinstance(instance['value'], str):
        yield ValidationError("%r not string" % instance['value'])
    if len(instance['value']) > 0:
        if re.search(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
                     instance['value']) is None:
            yield ValidationError(
                "%r не в формате почты" % (instance['value']))
        elif (validate_email(instance['value'], verify=True) is None or
              not validate_email(instance['value'], verify=True)):
            yield ValidationError(
                "%r адрес почты не существует в сети!" % (instance['value']))


def is_date(validator, value, instance, schema_profile_data):
    try:
        dateutil.parser.parse(instance)
    except ValueError:
        yield ValidationError("%r incorrect date format" % (instance))


def is_valid(validator, value, instance, schema_profile_password):
    if not isinstance(instance, str):
        yield ValidationError("%r not string" % instance)

    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    alphabet_upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numeric = '0123456789'
    special = '!@#$%^&*()_+~`|}{[]:;?><,./-='

    occurs = {'alphabet': 0, 'alphabetUpper': 0,
              'numeric': 0, 'special': 0}

    for char in instance:
        if char in alphabet:
            occurs['alphabet'] += 1
        if char in alphabet_upper:
            occurs['alphabetUpper'] += 1
        if char in numeric:
            occurs['numeric'] += 1
        if char in special:
            occurs['special'] += 1

    for key, value in occurs.items():
        if value == 0:
            yield ValidationError(
                "%r incorrect format of password (minimum 1 lower- and "
                "uppercase alphabet, numeric, and special characters)" % (
                    instance))
            break


all_validators = dict(Draft7Validator.VALIDATORS)
all_validators.update({'is_email_primary': is_email_primary,
                       'is_email': is_email,
                       'is_date': is_date, 'is_valid': is_valid})

MyValidator = validators.create(
    meta_schema=Draft7Validator.META_SCHEMA,
    validators=all_validators
)

profile_validator = MyValidator(schema_profile_data)
password_validator = MyValidator(schema_profile_password)
user_validator = MyValidator(schema_user_data)
