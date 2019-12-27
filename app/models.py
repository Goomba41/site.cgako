#! env/bin/python3.6
# -*- coding: utf8 -*-

"""Модели данных БД."""
from datetime import datetime

from app import bcrypt, db, ma

from dateutil.relativedelta import relativedelta

from flask import current_app, json

from sqlalchemy import func

from marshmallow import fields, pre_load, post_dump

from sqlalchemy_mptt.mixins import BaseNestedSets

# ------------------------------------------------------------
# Функции
# ------------------------------------------------------------

#  Обработка полученноых почт от пользователя
def cms_user_emails(emails):
    """Обработка почт."""
    for email_item in emails:
        email_item.update(
            {"verified": False,
             "activeUntil": (datetime.now() + relativedelta(
                                months=1)).isoformat()})
    return emails


# ------------------------------------------------------------
# Ассоциативные таблицы
# ------------------------------------------------------------

user_role = db.Table(
    'association_user_role',
    db.Column(
        'user_id',
        db.Integer,
        db.ForeignKey('cms_users.id'),
        primary_key=True
    ),
    db.Column(
        'role_id',
        db.Integer,
        db.ForeignKey('cms_roles.id'),
        primary_key=True
    )
)

role_permission = db.Table(
    'association_role_permission',
    db.Column(
        'role_id',
        db.Integer,
        db.ForeignKey('cms_roles.id'),
        primary_key=True
    ),
    db.Column(
        'permission_id',
        db.Integer,
        db.ForeignKey('association_permission.id'),
        primary_key=True
    )
)

# ------------------------------------------------------------
# Модели
# ------------------------------------------------------------


