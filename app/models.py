#! env/bin/python3.6
# -*- coding: utf8 -*-

"""Модели данных БД."""

from app import bcrypt, db, ma
from flask import json
from sqlalchemy import func

class CmsUsers(db.Model):
    """Модель данных пользователя."""

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(60))
    socials = db.Column(db.JSON(none_as_null=True))
    photo = db.Column(db.String(50))
    name = db.Column(db.String(20))
    surname = db.Column(db.String(20))
    patronymic = db.Column(db.String(20))
    email = db.Column(db.JSON(none_as_null=True))
    phone = db.Column(db.String(18), unique=True)
    about_me = db.Column(db.Text())

    birth_date = db.Column(db.Date)
    last_login = db.Column(db.JSON(none_as_null=True))

    status = db.Column(db.SmallInteger)

    # department_id = db.Column(db.Integer,
    # db.ForeignKey("arhiv.department.id"))
    # post_id = db.Column(db.Integer, db.ForeignKey("arhiv.post.id"))
    # role_id = db.Column(db.Integer, db.ForeignKey("arhiv.role.id"))

    # important_news = db.relationship('Important_news',
    # backref = 'user',lazy = 'dynamic')
    # history = db.relationship('History', backref = 'user_parent',
    # lazy = 'dynamic')
    # permission = db.relationship('Permission', backref = 'user',
    # lazy = 'dynamic')
    # news = db.relationship('News', backref = 'user',lazy = 'dynamic')
    # appeals = db.relationship('Appeals', backref = 'user',lazy = 'dynamic')
    # executor = db.relationship('Executor', backref = 'user',lazy = 'dynamic')

    # employee = db.relationship('Item',
    # backref='item_employee',
    # lazy='dynamic',
    # foreign_keys='Item.employee')
    # responsible = db.relationship('Item',
    # backref='item_responsible',
    # lazy='dynamic',
    # foreign_keys='Item.responsible')

    def __init__(self, login, password,
                 name, surname, patronymic,
                 email, phone, birth_date, about_me=None,
                 last_login=None, status=None, socials=None, photo=None):
        """Конструктор класса."""
        self.login = login
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.socials = {"ok": "",
                        "vk": "",
                        "google": "",
                        "yandex": ""} if socials is None else socials
        self.photo = None if photo is None else photo
        self.name = name
        self.surname = surname
        self.patronymic = patronymic
        self.email = email
        self.phone = phone
        self.birth_date = birth_date
        self.last_login = None if last_login is None else last_login
        self.status = 1 if status is None else status
        self.about_me = None if about_me is None else about_me

    def __repr__(self):
        """Форматирование представления экземпляра класса."""
        return 'Пользователь id:%i, логин:%r ' % (self.id, self.login)

    @classmethod
    def authenticate(cls, **kwargs):
        """Функция аутентификации."""
        login = kwargs.get('login')
        password = kwargs.get('password')

        if not login or not password:
            return (None, 'Не переданы данные\
        для аутентификации пользователя!', 'empty')

        #  email = {"value": login, "verified": True} # Вход через любую подтвержденную почту, привязанную к пользователю
        #  user = cls.query.filter((cls.login == login) | (func.json_contains(cls.email, json.dumps(email)))).first()

        user = cls.query.filter((cls.login == login) | (func.json_contains(cls.email, json.dumps({"value": login})))).first()

        if user:
            mail_status = list(filter(lambda mail: mail['type'] == "primary", user.email))
            if mail_status and not mail_status[0]['verified']:
                return (None, 'Основная почта не активирована!', 'username')
            elif not bcrypt.check_password_hash(user.password, password):
                return (None, 'Неверный пароль!', 'password')
        else:
            return (None, 'Пользователь не найден!', 'username')

        return (user, 'Успешно!')

    @classmethod
    def exist(cls, sid=None, **kwargs):
        """Проверка существования пользователя с данными в базе"""
        email_condition = {"value": kwargs.get('email'), "type": "primary"}

        if sid is None:
            exist = cls.query.filter(
                    (cls.login == kwargs.get('login')) |
                    ((func.json_contains(cls.email, json.dumps(email_condition)))) |
                    (cls.phone == kwargs.get('phone'))).first()
        else:
            exist = cls.query.filter(
                    ((cls.login == kwargs.get('login')) |
                     ((func.json_contains(cls.email, json.dumps(email_condition)))) |
                     (cls.phone == kwargs.get('phone'))) &
                    (cls.id != sid)).first()
        if exist:
            return True
        return False


class CmsUsersSchema(ma.ModelSchema):
    """Marshmallow-схема для перегона модели в json формат."""

    class Meta:
        """Мета модели, вносятся доп. параметры."""

        model = CmsUsers


class CmsProfileSchema(ma.ModelSchema):
    """Marshmallow-схема для перегона модели в json формат."""

    class Meta:
        """Мета модели, вносятся доп. параметры."""

        model = CmsUsers
        fields = ("login", "surname", "name", "patronymic", "email", "phone",
                  "birth_date", "about_me", "socials", "photo")