class CmsUsers(db.Model):
    """Модель данных пользователя."""

    id = db.Column(db.Integer, primary_key=True) # noqa: ignore=A003
    login = db.Column(db.String(20), unique=True, comment="Уникальный логин")
    password = db.Column(
        db.JSON(none_as_null=True),
        comment="Пароль и параметры"
    )
    socials = db.Column(
        db.JSON(none_as_null=True),
        comment="Идентификаторы социальных сетей"
    )
    photo = db.Column(db.String(50), comment="Имя файла фотокарточки")
    name = db.Column(db.String(20), comment="Имя")
    surname = db.Column(db.String(20), comment="Фамилия")
    patronymic = db.Column(db.String(20), comment="Отчество")
    email = db.Column(
        db.JSON(none_as_null=True),
        comment="Электронная почта и параметры"
    )
    phone = db.Column(db.String(18), unique=True, comment="Телефон")
    about_me = db.Column(db.Text(), comment="О себе (например, должность)")

    birth_date = db.Column(db.Date, comment="Дата рождения")
    last_login = db.Column(
        db.JSON(none_as_null=True),
        comment="Данные последнего входа"
    )

    status = db.Column(
        db.SmallInteger,
        comment="Статус записи пользователя (пока не используется)"
    )

    roles = db.relationship(
        'CmsRoles',
        secondary=user_role,
        lazy='subquery',
        backref=db.backref('users', lazy=True)
    )

    def __init__(self, login, password,
                 name, surname, patronymic,
                 email, phone, birth_date, about_me=None,
                 last_login=None, status=None, socials=None, photo=None):
        """Конструктор класса."""
        self.login = login
        self.password = {
            "value": bcrypt.generate_password_hash(password).decode('utf-8'),
            "blocked": False,
            "first_auth": True,
            "activeUntil": (datetime.now() + relativedelta(
                                    months=1)).isoformat(),
            "failed_times": 0
        }
        self.socials = {"ok": "",
                        "vk": "",
                        "google": "",
                        "yandex": ""} if socials is None else socials
        self.photo = None if photo is None else photo
        self.name = name
        self.surname = surname
        self.patronymic = patronymic
        self.email = cms_user_emails(email)
        self.phone = phone
        self.birth_date = birth_date
        self.last_login = None if last_login is None else last_login
        self.status = 1 if status is None else status
        self.about_me = '' if about_me is None else about_me

    def __repr__(self):
        """Форматирование представления экземпляра класса."""
        return 'Пользователь логин:%r ' % (self.login)

    @classmethod
    def authenticate(cls, check=False, **kwargs):
        """Функция аутентификации."""
        login = kwargs.get('login')
        password = kwargs.get('password')

        if not login or not password:
            return (None, 'Не переданы данные\
        для аутентификации пользователя!', 'empty')

        #  email = {"value": login, "verified": True}
        # Вход через любую подтвержденную почту, привязанную к пользователю
        #  user = cls.query.filter((cls.login == login) |
        #  (func.json_contains(cls.email, json.dumps(email)))).first()

        user = cls.query.filter((cls.login == login) | (
            func.json_contains(cls.email, json.dumps(
                {"value": login})))).first()

        if user:
            mail_status = list(
                filter(lambda mail: mail['type'] == "primary", user.email))
            if mail_status and not mail_status[0]['verified']:
                return (None, 'Основная почта не активирована!', 'username')
            elif user.password['blocked'] and not check:
                return (None, 'Пароль заблокирован!', 'password')
            elif not bcrypt.check_password_hash(
                    user.password['value'], password):
                max_fails = current_app.config['MAX_FAILED']
                user.password['failed_times'] += 1
                if user.password['failed_times'] >= max_fails:
                    user.password['blocked'] = True
                    user.password['failed_times'] = 0
                    CmsUsers.query.filter_by(id=user.id).update(
                        {'password': user.password})
                    db.session.commit()
                    return (None, 'Неверный пароль! Ваш пароль заблокирован!',
                            'password')
                else:
                    CmsUsers.query.filter_by(id=user.id).update(
                        {'password': user.password})
                    db.session.commit()
                    return (None, 'Неверный пароль! '
                            'Осталось попыток ввода: %i' % (
                                max_fails - user.password['failed_times']),
                            'password')
        else:
            return (None, 'Пользователь не найден!', 'username')

        user.password['failed_times'] = 0
        CmsUsers.query.filter_by(id=user.id).update(
            {'password': user.password})
        db.session.commit()

        return (user, 'Успешно!')

    @classmethod
    def exist(cls, sid=None, **kwargs):
        """Проверка существования пользователя с данными в базе."""
        email_condition = {"value": kwargs.get('email'), "type": "primary"}

        if sid is None:
            exist = cls.query.filter(
                    (cls.login == kwargs.get('login')) |
                    ((func.json_contains(
                        cls.email, json.dumps(email_condition)))) |
                    (cls.phone == kwargs.get('phone'))).first()
        else:
            exist = cls.query.filter(
                    ((cls.login == kwargs.get('login')) |
                     ((func.json_contains(
                        cls.email, json.dumps(email_condition)))) |
                     (cls.phone == kwargs.get('phone'))) &
                    (cls.id != sid)).first()
        if exist:
            return True
        return False

    @classmethod
    def can(cls, uid=None, action=None, object=None):
        """Проверка разрешений пользователя"""
        if cls.query.join(
            user_role).join(
                CmsRoles).join(
                    role_permission).join(
                        AssociationPermission).join(
                            SystemObjects).join(
                                SystemObjectsActions).filter(
                                    (CmsUsers.id == uid) &
                                    (SystemObjectsActions.uri == action) &
                                    (SystemObjects.uri == object)).first():
            return True
        return False


class CmsRoles(db.Model):
    """Модель системных ролей."""

    id = db.Column(db.Integer, primary_key=True) # noqa: ignore=A003
    title = db.Column(db.String(50), unique=True, comment="Название роли")
    deletable = db.Column(
        db.Boolean,
        default=True,
        nullable=False,
        comment="Удаляемая"
    )
    editable = db.Column(
        db.Boolean,
        default=True,
        nullable=False,
        comment="Редактируемая"
    )
    reassignable = db.Column(
        db.Boolean,
        default=True,
        nullable=False,
        comment="Переназначаемая"
    )

    permissions = db.relationship(
        'AssociationPermission',
        secondary=role_permission,
        lazy='subquery',
        backref=db.backref('roles', lazy=True)
    )

    def __init__(self, title):
        """Конструктор класса."""
        self.title = title

    def __repr__(self):
        """Форматирование представления экземпляра класса."""
        return 'Роль название:%r ' % (self.title)

    @classmethod
    def exist(cls, rid=None, **kwargs):
        """Проверка существования пользователя с данными в базе."""
        if rid is None:
            exist = cls.query.filter(
                        cls.id == kwargs.get('id')
                    ).first()
        else:
            exist = cls.query.filter(
                    (
                        cls.title == kwargs.get('title')
                    ) &
                    (cls.id != rid)).first()
        if exist:
            return True
        return False


class SystemObjects(db.Model):
    """Модель объектов системы."""

    id = db.Column(db.Integer, primary_key=True) # noqa: ignore=A003
    title = db.Column(db.String(50), unique=True, comment="Название объекта")
    uri = db.Column(db.String(50), unique=True, comment="Идентификатор")

    actions = db.relationship(
        'SystemObjectsActions',
        secondary='association_permission'
    )

    def __init__(self, title):
        """Конструктор класса."""
        self.title = title

    def __repr__(self):
        """Форматирование представления экземпляра класса."""
        return 'Системный объект название:%r ' % (self.title)


class SystemObjectsActions(db.Model):
    """Модель действий над объектами системы."""

    id = db.Column(db.Integer, primary_key=True) # noqa: ignore=A003
    title = db.Column(db.String(50), unique=True, comment="Название действия")
    uri = db.Column(db.String(50), unique=True, comment="Идентификатор")

    objects = db.relationship(
        SystemObjects,
        secondary='association_permission'
    )

    def __init__(self, title):
        """Конструктор класса."""
        self.title = title

    def __repr__(self):
        """Форматирование представления экземпляра класса."""
        return 'Действие над объектом название:%r ' % (self.title)


class AssociationPermission(db.Model):
    """Ассоциативная таблица для создания разрешения (объект + действие)."""

    id = db.Column(db.Integer, autoincrement=True, primary_key=True) # noqa: ignore=A003

    object_id = db.Column(db.Integer, db.ForeignKey('system_objects.id'), comment="Объект")
    action_id = db.Column(db.Integer, db.ForeignKey(
        'system_objects_actions.id'
    ), comment="Действие")

    objects = db.relationship(
        SystemObjects,
        backref=db.backref("permission")
    )
    actions = db.relationship(
        SystemObjectsActions,
        backref=db.backref("permission")
    )


class CmsStructure(db.Model, BaseNestedSets):
    """Модель системных разделов. Иерархическая структура Nested Set."""

    id = db.Column(db.Integer, primary_key=True) # noqa: ignore=A003
    title = db.Column(db.String(50), comment="Название раздела меню и структуры")
    deletable = db.Column(
        db.Boolean,
        default=True,
        nullable=False,
        comment="Удаляемый"
    )
    enabled = db.Column(
        db.Boolean,
        default=True,
        nullable=False,
        comment="Включен"
    )
    editable = db.Column(
        db.Boolean,
        default=True,
        nullable=False,
        comment="Редактируемый"
    )
    movable = db.Column(
        db.Boolean,
        default=True,
        nullable=False,
        comment="Перемещаемый"
    )
    appendable = db.Column(
        db.Boolean,
        default=True,
        nullable=False,
        comment="Потомки"
    )
    page_adding = db.Column(
        db.Boolean,
        default=True,
        nullable=False,
        comment="Добавление страниц"
    )
    pages = db.relationship(
        'SitePages',
        backref='structure',
        lazy='dynamic',
        uselist=True
    )

    def __repr__(self):
        """Форматирование представления экземпляра класса."""
        return "Раздел «%s»" % (self.title)

    @classmethod
    def exist(cls, sid=None, **kwargs):
        """Проверка существования пользователя с данными в базе."""
        if sid is None:
            exist = cls.query.filter(
                        cls.id == kwargs.get('id')
                    ).first()
        else:
            exist = cls.query.filter(
                    (
                        cls.id == kwargs.get('title')
                    ) &
                    (cls.id != sid)).first()
        if exist:
            return True
        return False


class CmsOrganization(db.Model):
    """Модель общей информации об архиве."""

    id = db.Column(db.Integer, primary_key=True) # noqa: ignore=A003
    full_company_name = db.Column(db.String(200), comment="Полное наименование организации")
    company_name = db.Column(db.String(50), comment="Наименование организации")
    requisites = db.Column(
        db.JSON(none_as_null=True),
        comment="Реквизиты организации"
    )
    buildings = db.relationship(
        'CmsOrganizationBuildings',
        backref='organization',
        lazy='dynamic'
    )

    def __repr__(self):
        """Форматирование представления экземпляра класса."""
        return "Организация: «%s»" % (self.company_name)


class CmsOrganizationBuildings(db.Model):
    """Модель общей информации об архиве."""

    id = db.Column(db.Integer, primary_key=True) # noqa: ignore=A003
    name = db.Column(db.String(50), comment="Имя здания")
    road_map = db.Column(db.String(500), comment="Карта проезда")
    work_time = db.Column(
        db.JSON(none_as_null=True),
        comment="Режимы работы"
    )
    employee_contacts = db.Column(
        db.JSON(none_as_null=True),
        comment="Контакты сотрудников"
    )
    organization_id = db.Column(db.Integer, db.ForeignKey('cms_organization.id'), nullable=False)

    def __repr__(self):
        """Форматирование представления экземпляра класса."""
        return "Здание: «%s»" % (self.name)

    def __init__(self, name, road_map=None, organization_id=None, work_time=None, employee_contacts=None):
        """Конструктор класса."""
        self.name = name
        self.road_map = None if road_map is None else road_map
        self.organization_id = CmsOrganization.query.first().id if organization_id is None else organization_id
        self.work_time = [] if work_time is None else work_time
        self.employee_contacts = [] if work_time is None else work_time


class SitePages(db.Model):
    """Модель страниц сайта."""
    id = db.Column(db.Integer, primary_key=True) # noqa: ignore=A003
    uri = db.Column(db.String(50), unique=True, comment="URL страницы")
    title = db.Column(db.String(100), comment="Заголовок страницы")
    text = db.Column(db.Text(), comment="Основной текст страницы")
    cover = db.Column(db.String(40), comment="Обложка страницы")
    gallery = db.Column(
        db.JSON(none_as_null=True),
        comment="Галерея"
    )
    files = db.Column(
        db.JSON(none_as_null=True),
        comment="Файлы"
    )
    seo_description = db.Column(db.String(255), comment="Описание страницы")
    seo_keywords = db.Column(
        db.JSON(none_as_null=True),
        comment="Ключевые слова страницы"
    )
    creation_date = db.Column(db.DateTime, comment="Дата создания/публикации")
    available = db.Column(
        db.Boolean,
        default=True,
        nullable=False,
        comment="Доступна"
    )
    mainpage = db.Column(
        db.Boolean,
        default=True,
        nullable=False,
        comment="На главной"
    )
    banner = db.Column(
        db.Boolean,
        default=False,
        nullable=False,
        comment="В баннер"
    )
    announcement = db.Column(
        db.Boolean,
        default=False,
        nullable=False,
        comment="Анонс"
    )
    structure_id = db.Column(
        db.Integer,
        db.ForeignKey('cms_structure.id'),
        nullable=False,
        comment="ID раздела"
    )

    def __init__(self, title, uri, text, seo_description, seo_keywords,
                 available, mainpage, banner, announcement,
                 structure_id=None, creation_date=None,
                 files=None, gallery=None, cover=None):
        """Конструктор класса."""
        self.title = title
        self.uri = uri
        self.text = text
        self.seo_description = seo_description
        self.seo_keywords = seo_keywords
        self.available = available
        self.mainpage = mainpage
        self.banner = banner
        self.announcement = announcement
        self.structure_id = 51 if structure_id is None else structure_id
        self.creation_date = datetime.utcnow() if creation_date is None else creation_date
        self.files = [] if files is None else files
        self.gallery = [] if gallery is None else gallery
        self.cover = None if cover is None else cover

    def __repr__(self):
        """Форматирование представления экземпляра класса."""
        return "Страница: «%s»" % (self.title)


class HistoryEvents(db.Model):
    """Модель страниц сайта."""
    id = db.Column(db.Integer, primary_key=True) # noqa: ignore=A003
    event_title = db.Column(db.String(100), comment="Заголовок")
    description_text = db.Column(db.Text(), comment="Описательный текст")
    event_date = db.Column(db.DateTime, comment="Дата")

    def __init__(self, event_title, description_text, event_date):
        """Конструктор класса."""
        self.event_title = title
        self.description_text = text
        self.event_date = creation_date

    def __repr__(self):
        """Форматирование представления экземпляра класса."""
        return "Памятная дата: «%s»" % (self.event_title)

# ------------------------------------------------------------
# Схемы
# ------------------------------------------------------------


class SystemObjectsSchema(ma.ModelSchema):
    """Marshmallow-схема для перегона модели в json формат."""

    class Meta:
        """Мета модели, вносятся доп. параметры."""

        model = SystemObjects
        exclude = ("actions", "permission")


class SystemObjectsActionsSchema(ma.ModelSchema):
    """Marshmallow-схема для перегона модели в json формат."""

    class Meta:
        """Мета модели, вносятся доп. параметры."""

        model = SystemObjectsActions
        exclude = ("objects", "permission")


class AssociationPermissionSchema(ma.ModelSchema):
    """Marshmallow-схема для перегона модели в json формат."""

    class Meta:
        """Мета модели, вносятся доп. параметры."""

        model = AssociationPermission
        exclude = ("roles",)

    actions = ma.Nested(SystemObjectsActionsSchema)
    objects = ma.Nested(SystemObjectsSchema)


class CmsRolesSchema(ma.ModelSchema):
    """Marshmallow-схема для перегона модели в json формат."""

    class Meta:
        """Мета модели, вносятся доп. параметры."""

        model = CmsRoles
        exclude = ("users",)
        #  fields = ("id", "title",)

    permissions = ma.Nested(AssociationPermissionSchema, many=True)


class CmsStructureSchema(ma.ModelSchema):
    """Marshmallow-схема для перегона модели в json формат."""

    class Meta:
        """Мета модели, вносятся доп. параметры."""

        model = CmsStructure

class BannerSchema(ma.ModelSchema):
    """Marshmallow-схема для перегона модели в json формат."""

    class Meta:
        """Мета модели, вносятся доп. параметры."""

        model = SitePages
        fields = ("id", "uri", "available", "cover", "seo_description", "text", "title", )

class AnnouncementsSchema(ma.ModelSchema):
    """Marshmallow-схема для перегона модели в json формат."""

    class Meta:
        """Мета модели, вносятся доп. параметры."""

        model = SitePages
        fields = ("id", "uri", "available", "cover", "seo_description", "text", "title", )

class PageSchema(ma.ModelSchema):
    """Marshmallow-схема для перегона модели в json формат."""

    class Meta:
        """Мета модели, вносятся доп. параметры."""

        model = SitePages
        fields = ("id", "uri",)

class MenuSchema(ma.ModelSchema):
    """Marshmallow-схема для перегона модели в json формат."""

    class Meta:
        """Мета модели, вносятся доп. параметры."""

        model = CmsStructure
        fields = ("id", "title", "enabled", "level", "pages")

    pages = ma.Nested(PageSchema, many=True)


class CmsOrganizationBuildingsSchema(ma.ModelSchema):
    """Marshmallow-схема для перегона модели в json формат."""

    class Meta:
        """Мета модели, вносятся доп. параметры."""

        model = CmsOrganizationBuildings


class CmsOrganizationSchema(ma.ModelSchema):
    """Marshmallow-схема для перегона модели в json формат."""

    class Meta:
        """Мета модели, вносятся доп. параметры."""

        model = CmsOrganization
    buildings = ma.Nested(CmsOrganizationBuildingsSchema, many=True)


class CmsUsersSchema(ma.ModelSchema):
    """Marshmallow-схема для перегона модели в json формат."""

    class Meta:
        """Мета модели, вносятся доп. параметры."""

        model = CmsUsers
    roles = ma.Nested(CmsRolesSchema, many=True)


class SitePagesSchema(ma.ModelSchema):
    """Marshmallow-схема для перегона модели в json формат."""

    class Meta:
        """Мета модели, вносятся доп. параметры."""

        model = SitePages
    structure = ma.Nested(CmsStructureSchema)


class HistoryEventsSchema(ma.ModelSchema):
    """Marshmallow-схема для перегона модели в json формат."""

    class Meta:
        """Мета модели, вносятся доп. параметры."""

        model = HistoryEvents


class CmsProfileSchema(ma.ModelSchema):
    """Marshmallow-схема для перегона модели в json формат."""

    class Meta:
        """Мета модели, вносятся доп. параметры."""

        model = CmsUsers
        fields = (
            "login", "surname", "name", "patronymic", "email", "phone",
            "birth_date", "about_me", "socials", "photo", "roles"
        )
    roles = ma.Nested(CmsRolesSchema, many=True)
