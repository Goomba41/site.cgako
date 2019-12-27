#! env/bin/python3.6
# -*- coding: utf8 -*-

"""Представления API версии 0. Содержит следующие представления: Пользователи,
Новости"""

import jwt
import traceback
import uuid
#  import base64
import os
import math
import requests
import dateutil
from random import SystemRandom

from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from itsdangerous import TimedJSONWebSignatureSerializer
from sqlalchemy import func, extract
from sqlalchemy.orm import aliased
from sqlalchemy.orm.attributes import flag_modified
from urllib.parse import urljoin
from user_agents import parse
from flask import current_app, json, Blueprint, \
    request, Response, url_for, render_template
from flask_mail import Message
from functools import wraps


from app import bcrypt, db, mail
from app.models import CmsUsers, CmsUsersSchema, CmsProfileSchema, \
    CmsRoles, CmsRolesSchema, SystemObjects, SystemObjectsActions, \
    AssociationPermission, AssociationPermissionSchema, user_role, \
    CmsStructure, CmsStructureSchema, CmsOrganization, \
    CmsOrganizationSchema, CmsOrganizationBuildings, \
    CmsOrganizationBuildingsSchema, SitePages, SitePagesSchema, MenuSchema, \
    BannerSchema, AnnouncementsSchema, HistoryEvents, HistoryEventsSchema
from app.json_validation import profile_validator, password_validator, \
    user_validator, user_update_validator, role_validator, \
    role_update_validator, section_validator, section_update_validator, \
    organization_update_validator, organization_buildings_validator, \
    page_validator, page_update_validator, filepage_update_validator, \
    imagepage_update_validator

API0 = Blueprint('API0', __name__)

# ------------------------------------------------------------
# Декораторы
# ------------------------------------------------------------


def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()

        invalid_msg = {'type': 'error',
                       'text': 'Некорректный токен. '
                               'Требуется регистрация или переданы'
                               ' неверные аутентификационные данные.',
                       'authenticated': False}
        expired_msg = {'type': 'error',
                       'text': 'Токен просрочен. Аутентифицируйтесь заново.',
                       'authenticated': False}

        if len(auth_headers) != 2:
            response = Response(
                response=json.dumps(invalid_msg),
                status=401,
                mimetype='application/json'
            )
            return response

        try:
            token = auth_headers[1]
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            user = CmsUsers.query.filter_by(id=data['uid']).first()
            if not user:
                raise RuntimeError('User not found')
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            response = Response(
                response=json.dumps(expired_msg),
                status=401,
                mimetype='application/json'
            )
            return response
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            response = Response(
                response=json.dumps(invalid_msg),
                status=401,
                mimetype='application/json'
            )
            return response

    return _verify


# ------------------------------------------------------------
# Функции
# ------------------------------------------------------------

#  Генерация ответа сервера при ошибке
def server_error(dbg=None):
    """Вывод серверной ошибки с трейсом. Параметр dbg отвечает за вывод
    в формате traceback."""

    if dbg is not None:
        text = traceback.format_exc()
    else:
        text = "Серверная ошибка!"

    response = Response(
        response=json.dumps({'type': 'warning', 'text': text}),
        status=500,
        mimetype='application/json'
    )

    return response


#  Генерация токена подтверждения почты
def generate_confirmation_token(jdict, expiration=3600):
    """Генерация токена для подтверждения почты."""

    serializer = TimedJSONWebSignatureSerializer(
        current_app.config['SECRET_KEY'], expires_in=expiration)

    return serializer.dumps(
        jdict,
        salt=current_app.config['VERIFICATION_SALT'])


#  Проверка токена подтверждения почты
def confirm_email_token(token):
    """Верификация токена для подтверждения почты."""

    serializer = TimedJSONWebSignatureSerializer(
        current_app.config['SECRET_KEY'])

    try:
        email = serializer.loads(
            token,
            salt=current_app.config['VERIFICATION_SALT'],
        )
    except Exception:
        return (False, None)

    return (True, email)


#  Отправка письма
def send_email(to, subject, template):
    """Отправка электронных писем."""

    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )

    mail.send(msg)


#  Пагинация получаемого с API списка
def pagination_of_list(query_result, url, start, limit, q=None):
    """ Пагинация результатов запроса. Принимает параметры:
    результат запроса (json), URL API для генерации ссылок, стартовая позиция,
    количество выводимых записей"""

    records_count = len(query_result)

    if not isinstance(start, int):
        try:
            start = int(start)
        except ValueError:
            start = 1
    elif start < 1:
        start = 1

    if not isinstance(limit, int):
        try:
            limit = int(limit)
        except ValueError:
            limit = current_app.config['LIMIT']
    elif limit < 1:
        limit = current_app.config['LIMIT']

    if records_count < start:
        start = records_count

    response_obj = {}
    response_obj['start'] = start
    response_obj['limit'] = limit
    response_obj['count'] = records_count

    pages_count = math.ceil(records_count / limit)
    response_obj['pages'] = pages_count if pages_count > 0 else 1

    # Создаем URL на предыдущую страницу
    if start == 1:
        response_obj['previous'] = ''
    else:
        start_copy = max(1, start - limit)  # Странный просчет последней стр
        limit_copy = start - 1
        params = '?start=%d&limit=%d' % (start_copy, limit_copy)
        if q:
            params = params + '&q=%s' % (q)
        new_url = urljoin(url,
                          params)
        response_obj['previous'] = new_url
        print(new_url)

    # Создаем URL на следующую страницу
    if start + limit > records_count:
        response_obj['next'] = ''
    else:
        start_copy = start + limit
        params = '?start=%d&limit=%d' % (start_copy, limit)
        if q:
            params = params + '&q=%s' % (q)
        new_url = urljoin(url,
                          params)
        response_obj['next'] = new_url

    # Отсеивание результатов запроса
    response_obj['results'] = query_result[(start - 1):(start - 1 + limit)]

    return response_obj


#  Манипуляции с датой
def date_manipulation(value, action, period='month', number=3):
    if action == "plus":
        if period == 'day':
            return (value + relativedelta(days=number)).isoformat()
        elif period == 'week':
            return (value + relativedelta(weeks=number)).isoformat()
        elif period == 'month':
            return (value + relativedelta(months=number)).isoformat()
        elif period == 'year':
            return (value + relativedelta(years=number)).isoformat()
    elif action == "minus":
        if period == 'day':
            return (value - relativedelta(days=number)).isoformat()
        elif period == 'week':
            return (value - relativedelta(weeks=number)).isoformat()
        elif period == 'month':
            return (value - relativedelta(months=number)).isoformat()
        elif period == 'year':
            return (value - relativedelta(years=number)).isoformat()
    else:
        return value


#  Функция для преобразования
#  структуры сайта в json
def cat_to_json(item):
    return {
        'id': item.id,
        'name': item.title,
        'deletable': item.deletable,
        'editable': item.editable,
        'enabled': item.enabled,
        'addLeafNodeDisabled': True,
        'editNodeDisabled': not item.editable,
        'delNodeDisabled': not item.deletable,
        'level': item.level,
        'addLeafNodeDisabled': True if not item.appendable else False,
        'addTreeNodeDisabled': True if not item.appendable else False,
        'dragDisabled': True if not item.movable else False
    }


# Проверка размера файла
def get_fsize(fobj):
    if fobj.content_length:
        return fobj.content_length

    try:
        pos = fobj.tell()
        fobj.seek(0, 2)  # проход до конца
        size = fobj.tell()
        fobj.seek(pos)  # вернуться в начальную позицию
        return size
    except (AttributeError, IOError):
        pass

    # файлы в памяти, которые не поддерживают seeking или tell
    return 0  # предположим, что достаточно мал


#  Форматирование байтов в другие размеры
def formatBytes(fbytes, decimals=2, power=None):
    if (fbytes == 0):
        return {'number': 0, 'measure': 'B'}

    k = 1024
    if decimals < 0:
        dm = 0
    else:
        dm = decimals
    sizes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    i = 0

    if (power):
        i = power
    else:
        i = math.floor(math.log(fbytes) / math.log(k))

    return {'number': float(round(fbytes / (k ** i), dm)), 'measure': sizes[i]}


#  Генерация пароля с определенной длиной
#  Переделать под генерацию пароля с задаваемой длиной
def pass_generation(size=8):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    alphabet_upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numeric = '0123456789'
    special = '!@#$%^&*()_+~`|}{[]:;?><,./-='
    cryptogen = SystemRandom()

    character_set = alphabet + alphabet_upper + numeric + special

    password_symbols = ''.join(
        cryptogen.choice(character_set) for i in range(size-4))

    password_symbols += cryptogen.choice(alphabet)
    password_symbols += cryptogen.choice(alphabet_upper)
    password_symbols += cryptogen.choice(numeric)
    password_symbols += cryptogen.choice(special)

    password_symbols = list(map(str, password_symbols))

    #  // алгоритм Фишера-Йетса для перемешивания символов
    for i in range(len(password_symbols) - 1, 0, -1):
        j = math.floor(cryptogen.random() * (i + 1))
        temp = password_symbols[j]
        password_symbols[j] = password_symbols[i]
        password_symbols[i] = temp

    password = password_symbols = ''.join(password_symbols)

    return password


# ------------------------------------------------------------
# Логин
# ------------------------------------------------------------


@API0.route('/login', methods=['POST'])
def login():
    """Функция логина пользователя, создание JWT-токена"""

    try:
        login_data = request.get_json()
        client_ip = login_data.pop('ip', None)
        client_agent = login_data.pop('agent', None)

        user = CmsUsers.authenticate(**login_data)

        if not user[0]:

            response = Response(
                response=json.dumps({'type': 'error',
                                     'text': user[1],
                                     'field': user[2],
                                     'authenticated': False}),
                status=401,
                mimetype='application/json'
            )

            return response

        #  Проверка почт и изменение статуса активации, если время истекло
        #  и генерация и отсылка письма с токеном активации
        #  за неделю и в день истечения
        #  (проблема со спамом, необходимо определять
        #  отправлено ли письмо в этот день)
        for mail_item in user[0].email:
            if mail_item.get("value", None):
                activation_date = dateutil.parser.parse(
                                mail_item['activeUntil'])
                diff = (activation_date - datetime.now()).days
                if diff == 6 or diff == -1:
                    token = generate_confirmation_token(
                        {
                         "uid": user[0].id,
                         "value": mail_item['value'],
                         "type": mail_item['type']
                        }, expiration=3600)
                    confirm_url = 'http://192.168.0.89:8080/verify' \
                                  '/mail/' + token.decode("utf-8")
                    html = render_template(
                        'confirmation_mail.html',
                        confirm_url=confirm_url,
                        active_time="1 час")
                    subject = 'Подтверждение адреса электронной ' \
                              'почты в CMS сайта ЦГАКО'
                    print(subject)
                    print(mail_item)
                    send_email(mail_item['value'], subject, html)
                if diff <= 0:
                    mail_item['activeUntil'] = datetime.now().isoformat()
                    mail_item['verified'] = False
        #  -------------------------------------------------------------

        #  Проверка пароля и перегенерация, если время истекло
        #  и генерация и отсылка письма с токеном активации
        #  за неделю и в день истечения
        #  (проблема со спамом, необходимо определять
        #  отправлено ли письмо в этот день)
        pjson = user[0].password
        activation_date_pass = dateutil.parser.parse(
                        pjson['activeUntil'])
        diff = (activation_date_pass - datetime.now()).days
        if pjson['first_auth']:
            pjson['blocked'] = True
        if diff == 6:
            primary_mail = list(
                filter(
                    lambda mail: mail['type'] == "primary",
                    user[0].email)
                    )[0]["value"]
            html = render_template(
                'password_warning.html',
                email=primary_mail)
            subject = 'Окончание действия пароля ' \
                      'в CMS сайта ЦГАКО'
            for mail_item in user[0].email:
                send_email(mail_item['value'], subject, html)
        if diff <= 0:
            password = pass_generation(8)
            pjson['value'] = bcrypt.generate_password_hash(
                password).decode('utf-8')
            pjson['activeUntil'] = (
                datetime.now() + relativedelta(months=1)).isoformat()
            pjson['blocked'] = False
            pjson['first_auth'] = True
            primary_mail = list(
                filter(
                    lambda mail: mail['type'] == "primary",
                    user[0].email)
                    )[0]["value"]
            html = render_template(
                'password_change.html',
                password=password,
                login=user[0].login,
                email=primary_mail,)
            subject = 'Вам выдан новый пароль ' \
                      'в CMS сайта ЦГАКО'
            send_email(primary_mail, subject, html)

        #  -------------------------------------------------------------

        #  Генерация токена доступа для пользователя
        today = datetime.now()
        token_duration = current_app.config['TOKEN_DURATION']
        day_start = today.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(
                                        days=token_duration)

        token = jwt.encode({
                            'uid': user[0].id,
                            'iat': day_start,
                            'exp': day_end
                           },
                           current_app.config['SECRET_KEY'])

        last_login_data = {'datetime': today.isoformat()}
        #  -------------------------------------------------------------

        #  Получение данных о клиенте пользователя (ip, user-agent)
        if client_ip:
            last_login_data.update({'ip': client_ip})
        else:
            last_login_data.update(
                requests.get('https://api.ipify.org/?format=json').json())

        if client_agent:
            last_login_data.update({'agent': client_agent})
            user_agent = parse(client_agent)
            if user_agent.is_pc:
                device = 'pc'
            elif user_agent.is_mobile:
                device = 'mobile'
            elif user_agent.is_tablet:
                device = 'tablet'
            else:
                device = 'unknown'
            last_login_data.update({
                'browser': ('%s %s' % (user_agent.browser.family,
                                       user_agent.browser.version_string
                                       )).strip(),
                'os': ('%s %s' % (user_agent.os.family,
                                  user_agent.os.version_string)).strip(),
                'device': device,
            })
        else:
            last_login_data.update(
                {'agent': request.headers.get('User-Agent')})

        CmsUsers.query.filter_by(id=user[0].id).update(
            {'last_login': last_login_data,
             'email': user[0].email,
             'password': user[0].password})
        db.session.commit()
        #  -------------------------------------------------------------

        #  test = jwt.decode(token, current_app.config['SECRET_KEY'])
        #  print(test)
        #  print(datetime.utcfromtimestamp(test['iat']))
        #  print(datetime.utcfromtimestamp(test['exp']))

        response = Response(
            response=json.dumps(token.decode('utf-8')),
            status=200,
            mimetype='application/json'
        )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response

# ------------------------------------------------------------
# Верификация почты
# ------------------------------------------------------------


@API0.route('/verify/mail/<string:token>', methods=['GET'])
def verify_mail(token):
    """Функция верификации почты пользователя"""

    try:

        verified = confirm_email_token(token)

        if verified[0]:

            uid = verified[1].pop('uid', None)
            email = verified[1]

            user_emails = CmsUsers.query.filter(
                    (func.json_contains(CmsUsers.email, json.dumps(email))) &
                    (CmsUsers.id == uid)).first().email

            for mail_item in user_emails:
                if (mail_item['value'] == email['value'] and
                        mail_item['type'] == email['type']):
                    mail_item.update(
                        {'verified': True, 'activeUntil': date_manipulation(
                            datetime.now(), action="plus")})

            CmsUsers.query.filter_by(id=uid).update({'email': user_emails})
            db.session.commit()

            response = Response(
                response=json.dumps({'type': 'success',
                                     'text': 'Ваша почта подтверждена, '
                                     'спасибо!'}),
                status=200,
                mimetype='application/json'
            )
        else:
            response = Response(
                response=json.dumps({'type': 'danger',
                                     'text': 'Токен'
                                             ' поврежден или просрочен!'}),
                status=422,
                mimetype='application/json'
            )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response

# ------------------------------------------------------------
# Профиль вошедшего пользователя
# ------------------------------------------------------------


@API0.route('/profile/<int:uid>', methods=['GET'])
@token_required
def get_profile_by_id(current_user, uid):
    """ Получение профиля пользователя по id в json"""

    try:

        user_schema = CmsProfileSchema()
        user = CmsUsers.query.get(uid)
        udata = user_schema.dump(user)

        response = Response(
            response=json.dumps(udata.data),
            status=200,
            mimetype='application/json'
        )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


@API0.route('/profile/<int:uid>/data', methods=['PUT'])
@token_required
def update_profile_data(current_user, uid):
    """ Изменение данных пользователя через профиль"""

    try:

        update_data = request.get_json()

        #  Фото попать обязательно
        update_data.pop('photo', None)
        update_data.pop('roles', None)
        #  Не попать после реализации
        update_data.pop('socials', None)

        if not profile_validator.is_valid(update_data):
            errors = []
            for error in sorted(profile_validator.iter_errors(
                                update_data), key=str):
                errors.append(error.message)

            separator = '; '
            error_text = separator.join(errors)
            response = Response(
                    response=json.dumps({'type': 'danger',
                                         'text': error_text}),
                    status=422,
                    mimetype='application/json'
                )

        else:
            primary_mail = list(
                filter(
                    lambda mail: mail['type'] == "primary",
                    update_data['email'])
                    )[0]["value"]
            exist = CmsUsers.exist(sid=uid, **{
                                      'login': update_data['login'],
                                      'email': primary_mail,
                                      'phone': update_data['phone']
                                      })

            if exist:
                response = Response(
                    response=json.dumps({'type': 'danger',
                                         'text': 'Уже есть пользователь '
                                                 'с такими логином, '
                                                 'телефоном или почтой! '
                                                 'Выберите другие!'}),
                    status=422,
                    mimetype='application/json'
                )
            else:
                previous = CmsUsers.query.filter_by(id=uid).first().email
                current = update_data['email']
                pairs = zip(current, previous)

                changed = [x for x, y in pairs if x != y]
                if changed:
                    for mail_item in changed:
                        sended_date = dateutil.parser.parse(
                            mail_item['activeUntil'])
                        if sended_date <= datetime.now():
                            mail_item['activeUntil'] = date_manipulation(
                                datetime.now(), action="plus")
                        mail_item['verified'] = False
                        if mail_item['value']:
                            token = generate_confirmation_token(
                                {
                                 "uid": uid,
                                 "value": mail_item['value'],
                                 "type": mail_item['type']
                                }, expiration=3600)
                            confirm_url = 'http://192.168.0.89:8080/verify' \
                                          '/mail/' + token.decode("utf-8")
                            html = render_template(
                                'confirmation_mail.html',
                                confirm_url=confirm_url,
                                active_time="1 час")
                            subject = 'Подтверждение адреса электронной ' \
                                      'почты в CMS сайта ЦГАКО'
                            send_email(mail_item['value'], subject, html)

                CmsUsers.query.filter_by(id=uid).update(update_data)
                db.session.commit()

                response = Response(
                    response=json.dumps({'type': 'success',
                                         'text': 'Данные профиля обновлены!',
                                         'link': url_for('.get_profile_by_id',
                                                         uid=uid,
                                                         _external=True)}),
                    status=200,
                    mimetype='application/json'
                )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


@API0.route('/profile/<int:uid>/password', methods=['PUT'])
@token_required
def update_profile_password(current_user, uid):
    """ Изменение пароля через профиль пользователя"""

    try:

        update_data = request.get_json()

        if not password_validator.is_valid(update_data):
            errors = []
            for error in sorted(password_validator.iter_errors(
                                update_data), key=str):
                errors.append(error.message)

            separator = '; '
            error_text = separator.join(errors)
            response = Response(
                    response=json.dumps({'type': 'danger',
                                         'text': error_text}),
                    status=422,
                    mimetype='application/json'
                )
        else:

            auth_data = {'login': update_data['login'],
                         'password': update_data['passwordOld']}
            user = CmsUsers.authenticate(check=True, **auth_data)

            if not user[0]:

                response = Response(
                    response=json.dumps({'type': 'error',
                                         'text': user[1],
                                         'field': user[2]}),
                    status=401,
                    mimetype='application/json'
                )

            else:
                update_data.update(
                    passwordNew=bcrypt.generate_password_hash(
                        update_data['passwordNew']).decode('utf-8'))
                CmsUsers.query.filter_by(id=uid).update(
                    {
                        'password': {
                            "value": update_data['passwordNew'],
                            "blocked": False,
                            "first_auth": False,
                            "activeUntil": (datetime.now() + relativedelta(
                                months=1)).isoformat(),
                            "failed_times": 0
                        }
                    })
                db.session.commit()

                response = Response(
                    response=json.dumps({'type': 'success',
                                         'text': 'Успешно обновлен пароль!',
                                         'link': url_for('.get_profile_by_id',
                                                         uid=uid,
                                                         _external=True)}),
                    status=200,
                    mimetype='application/json'
                )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


@API0.route('/profile/<int:uid>/avatar', methods=['PUT'])
@API0.route('/users/<int:uid>/avatar', methods=['PUT'])
@token_required
def update_profile_avatar(current_user, uid):
    """ Изменение аватара пользователя"""

    try:
        usr_query = CmsUsers.query.filter_by(id=uid)

        if request.files.getlist('avatar'):

            if not len(request.files.getlist('avatar')) > 1:

                avatar_image = request.files['avatar']

                if avatar_image.content_type not in ['image/jpeg',
                                                     'image/png', 'image/gif']:
                    response = Response(
                        response=json.dumps({'type': 'danger',
                                             'text': 'Вы отправили'
                                                     'файл без расширения'
                                                     ' или это не изображение'
                                                     ' (jpeg, png, gif)!'}),
                        status=422,
                        mimetype='application/json'
                    )
                else:
                    if usr_query.first().photo:
                        img_extension = avatar_image.content_type.split('/')[1]
                        img_file_name = usr_query.first().photo.split(
                            '.')[0] + \
                            '.' + img_extension
                        avatar_filepath = os.path.join(
                            current_app.config['CMS_USERS_AVATARS'],
                            usr_query.first().photo)
                        if os.path.isfile(avatar_filepath):
                            os.remove(avatar_filepath)
                    else:
                        img_extension = avatar_image.content_type.split('/')[1]
                        img_file_name = uuid.uuid1().hex + '.' + img_extension

                    usr_query.update(
                        {'photo': img_file_name})
                    db.session.commit()

                    avatar_image.save(
                        os.path.join(
                            current_app.config['CMS_USERS_AVATARS'],
                            img_file_name))

                    response = Response(
                        response=json.dumps({'type': 'success',
                                             'text': 'Фотокарточка вклеена!',
                                             'link': url_for('.get_user_by_id',
                                                             uid=uid,
                                                             _external=True)}),
                        status=200,
                        mimetype='application/json'
                    )
            else:
                response = Response(
                    response=json.dumps({'type': 'danger',
                                         'text': 'Вы отправили'
                                                 'более 1 файла!'}),
                    status=422,
                    mimetype='application/json'
                )
        else:
            response = Response(
                response=json.dumps({'type': 'danger',
                                     'text': 'Вы не отправили'
                                             ' файла!'}),
                status=422,
                mimetype='application/json'
            )

        return response

        #  Запись файла в формате base64
        #  Могут возникнуть проблемы при пересылке base64 от клиента серверу
        #  потому что конвертирование файла в base64 строку
        #  увеличивает вес приблизительно на 33%
        #  img_data = update_data['avatarForm'].split(';')
        #  img_enc_string = img_data[1].split(',')[1]
        #  img_extension = img_data[0].split('/')[1]
        #  img_file_name = uuid.uuid1().hex + '.' + img_extension

        #  with open(img_file_name, "wb") as fh:
        #  fh.write(base64.decodebytes(
        #  bytes(img_enc_string, encoding='utf-8')
        #  ))

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


@API0.route('/profile/<int:uid>/avatar', methods=['DELETE'])
@API0.route('/users/<int:uid>/avatar', methods=['DELETE'])
@token_required
def delete_profile_avatar(current_user, uid):
    """ Удаление аватара пользователя"""

    try:
        usr_query = CmsUsers.query.filter_by(id=uid)

        if usr_query.first().photo:
            avatar_filepath = os.path.join(
                    current_app.config['CMS_USERS_AVATARS'],
                    usr_query.first().photo)
            if os.path.isfile(avatar_filepath):
                os.remove(avatar_filepath)
        usr_query.update({'photo': None})
        db.session.commit()

        response = Response(
                response=json.dumps({'type': 'success',
                                     'text': 'Фотокарточка вырезана!',
                                     'link': url_for('.get_profile_by_id',
                                                     uid=uid,
                                                     _external=True)}),
                status=200,
                mimetype='application/json'
            )

        return response

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


@API0.route('/profile/<int:uid>/mail/verify-send', methods=['GET'])
@token_required
def verify_mail_send(current_user, uid):
    """Отправка письма с подтверждением почты."""

    try:
        if request.args.get('value') and request.args.get('type'):

            user = CmsUsers.query.filter(
                (func.json_contains(CmsUsers.email, json.dumps(
                    {'value': request.args.get('value'),
                     'type': request.args.get('type')}))) &
                (CmsUsers.id == uid)).first()

            if user:

                token = generate_confirmation_token(
                    {
                     "uid": uid,
                     "value": request.args.get('value'),
                     "type": request.args.get('type')
                    }, expiration=86400)
                confirm_url = 'http://192.168.0.89:8080/verify' \
                              '/mail/' + token.decode("utf-8")
                html = render_template(
                    'confirmation_mail.html',
                    confirm_url=confirm_url,
                    active_time="1 день")
                subject = 'Подтверждение адреса электронной ' \
                          'почты в CMS сайта ЦГАКО'
                send_email(request.args.get('value'), subject, html)

                response = Response(
                    response=json.dumps({'type': 'success',
                                         'text': 'Письмо для подтверждения'
                                                 ' отправлено!'}),
                    status=200,
                    mimetype='application/json'
                )
            else:
                response = Response(
                    response=json.dumps({'type': 'danger',
                                         'text': 'У данного пользователя нет'
                                                 ' почты с такими'
                                                 ' параметрами!'}),
                    status=422,
                    mimetype='application/json'
                )
        else:
            response = Response(
                response=json.dumps({'type': 'danger',
                                     'text': 'Не отправлены требуемые'
                                             ' параметры: почта (value), '
                                             ' тип почты (type)!'}),
                status=422,
                mimetype='application/json'
            )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response

# ------------------------------------------------------------
# Администрирование пользователей
# ------------------------------------------------------------


@API0.route('/users', methods=['GET'])
@token_required
def get_users(current_user):
    """ Получение полного списка пользователей в json"""
    try:

        user_schema = CmsUsersSchema(many=True, exclude=['password'])

        users = CmsUsers.query.all()
        udata = user_schema.dump(users)
        udata = udata.data

        udata = pagination_of_list(
            udata,
            url_for('API0.get_users',
                    _external=True),
            start=request.args.get('start', 1),
            limit=request.args.get('limit',
                                   CmsUsers.query.count())
        )

        response = Response(
            response=json.dumps(udata),
            status=200,
            mimetype='application/json'
        )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


@API0.route('/users/<int:uid>', methods=['GET'])
@token_required
def get_user_by_id(current_user, uid):
    """ Получение одного пользователя по id в json"""

    try:
        user_schema = CmsUsersSchema(exclude=['password'])
        user = CmsUsers.query.get(uid)
        udata = user_schema.dump(user)

        response = Response(
            response=json.dumps(udata.data),
            status=200,
            mimetype='application/json'
        )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


@API0.route('/users', methods=['POST'])
@token_required
def post_users(current_user):
    """ Добавление записи пользователя в БД"""

    try:
        if CmsUsers.can(current_user.id, "post", "users"):

            post_data = request.get_json()

            if not user_validator.is_valid(post_data):
                errors = []
                for error in sorted(user_validator.iter_errors(
                                    post_data), key=str):
                    errors.append(error.message)

                separator = '; '
                error_text = separator.join(errors)

                response = Response(
                        response=json.dumps({'type': 'danger',
                                             'text': error_text}),
                        status=422,
                        mimetype='application/json'
                    )
            else:

                primary_mail = list(
                    filter(
                        lambda mail: mail['type'] == "primary",
                        post_data['email'])
                        )[0]["value"]

                exist = CmsUsers.exist(**{
                                          'login': post_data['login'],
                                          'email': primary_mail,
                                          'phone': post_data['phone']
                                          })

                if exist:
                    response = Response(
                        response=json.dumps({'type': 'danger',
                                             'text': 'Уже есть пользователь '
                                                     'с такими логином, '
                                                     'телефоном или основной '
                                                     'почтой!'}),
                        status=422,
                        mimetype='application/json'
                    )
                else:
                    user = CmsUsers(
                        login=post_data['login'],
                        password=post_data['password'],
                        name=post_data['name'],
                        surname=post_data['surname'],
                        patronymic=post_data['patronymic'],
                        birth_date=post_data['birth_date'],
                        email=post_data['email'],
                        phone=post_data['phone'],
                        about_me=post_data.get('about_me', None)
                    )

                    new_roles = post_data.pop('roles', None)

                    if new_roles is not None:
                        for role in new_roles:
                            #  Проверить, существует ли роль в базе,
                            #  если нет, то ничего
                            #  иначе добавить пользователю роль
                            role_exist = CmsRoles.query.filter_by(
                                id=role['id']).first()
                            if (role_exist is not None and
                                    role_exist.reassignable):
                                user.roles.append(role_exist)
                        if not user.roles:
                            user.roles.append(
                                CmsRoles.query.filter_by(id=4).first())
                    else:
                        user.roles.append(
                            CmsRoles.query.filter_by(id=4).first())

                    db.session.add(user)
                    db.session.commit()

                    password = post_data['password']
                    login = post_data['login']
                    additional_mails = []
                    for mail_item in post_data['email']:
                        if (mail_item['value'] and
                                mail_item['type'] != "primary"):
                            additional_mails.append(mail_item['value'])

                    token = generate_confirmation_token(
                        {
                         "uid": user.id,
                         "value": primary_mail,
                         "type": "primary"
                        }, expiration=3600)
                    confirm_url = 'http://192.168.0.89:8080/verify' \
                                  '/mail/' + token.decode("utf-8")
                    html = render_template(
                        'user_created.html',
                        confirm_url=confirm_url,
                        password=password,
                        login=login,
                        emails=additional_mails,
                        active_time="1 час")
                    subject = 'Для Вас создан пользователь ' \
                              'в CMS сайта ЦГАКО'
                    send_email(primary_mail, subject, html)

                    response = Response(
                        response=json.dumps({'type': 'success',
                                             'text': 'Добавлен пользователь '
                                                     '@'+str(user.login)+'!',
                                             'link': url_for('.get_user_by_id',
                                                             uid=user.id,
                                                             _external=True)}),
                        status=200,
                        mimetype='application/json'
                    )
        else:
            response = Response(
                response=json.dumps({'type': 'danger',
                                     'text': 'Доступ запрещен (403)'}),
                status=403,
                mimetype='application/json'
            )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


@API0.route('/users/<int:uid>', methods=['PUT'])
@token_required
def update_users(current_user, uid):
    """ Изменение записи пользователя в БД"""

    try:
        if CmsUsers.can(current_user.id, "put", "users"):

            update_data = request.get_json()

            if current_user.id == uid:
                response = Response(
                    response=json.dumps({'type': 'danger',
                                         'text': 'Воспользуйтесь профилем'
                                                 ' для изменения собственных'
                                                 ' данных!'}),
                    status=422,
                    mimetype='application/json'
                )
            else:
                #  Удаление лишних полей для валидации json
                for pop_item in [
                        'id', 'socials', 'photo', 'last_login', 'status']:
                    update_data.pop(pop_item, None)

                if not user_update_validator.is_valid(update_data):

                    errors = []
                    for error in sorted(user_update_validator.iter_errors(
                                        update_data), key=str):
                        errors.append(error.message)

                    separator = '; '
                    error_text = separator.join(errors)
                    response = Response(
                            response=json.dumps({'type': 'danger',
                                                 'text': error_text}),
                            status=422,
                            mimetype='application/json'
                        )

                else:
                    #  Получить основную почту из полученных данных
                    #  и проверить пользователя на существование
                    #  с такой почтой, логином, паролем
                    primary_mail = list(
                        filter(
                            lambda mail: mail['type'] == "primary",
                            update_data['email'])
                            )[0]["value"]
                    exist = CmsUsers.exist(sid=uid, **{
                                              'login': update_data['login'],
                                              'email': primary_mail,
                                              'phone': update_data['phone']
                                              })

                    if exist:
                        response = Response(
                            response=json.dumps(
                                {'type': 'danger',
                                 'text': 'Пользователь с такими'
                                         ' данными существует!'}),
                            status=422,
                            mimetype='application/json'
                        )
                    else:
                        #  Составить попарный список
                        #  предыдущих и полученных почт
                        previous = CmsUsers.query.filter_by(
                            id=uid).first().email
                        current = update_data['email']
                        pairs = zip(current, previous)

                        #  И проверить, если почта изменилась,
                        #  сбросить активацию и отправить письмо с токеном
                        changed = [x for x, y in pairs if x != y]
                        if changed:
                            for mail_item in changed:
                                sended_date = dateutil.parser.parse(
                                    mail_item['activeUntil'])
                                if sended_date <= datetime.now():
                                    mail_item[
                                        'activeUntil'] = date_manipulation(
                                            datetime.now(), action="plus")
                                mail_item['verified'] = False
                                if mail_item['value']:
                                    token = generate_confirmation_token(
                                        {
                                         "uid": uid,
                                         "value": mail_item['value'],
                                         "type": mail_item['type']
                                        }, expiration=3600)
                                    confirm_url = 'http://192.168.0.89:8080/' \
                                                  'verify/mail/' + \
                                                  token.decode(
                                                    "utf-8")
                                    html = render_template(
                                        'confirmation_mail.html',
                                        confirm_url=confirm_url,
                                        active_time="1 час")
                                    subject = 'Подтверждение адреса ' \
                                              'электронной почты в ' \
                                              'CMS сайта ЦГАКО'
                                    send_email(
                                        mail_item['value'], subject, html)

                        old_data = CmsUsers.query.filter_by(id=uid)
                        old_login = old_data.first().login

                        #  Обработка списка ролей
                        new_roles = update_data.pop('roles', None)

                        if new_roles is not None:
                            old_roles = old_data.first()

                            #  Просмотреть список ролей на наличие
                            #  непереназначаемых и сохранить только их
                            to_preserve = []
                            for role in old_roles.roles:
                                if not role.reassignable:
                                    to_preserve.append(role)
                            old_roles.roles = to_preserve

                            for role in new_roles:
                                #  Проверить, существует ли роль в базе,
                                #  и является ли переназначаемой
                                #  если нет, то ничего
                                #  иначе добавить пользователю роль
                                role_exist = CmsRoles.query.filter_by(
                                    id=role['id']).first()
                                if (role_exist is not None
                                        and role_exist.reassignable):
                                    old_roles.roles.append(role_exist)
                            if not old_roles.roles:
                                old_roles.roles.append(
                                    CmsRoles.query.filter_by(id=4).first())

                        old_data.update(update_data)
                        db.session.commit()

                        response = Response(
                            response=json.dumps(
                                {'type': 'success',
                                 'text': 'Изменен пользователь '
                                         '@'+str(old_login)+'!',
                                 'link': url_for('.get_user_by_id',
                                                 uid=uid,
                                                 _external=True)}),
                            status=200,
                            mimetype='application/json'
                        )
        else:
            response = Response(
                response=json.dumps({'type': 'danger',
                                     'text': 'Доступ запрещен (403)'}),
                status=403,
                mimetype='application/json'
            )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


@API0.route('/users/<int:uid>', methods=['DELETE'])
@token_required
def delete_users(current_user, uid):
    """ Удаление записи пользователя из БД"""

    try:
        if CmsUsers.can(current_user.id, "delete", "users"):

            user = CmsUsers.query.get(uid)

            if user.photo:
                os.remove(os.path.join(
                    current_app.config['CMS_USERS_AVATARS'],
                    user.photo))

            db.session.delete(user)
            db.session.commit()

            response = Response(
                response=json.dumps({'type': 'success',
                                     'text': 'Успешно удалено!'}),
                status=200,
                mimetype='application/json'
            )
        else:
            response = Response(
                response=json.dumps({'type': 'danger',
                                     'text': 'Доступ запрещен (403)'}),
                status=403,
                mimetype='application/json'
            )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


@API0.route('/users/<int:uid>/mail/verify-reset', methods=['GET'])
@token_required
def verify_mail_reset(current_user, uid):
    """Сброс активации почты пользователя"""

    try:
        if request.args.get('value') and request.args.get('type'):

            user = CmsUsers.query.filter(
                (func.json_contains(CmsUsers.email, json.dumps(
                    {'value': request.args.get('value'),
                     'type': request.args.get('type')}))) &
                (CmsUsers.id == uid)).first()

            if user:
                for mail_item in user.email:
                    if (mail_item['value'] == request.args.get('value') and
                            mail_item['type'] == request.args.get('type')):
                        mail_item['verified'] = False
                CmsUsers.query.filter_by(id=uid).update({"email": user.email})
                db.session.commit()

                response = Response(
                    response=json.dumps({'type': 'success',
                                         'text': 'Активация электронного'
                                                 ' адреса успешно сброшена!'}),
                    status=200,
                    mimetype='application/json'
                )
            else:
                response = Response(
                    response=json.dumps({'type': 'danger',
                                         'text': 'У данного пользователя нет'
                                                 ' почты с такими'
                                                 ' параметрами!'}),
                    status=422,
                    mimetype='application/json'
                )
        else:
            response = Response(
                response=json.dumps({'type': 'danger',
                                     'text': 'Не отправлены требуемые'
                                             ' параметры: почта (value), '
                                             ' тип почты (type)!'}),
                status=422,
                mimetype='application/json'
            )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


@API0.route('/users/<int:uid>/password/block', methods=['GET'])
@token_required
def users_password_block(current_user, uid):
    """Блокирование пароля пользователя"""

    try:
        if CmsUsers.can(current_user.id, "put", "users"):

            user = CmsUsers.query.filter(CmsUsers.id == uid).first()

            if user:
                user.password['blocked'] = True
                CmsUsers.query.filter_by(id=uid).update(
                    {"password": user.password})
                db.session.commit()

                response = Response(
                    response=json.dumps({'type': 'success',
                                         'text': 'Пароль пользователя успешно'
                                                 ' заблокирован!'}),
                    status=200,
                    mimetype='application/json'
                )
            else:
                response = Response(
                    response=json.dumps({'type': 'danger',
                                         'text': 'Пользователь не найден!'}),
                    status=422,
                    mimetype='application/json'
                )
        else:
            response = Response(
                response=json.dumps({'type': 'danger',
                                     'text': 'Доступ запрещен (403)'}),
                status=403,
                mimetype='application/json'
            )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


@API0.route('/users/<int:uid>/password/reset', methods=['GET'])
@token_required
def users_password_reset(current_user, uid):
    """Блокирование пароля пользователя"""

    try:
        if CmsUsers.can(current_user.id, "put", "users"):

            user = CmsUsers.query.filter(CmsUsers.id == uid).first()

            if user:

                password = pass_generation(8)
                user.password['value'] = bcrypt.generate_password_hash(
                    password).decode('utf-8')
                user.password['activeUntil'] = (
                    datetime.now() + relativedelta(months=1)).isoformat()
                user.password['blocked'] = False
                user.password['first_auth'] = True

                CmsUsers.query.filter_by(id=uid).update(
                    {"password": user.password})
                db.session.commit()

                primary_mail = list(
                    filter(
                        lambda mail: mail['type'] == "primary",
                        user.email)
                        )[0]["value"]
                html = render_template(
                    'password_change.html',
                    password=password,
                    login=user.login,
                    email=primary_mail,)
                subject = 'Вам выдан новый пароль ' \
                          'в CMS сайта ЦГАКО'
                send_email(primary_mail, subject, html)

                response = Response(
                    response=json.dumps(
                        {'type': 'success',
                         'text': 'Пароль пользователя успешно'
                                 ' сброшен! Авторизацонные данные'
                                 ' высланы на почту!'}),
                    status=200,
                    mimetype='application/json'
                )
            else:
                response = Response(
                    response=json.dumps({'type': 'danger',
                                         'text': 'Пользователь не найден!'}),
                    status=422,
                    mimetype='application/json'
                )
        else:
            response = Response(
                response=json.dumps({'type': 'danger',
                                     'text': 'Доступ запрещен (403)'}),
                status=403,
                mimetype='application/json'
            )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response

# ------------------------------------------------------------
# Роли
# ------------------------------------------------------------


@API0.route('/roles', methods=['GET'])
@token_required
def get_roles(current_user):
    """ Получение полного списка ролей в json"""

    try:
        role_schema = CmsRolesSchema(many=True, exclude=['users'])

        roles = CmsRoles.query.all()
        rdata = role_schema.dump(roles)
        rdata = rdata.data

        rdata = pagination_of_list(
            rdata,
            url_for('API0.get_roles',
                    _external=True),
            start=request.args.get('start', 1),
            limit=request.args.get('limit',
                                   CmsRoles.query.count())
        )

        response = Response(
            response=json.dumps(rdata),
            status=200,
            mimetype='application/json'
        )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


@API0.route('/roles/<int:rid>', methods=['GET'])
@token_required
def get_role_by_id(current_user, rid):
    """ Получение одной роли по id в json"""

    try:

        role_schema = CmsRolesSchema(exclude=['users'])
        roles = CmsRoles.query.get(rid)
        rdata = role_schema.dump(roles)

        response = Response(
            response=json.dumps(rdata.data),
            status=200,
            mimetype='application/json'
        )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


@API0.route('/roles/<int:rid>', methods=['DELETE'])
@token_required
def delete_roles(current_user, rid):
    """ Удаление записи роли из БД"""

    try:
        if CmsUsers.can(current_user.id, "delete", "roles"):

            role = CmsRoles.query.get(rid)

            if role.deletable:
                db.session.delete(role)

                #  После удаления роли запросить пользователей без ролей
                #  если есть, добавить обозначенную роль
                uwr = CmsUsers.query.filter(CmsUsers.roles == None).all() # noqa: ignore=E711
                if uwr:
                    # Пользователь (придумать 'по умолчанию")
                    base_role = CmsRoles.query.get(4)
                    for u in uwr:
                        u.roles.append(base_role)

                db.session.commit()

                response = Response(
                    response=json.dumps({'type': 'success',
                                         'text': 'Успешно удалено!'}),
                    status=200,
                    mimetype='application/json'
                )
            else:
                response = Response(
                    response=json.dumps({'type': 'danger',
                                         'text': 'Эту роль нельзя удалить!'}),
                    status=401,
                    mimetype='application/json'
                )
        else:
            response = Response(
                response=json.dumps({'type': 'danger',
                                     'text': 'Доступ запрещен (403)'}),
                status=403,
                mimetype='application/json'
            )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


@API0.route('/roles', methods=['POST'])
@token_required
def post_role(current_user):
    """ Добавление записи пользователя в БД"""

    try:
        if CmsUsers.can(current_user.id, "post", "roles"):

            post_data = request.get_json()

            if not role_validator.is_valid(post_data):
                errors = []
                for error in sorted(role_validator.iter_errors(
                                    post_data), key=str):
                    errors.append(error.message)

                separator = '; '
                error_text = separator.join(errors)

                response = Response(
                        response=json.dumps({'type': 'danger',
                                             'text': error_text}),
                        status=422,
                        mimetype='application/json'
                    )
            else:

                exist = CmsRoles.exist(**{
                                          'title': post_data['title']
                                          })

                if exist:
                    response = Response(
                        response=json.dumps({'type': 'danger',
                                             'text': 'Уже есть такая роль!'}),
                        status=422,
                        mimetype='application/json'
                    )
                else:
                    role = CmsRoles(
                        title=post_data['title'],
                    )

                    new_permissions = post_data.pop('permissions', None)

                    if new_permissions is not None:
                        for permission in new_permissions:
                            permission_exist = \
                                AssociationPermission.query.filter_by(
                                    id=permission['id']).first()
                            if permission_exist is not None:
                                role.permissions.append(permission_exist)

                    db.session.add(role)
                    db.session.commit()

                    response = Response(
                        response=json.dumps({'type': 'success',
                                             'text': 'Добавлена роль '
                                                     '«'+str(role.title)+'»!',
                                             'link': url_for('.get_role_by_id',
                                                             rid=role.id,
                                                             _external=True)}),
                        status=200,
                        mimetype='application/json'
                    )
        else:
            response = Response(
                response=json.dumps({'type': 'danger',
                                     'text': 'Доступ запрещен (403)'}),
                status=403,
                mimetype='application/json'
            )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


@API0.route('/roles/<int:rid>', methods=['PUT'])
@token_required
def update_roles(current_user, rid):
    """ Изменение записи системной роли в БД"""

    try:
        if CmsUsers.can(current_user.id, "put", "roles"):

            update_data = request.get_json()
            print(update_data)
            for key in list(update_data.keys()):
                if key not in ['title', 'permissions']:
                    del update_data[key]
            print(update_data)

            exist_req = CmsRoles.exist(**{
                                      'id': rid
                                    })

            if not exist_req:
                response = Response(
                    response=json.dumps(
                        {'type': 'danger',
                         'text': 'Такой роли'
                                 ' не существует!'}),
                    status=422,
                    mimetype='application/json'
                )
            else:
                role = CmsRoles.query.filter_by(id=rid)

                if not role.first().editable:
                    response = Response(
                        response=json.dumps(
                            {'type': 'danger',
                             'text': 'Роль нельзя'
                                     ' изменять!'}),
                        status=422,
                        mimetype='application/json'
                    )
                else:

                    if not role_update_validator.is_valid(update_data):
                        errors = []
                        for error in sorted(role_update_validator.iter_errors(
                                            update_data), key=str):
                            errors.append(error.message)

                        separator = '; '
                        error_text = separator.join(errors)
                        response = Response(
                                response=json.dumps({'type': 'danger',
                                                     'text': error_text}),
                                status=422,
                                mimetype='application/json'
                            )

                    else:

                        exist = CmsRoles.exist(rid=rid, **{
                                                  'title': update_data['title']
                                                  })

                        if exist:
                            response = Response(
                                response=json.dumps(
                                    {'type': 'danger',
                                     'text': 'Другая роль с таким'
                                             ' именем существует!'}),
                                status=422,
                                mimetype='application/json'
                            )
                        else:
                            old_title = role.first().title

                            new_permissions = update_data.pop(
                                'permissions', None)

                            if new_permissions is not None:
                                old_permissions = role.first()
                                old_permissions.permissions.clear()
                                for permission in new_permissions:
                                    permission_exist = \
                                        AssociationPermission.query.filter_by(
                                            id=permission['id']).first()
                                    if permission_exist is not None:
                                        old_permissions.permissions.append(
                                            permission_exist)

                            role.update(update_data)
                            db.session.commit()

                            response = Response(
                                response=json.dumps(
                                    {'type': 'success',
                                     'text': 'Изменена роль '
                                             '«'+str(old_title)+'»!',
                                     'link': url_for('.get_role_by_id',
                                                     rid=rid,
                                                     _external=True)}),
                                status=200,
                                mimetype='application/json'
                            )

        else:
            response = Response(
                response=json.dumps({'type': 'danger',
                                     'text': 'Доступ запрещен (403)'}),
                status=403,
                mimetype='application/json'
            )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


# ------------------------------------------------------------
# Разрешения
# ------------------------------------------------------------


@API0.route('/permissions', methods=['GET'])
@token_required
def get_permissions(current_user):
    """ Получение списка разрешений в json"""

    try:
        permission_schema = AssociationPermissionSchema(many=True)
        permissions = AssociationPermission.query.all()
        pdata = permission_schema.dump(permissions)
        pdata = pdata.data

        response = Response(
            response=json.dumps(pdata),
            status=200,
            mimetype='application/json'
        )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


# ------------------------------------------------------------
# Структура
# ------------------------------------------------------------


@API0.route('/structure', methods=['GET'])
@token_required
def get_structure(current_user):
    """ Получение структуры сайта в json"""

    try:

        if request.args.get("end"):
            structure_schema = CmsStructureSchema(many=True)
            structure_ends = CmsStructure.query.filter(
                CmsStructure.left == (CmsStructure.right - 1)).all()
            structure_ends_filtered = []
            for item in structure_ends:
                if not item.pages.all() and item.page_adding or item.id == 54:
                    structure_ends_filtered.append(item)
            sdata = structure_schema.dump(structure_ends_filtered)
            sdata = sdata.data

            response = Response(
                response=json.dumps(sdata),
                status=200,
                mimetype='application/json'
            )
        else:
            structure = CmsStructure.query.filter(CmsStructure.id == 1).first()
            response = Response(
                response=json.dumps(
                    structure.drilldown_tree(
                        json=True, json_fields=cat_to_json)[0]),
                status=200,
                mimetype='application/json'
            )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


#  Функция для меню в json
def menu_json(item):
    schema = MenuSchema()
    #  permissions = AssociationPermission.query.all()
    #  if item.pages.all():
    data = schema.dump(item)
    #  print(data.data)
    #  print(item.pages.all())
    return data.data


@API0.route('/menu', methods=['GET'])
def get_structure_open():
    """ Получение структуры сайта в json открытая"""
    try:

        structure = CmsStructure.query.filter(CmsStructure.id == 1).first()
        tree = json.dumps(
            structure.drilldown_tree(
                json=True, json_fields=menu_json)[0])
        #  print(tree)

        response = Response(
            response=tree,
            status=200,
            mimetype='application/json'
        )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


@API0.route('/structure/<int:sid>', methods=['DELETE'])
@token_required
def delete_structure(current_user, sid):
    """ Удаление раздела из структуры сайта"""

    try:
        if CmsUsers.can(current_user.id, "delete", "structure"):
            section = CmsStructure.query.filter(CmsStructure.id == sid).first()
            if section:
                print(section.deletable)
                if not section.deletable:
                    response = Response(
                        response=json.dumps({'type': 'danger',
                                             'text': 'Этот раздел '
                                             'нельзя удалять!'}),
                        status=422,
                        mimetype='application/json'
                    )
                else:
                    db.session.delete(section)
                    db.session.commit()
                    response = Response(
                        response=json.dumps({'type': 'success',
                                             'text': 'Успешно удалено!'}),
                        status=200,
                        mimetype='application/json'
                    )
            else:
                response = Response(
                    response=json.dumps({'type': 'danger',
                                         'text': 'Запись не найдена! (404)'}),
                    status=404,
                    mimetype='application/json'
                )
        else:
            response = Response(
                response=json.dumps({'type': 'danger',
                                     'text': 'Доступ запрещен (403)'}),
                status=403,
                mimetype='application/json'
            )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


@API0.route('/structure', methods=['POST'])
@token_required
def post_structure(current_user):
    """ Добавление раздела в структуру сайта"""

    try:
        if CmsUsers.can(current_user.id, "post", "structure"):
            post_data = request.get_json()

            for key in list(post_data.keys()):
                if key not in ['pid', 'name', 'enabled']:
                    del post_data[key]

            if not section_validator.is_valid(post_data):
                errors = []
                for error in sorted(section_validator.iter_errors(
                                    post_data), key=str):
                    errors.append(error.message)

                separator = '; '
                error_text = separator.join(errors)

                response = Response(
                        response=json.dumps({'type': 'danger',
                                             'text': error_text}),
                        status=422,
                        mimetype='application/json'
                    )
            else:

                exist = CmsStructure.exist(**{
                                          'id': post_data['pid']
                                          })
                if not exist:
                    response = Response(
                        response=json.dumps({'type': 'danger',
                                             'text': 'Такой родительский '
                                                     'раздел не существует!'}),
                        status=422,
                        mimetype='application/json'
                    )
                else:
                    new_section = CmsStructure(
                        parent_id=post_data['pid'],
                        enabled=post_data['enabled'],
                        title=post_data['name'],
                    )

                    db.session.add(new_section)
                    db.session.commit()

                    response = Response(
                        response=json.dumps(
                            {'type': 'success',
                             'text': 'Добавлен раздел '
                                     '«'+str(new_section.title)+'»!',
                             'link': url_for('.get_structure',
                                             _external=True)}),
                        status=200,
                        mimetype='application/json'
                    )
        else:
            response = Response(
                response=json.dumps({'type': 'danger',
                                     'text': 'Доступ запрещен (403)'}),
                status=403,
                mimetype='application/json'
            )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


@API0.route('/structure/<int:sid>', methods=['PUT'])
@token_required
def update_structure(current_user, sid):
    """ Добавление раздела в структуру сайта"""

    try:
        if CmsUsers.can(current_user.id, "put", "structure"):

            exist = CmsStructure.exist(**{
                                      'id': sid
                                      })

            if not exist:

                response = Response(
                    response=json.dumps(
                        {'type': 'danger',
                         'text': 'Такого раздела'
                                 ' не существует!'}),
                    status=422,
                    mimetype='application/json'
                )

            else:

                structure = CmsStructure.query.filter(
                    CmsStructure.id == sid).first()

                if not structure.editable:
                    response = Response(
                        response=json.dumps(
                            {'type': 'danger',
                             'text': 'Раздел нельзя'
                                     ' изменять!'}),
                        status=422,
                        mimetype='application/json'
                    )
                else:

                    update_data = request.get_json()

                    for key in list(update_data.keys()):
                        if key not in ['name', 'enabled']:
                            del update_data[key]

                    if not section_update_validator.is_valid(update_data):
                        errors = []
                        for error in sorted(
                            section_update_validator.iter_errors(
                                update_data), key=str):
                            errors.append(error.message)

                        separator = '; '
                        error_text = separator.join(errors)
                        response = Response(
                                response=json.dumps({'type': 'danger',
                                                     'text': error_text}),
                                status=422,
                                mimetype='application/json'
                            )
                    else:
                        structure_name_old = structure.title

                        structure.title = update_data['name']
                        structure.enabled = update_data['enabled']

                        db.session.add(structure)
                        db.session.commit()

                        response = Response(
                            response=json.dumps(
                                {'type': 'success',
                                 'text': 'Отредактирован раздел '
                                         '«'+str(structure_name_old)+'»!',
                                 'link': url_for('.get_structure',
                                                 _external=True)}),
                            status=200,
                            mimetype='application/json'
                        )

        else:
            response = Response(
                response=json.dumps({'type': 'danger',
                                     'text': 'Доступ запрещен (403)'}),
                status=403,
                mimetype='application/json'
            )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


@API0.route('/structure/<int:sid>/parent/<int:pid>', methods=['PUT'])
@token_required
def update_parent_structure(current_user, sid, pid):
    """ Добавление раздела в структуру сайта"""

    try:
        if CmsUsers.can(current_user.id, "put", "structure"):
            if pid == sid:
                response = Response(
                    response=json.dumps({'type': 'danger',
                                         'text': 'Нельзя переносить '
                                                 'раздел сам в себя!'}),
                    status=422,
                    mimetype='application/json'
                )
            else:
                parent_exist = CmsStructure.exist(**{
                                          'id': pid
                                          })
                section_exist = CmsStructure.exist(**{
                                          'id': sid
                                          })

                if not (parent_exist and section_exist):
                    if not parent_exist:
                        text = 'Такой родительский раздел не существует!'
                    else:
                        text = 'Такой раздел не существует!'
                        response = Response(
                            response=json.dumps({'type': 'danger',
                                                 'text': text}),
                            status=422,
                            mimetype='application/json'
                        )
                else:
                    section = CmsStructure.query.filter(
                        CmsStructure.id == sid).one()
                    section.parent_id = pid
                    db.session.add(section)
                    db.session.commit()

                    response = Response(
                        response=json.dumps(
                            {'type': 'success',
                             'text': 'Перенесён раздел '
                                     '«'+str(section.title)+'»!',
                             'link': url_for('.get_structure',
                                             _external=True)}),
                        status=200,
                        mimetype='application/json'
                    )
        else:
            response = Response(
                response=json.dumps({'type': 'danger',
                                     'text': 'Доступ запрещен (403)'}),
                status=403,
                mimetype='application/json'
            )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


# ------------------------------------------------------------
# Контакты и информация об организации
# ------------------------------------------------------------


@API0.route('/organization', methods=['GET'])
@token_required
def get_organization(current_user):
    """ Информация об организации в json. """

    try:

        organization = CmsOrganization.query.first()
        organization_schema = CmsOrganizationSchema()

        odata = organization_schema.dump(organization)
        odata = odata.data

        response = Response(
            response=json.dumps(odata),
            status=200,
            mimetype='application/json'
        )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


@API0.route('/contacts', methods=['GET'])
def get_organization_open():
    """ Информация об организации в json. """

    try:
        organization = CmsOrganization.query.first()
        organization_schema = CmsOrganizationSchema()

        odata = organization_schema.dump(organization)
        odata = odata.data

        response = Response(
            response=json.dumps(odata),
            status=200,
            mimetype='application/json'
        )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


@API0.route('/organization', methods=['PUT'])
@token_required
def update_organization(current_user):
    """ Обновление информации об организации. """

    try:
        if CmsUsers.can(current_user.id, "put", "contacts"):

            organization = CmsOrganization.query.first()

            update_data = request.get_json()

            for key in list(update_data.keys()):
                if key not in ['company_name', 'full_company_name',
                               'requisites']:
                    del update_data[key]
            if not organization_update_validator.is_valid(update_data):
                errors = []
                for error in sorted(
                    organization_update_validator.iter_errors(
                        update_data), key=str):
                    errors.append(error.message)

                separator = '; '
                error_text = separator.join(errors)
                response = Response(
                        response=json.dumps({'type': 'danger',
                                             'text': error_text}),
                        status=422,
                        mimetype='application/json'
                    )
            else:
                organization_name_old = organization.company_name

                organization.company_name = update_data['company_name']
                organization.full_company_name = update_data[
                    'full_company_name']
                if 'requisites' in update_data:
                    organization.requisites = update_data['requisites']

                db.session.add(organization)
                db.session.commit()

                response = Response(
                    response=json.dumps(
                        {'type': 'success',
                         'text': 'Отредактирована основная '
                                 'информация организации '
                                 + str(organization_name_old) + '!',
                         'link': url_for('.get_organization',
                                         _external=True)}),
                    status=200,
                    mimetype='application/json'
                )
        else:
            response = Response(
                response=json.dumps({'type': 'danger',
                                     'text': 'Доступ запрещен (403)'}),
                status=403,
                mimetype='application/json'
            )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


@API0.route('/organization/buildings', methods=['GET'])
@token_required
def get_organization_buildings(current_user):
    """ Получение информации о зданиях организации в json."""

    try:

        organization_buildings = CmsOrganization.query.first().buildings.all()
        organization_buildings_schema = CmsOrganizationBuildingsSchema(
            many=True)

        obdata = organization_buildings_schema.dump(organization_buildings)
        obdata = obdata.data

        response = Response(
            response=json.dumps(obdata),
            status=200,
            mimetype='application/json'
        )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


@API0.route('/organization/buildings', methods=['POST'])
@token_required
def post_organization_buildings(current_user):
    """ Добавление раздела в структуру сайта"""

    try:
        if CmsUsers.can(current_user.id, "post", "contacts"):
            post_data = request.get_json()

            for key in list(post_data.keys()):
                if key not in ['name', 'road_map']:
                    del post_data[key]

            if not organization_buildings_validator.is_valid(post_data):
                errors = []
                for error in sorted(
                        organization_buildings_validator.iter_errors(
                            post_data), key=str):
                    errors.append(error.message)

                separator = '; '
                error_text = separator.join(errors)

                response = Response(
                        response=json.dumps({'type': 'danger',
                                             'text': error_text}),
                        status=422,
                        mimetype='application/json'
                    )
            else:
                new_building = CmsOrganizationBuildings(
                    name=post_data['name'],
                    road_map=post_data['road_map']
                )
                db.session.add(new_building)
                db.session.commit()

                response = Response(
                    response=json.dumps(
                        {'type': 'success',
                         'text': 'Добавлено здание '
                                 '«'+str(new_building.name)+'»!',
                         'link': url_for('.get_structure',
                                         _external=True)}),
                    status=200,
                    mimetype='application/json'
                )
        else:
            response = Response(
                response=json.dumps({'type': 'danger',
                                     'text': 'Доступ запрещен (403)'}),
                status=403,
                mimetype='application/json'
            )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


@API0.route('/organization/buildings/<int:bid>', methods=['PUT'])
@token_required
def update_organization_building(current_user, bid):
    """ Обновление информации о здании организации. """

    try:
        if CmsUsers.can(current_user.id, "put", "contacts"):

            building = CmsOrganizationBuildings.query.get(bid)

            if not building:
                response = Response(
                    response=json.dumps({'type': 'danger',
                                         'text': 'Такое здание '
                                                 'не существует!'}),
                    status=422,
                    mimetype='application/json'
                )
            else:

                update_data = request.get_json()

                for key in list(update_data.keys()):
                    if key not in [
                            'name', 'road_map', 'work_time',
                            'employee_contacts']:
                        del update_data[key]

                for item in update_data['employee_contacts']:
                    if not item.get('cid', None):
                        item.update({'cid': str(uuid.uuid4())})

                if not organization_buildings_validator.is_valid(update_data):
                    errors = []
                    for error in sorted(
                        organization_buildings_validator.iter_errors(
                            update_data), key=str):
                        errors.append(error.message)

                    separator = '; '
                    error_text = separator.join(errors)
                    response = Response(
                            response=json.dumps({'type': 'danger',
                                                 'text': error_text}),
                            status=422,
                            mimetype='application/json'
                        )
                else:
                    building_name_old = building.name

                    previous = building.employee_contacts
                    current = update_data['employee_contacts']
                    diff = [item for item in previous if item not in current]
                    if diff:
                        for item in diff:
                            if bool(item.get("photo")):
                                photo_filepath = os.path.join(
                                    current_app.config['CMS_EMPLOYEE_PHOTOS'],
                                    item.get("photo"))
                                if os.path.isfile(photo_filepath):
                                    print(photo_filepath)
                                    os.remove(photo_filepath)

                    building.name = update_data['name']
                    building.road_map = update_data['road_map']
                    if 'work_time' in update_data:
                        building.work_time = update_data['work_time']
                    if 'employee_contacts' in update_data:
                        building.employee_contacts = update_data[
                            'employee_contacts']

                    db.session.add(building)
                    db.session.commit()

                    response = Response(
                        response=json.dumps(
                            {'type': 'success',
                             'text': 'Отредактирована информация '
                                     'о здании «'
                                     + str(building_name_old) + '»!',
                             'link': url_for('.get_organization_buildings',
                                             _external=True)}),
                        status=200,
                        mimetype='application/json'
                    )
        else:
            response = Response(
                response=json.dumps({'type': 'danger',
                                     'text': 'Доступ запрещен (403)'}),
                status=403,
                mimetype='application/json'
            )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


@API0.route(
    '/organization/buildings/<int:bid>/contacts/<string:cid>/photo',
    methods=['PUT'])
@token_required
def update_organization_building_conph(current_user, bid, cid):
    """ Обновление фото контакта здания """

    try:
        if CmsUsers.can(current_user.id, "put", "contacts"):

            building = CmsOrganizationBuildings.query.get(bid)

            if not building:
                response = Response(
                    response=json.dumps({'type': 'danger',
                                         'text': 'Такое здание '
                                                 'не существует!'}),
                    status=422,
                    mimetype='application/json'
                )
            else:
                if not any(
                        (
                        contact.get(
                            'cid', None) == cid
                        ) for contact in building.employee_contacts):
                    response = Response(
                        response=json.dumps(
                            {'type': 'danger',
                             'text': 'Такой контакт сотрудника '
                             'не существует!'}),
                        status=422,
                        mimetype='application/json'
                    )
                else:

                    if request.files.getlist('employee_photo'):

                        if not len(
                                request.files.getlist(
                                        'employee_photo')) > 1:

                            image = request.files['employee_photo']

                            if image.content_type not in [
                                    'image/jpeg', 'image/png', 'image/gif']:
                                response = Response(
                                    response=json.dumps(
                                        {'type': 'danger',
                                         'text': 'Вы отправили'
                                                 'файл без расширения'
                                                 ' или это не изображение'
                                                 ' (jpeg, png, gif)!'}),
                                    status=422,
                                    mimetype='application/json'
                                )
                            else:
                                c_data = [contact for contact in building.employee_contacts if contact.get('cid', None) == cid][0] # noqa: ignore=E501
                                if bool(c_data.get("photo")):
                                    img_extension = image.content_type.split(
                                        '/')[1]
                                    img_file_name = c_data.get("photo").split(
                                        '.')[0] + '.' + img_extension
                                    photo_filepath = os.path.join(
                                        current_app.config[
                                            'CMS_EMPLOYEE_PHOTOS'],
                                        c_data.get("photo"))
                                    if os.path.isfile(photo_filepath):
                                        os.remove(photo_filepath)
                                else:
                                    img_extension = image.content_type.split(
                                        '/')[1]
                                    img_file_name = uuid.uuid1(
                                        ).hex + '.' + img_extension

                                c_data.update(
                                    {'photo': img_file_name})
                                flag_modified(building, 'employee_contacts')
                                db.session.commit()

                                image.save(
                                    os.path.join(
                                        current_app.config[
                                            'CMS_EMPLOYEE_PHOTOS'],
                                        img_file_name)
                                )

                                response = Response(
                                    response=json.dumps(
                                        {'type': 'success',
                                         'text': 'Фото изменено!'}),
                                    status=200,
                                    mimetype='application/json'
                                )
                        else:
                            response = Response(
                                response=json.dumps(
                                    {'type': 'danger',
                                     'text': 'Вы отправили'
                                     'более 1 файла!'}),
                                status=422,
                                mimetype='application/json'
                            )
                    else:
                        response = Response(
                            response=json.dumps({'type': 'danger',
                                                 'text': 'Вы не отправили'
                                                         ' файла!'}),
                            status=422,
                            mimetype='application/json'
                        )

                    return response

        else:
            response = Response(
                response=json.dumps({'type': 'danger',
                                     'text': 'Доступ запрещен (403)'}),
                status=403,
                mimetype='application/json'
            )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


@API0.route(
    '/organization/buildings/<int:bid>/contacts/<string:cid>/photo',
    methods=['DELETE'])
@token_required
def delete_organization_building_conph(current_user, bid, cid):
    """ Удаление фото контакта здания """

    try:
        if CmsUsers.can(current_user.id, "put", "contacts"):
            building = CmsOrganizationBuildings.query.get(bid)

            if not building:
                response = Response(
                    response=json.dumps({'type': 'danger',
                                         'text': 'Такое здание '
                                                 'не существует!'}),
                    status=422,
                    mimetype='application/json'
                )
            else:
                if not any(
                        (
                        contact.get(
                            'cid', None) == cid
                        ) for contact in building.employee_contacts):
                    response = Response(
                        response=json.dumps(
                            {'type': 'danger',
                             'text': 'Такой контакт сотрудника '
                             'не существует!'}),
                        status=422,
                        mimetype='application/json'
                    )
                else:
                    c_data = [contact for contact in building.employee_contacts if contact.get('cid', None) == cid][0] # noqa: ignore=E501
                    if bool(c_data.get("photo")):
                        photo_filepath = os.path.join(
                            current_app.config['CMS_EMPLOYEE_PHOTOS'],
                            c_data.get("photo"))
                        if os.path.isfile(photo_filepath):
                            os.remove(photo_filepath)

                    c_data.update(
                        {'photo': ''})
                    flag_modified(building, 'employee_contacts')
                    db.session.commit()

                    response = Response(
                        response=json.dumps({'type': 'success',
                                             'text': 'Фото удалено!'}),
                        status=200,
                        mimetype='application/json'
                    )
        else:
            response = Response(
                response=json.dumps({'type': 'danger',
                                     'text': 'Доступ запрещен (403)'}),
                status=403,
                mimetype='application/json'
            )

        return response

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


@API0.route('/organization/buildings/<int:bid>', methods=['DELETE'])
@token_required
def delete_organization_buildings(current_user, bid):
    """ Удаление здания организации. """

    try:
        if CmsUsers.can(current_user.id, "delete", "contacts"):
            organization_buildings = CmsOrganizationBuildings.query.get(bid)
            if organization_buildings:

                for item in organization_buildings.employee_contacts:
                    if bool(item.get("photo", None)):
                        photo_filepath = os.path.join(
                            current_app.config['CMS_EMPLOYEE_PHOTOS'],
                            item.get("photo"))
                        if os.path.isfile(photo_filepath):
                            os.remove(photo_filepath)

                db.session.delete(organization_buildings)
                db.session.commit()
                response = Response(
                    response=json.dumps({'type': 'success',
                                         'text': 'Успешно удалено!'}),
                    status=200,
                    mimetype='application/json'
                )
            else:
                response = Response(
                    response=json.dumps({'type': 'danger',
                                         'text': 'Запись не найдена! (404)'}),
                    status=404,
                    mimetype='application/json'
                )
        else:
            response = Response(
                response=json.dumps({'type': 'danger',
                                     'text': 'Доступ запрещен (403)'}),
                status=403,
                mimetype='application/json'
            )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response

# ------------------------------------------------------------
# Страницы
# ------------------------------------------------------------


@API0.route('/pages', methods=['GET'])
@token_required
def get_pages(current_user):
    """ Получение полного списка страниц в json"""
    try:

        page_schema = SitePagesSchema(many=True)

        pages = SitePages.query.order_by(
                SitePages.creation_date.desc()).all()
        pdata = page_schema.dump(pages)
        pdata = pdata.data

        pdata = pagination_of_list(
            pdata,
            url_for('API0.get_pages',
                    _external=True),
            start=request.args.get('start', 1),
            limit=request.args.get('limit',
                                   SitePages.query.count())
        )

        response = Response(
            response=json.dumps(pdata),
            status=200,
            mimetype='application/json'
        )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


@API0.route('/pages/<string:uri>', methods=['GET'])
def get_page(uri):
    """ Получение информации о странице в json"""
    try:
        page_schema = SitePagesSchema()

        page = SitePages.query.filter(SitePages.uri == uri).first()
        pdata = page_schema.dump(page)
        pdata = pdata.data

        response = Response(
            response=json.dumps(pdata),
            status=200,
            mimetype='application/json'
        )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


@API0.route('/banners', methods=['GET'])
def get_page_as_banners():
    """ Получение страниц для баннеров json"""
    try:
        page_schema = BannerSchema(many=True)

        t = True
        banners = SitePages.query.filter(SitePages.banner == t).all()
        bdata = page_schema.dump(banners)
        bdata = bdata.data

        response = Response(
            response=json.dumps(bdata),
            status=200,
            mimetype='application/json'
        )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


@API0.route('/announcements', methods=['GET'])
def get_page_as_announcements():
    """ Получение страниц для анонсов json"""
    try:
        page_schema = AnnouncementsSchema(many=True)

        t = True
        announcements = SitePages.query.filter(
            SitePages.announcement == t).all()
        adata = page_schema.dump(announcements)
        adata = adata.data

        response = Response(
            response=json.dumps(adata),
            status=200,
            mimetype='application/json'
        )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


@API0.route('/pages/last', methods=['GET'])
def get_last_pages():
    """ Получение последних страниц в json"""
    try:
        page_schema = SitePagesSchema(many=True)

        llimit = int(request.args.get('limit', 6))
        if (llimit % 2 != 0):
            llimit += 1
        t = True
        page = SitePages.query.filter(
            SitePages.mainpage == t).order_by(
                SitePages.creation_date.desc()).limit(llimit).all()
        pdata = page_schema.dump(page)
        pdata = pdata.data

        response = Response(
            response=json.dumps(pdata),
            status=200,
            mimetype='application/json'
        )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


@API0.route('/pages/news', methods=['GET'])
def get_news_pages():
    """ Получение новостных страниц в json"""
    try:
        page_schema = SitePagesSchema(many=True)

        llimit = int(request.args.get('limit', 3))
        if (llimit % 3 != 0):
            while llimit % 3 != 0:
                llimit += 1

        pages = SitePages.query.filter(
            SitePages.structure_id == 54).order_by(
                SitePages.creation_date.desc()).all()

        pdata = page_schema.dump(pages)
        pdata = pdata.data

        pdata = pagination_of_list(
            pdata,
            url_for('API0.get_news_pages',
                    _external=True),
            start=request.args.get('start', 1),
            limit=llimit
        )

        response = Response(
            response=json.dumps(pdata),
            status=200,
            mimetype='application/json'
        )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


@API0.route('/pages/<int:pid>', methods=['DELETE'])
@token_required
def delete_pages(current_user, pid):
    """ Удаление записи страницы из БД"""

    try:
        if CmsUsers.can(current_user.id, "delete", "pages"):

            page = SitePages.query.get(pid)

            #  if user.photo:
            #  os.remove(os.path.join(
            #  current_app.config['CMS_USERS_AVATARS'],
            #  user.photo))

            db.session.delete(page)
            db.session.commit()

            response = Response(
                response=json.dumps({'type': 'success',
                                     'text': 'Успешно удалено!'}),
                status=200,
                mimetype='application/json'
            )
        else:
            response = Response(
                response=json.dumps({'type': 'danger',
                                     'text': 'Доступ запрещен (403)'}),
                status=403,
                mimetype='application/json'
            )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


@API0.route('/pages', methods=['POST'])
@token_required
def post_pages(current_user):
    """ Добавление страницы на сайт"""

    try:
        if CmsUsers.can(current_user.id, "post", "pages"):
            post_data = request.get_json()
            if not page_validator.is_valid(post_data):
                errors = []
                for error in sorted(
                        page_validator.iter_errors(
                            post_data), key=str):
                    errors.append(error.message)

                separator = '; '
                error_text = separator.join(errors)

                response = Response(
                        response=json.dumps({'type': 'danger',
                                             'text': error_text}),
                        status=422,
                        mimetype='application/json'
                    )
            else:
                if SitePages.query.filter(
                            SitePages.uri == post_data['uri']
                        ).first():
                    response = Response(
                        response=json.dumps({
                            'type': 'danger',
                            'text': 'Страница с таким URI существует! '
                                    'Придумайте другой или сгенерируйте '
                                    'новый URI!'
                            }),
                        status=422,
                        mimetype='application/json'
                    )
                else:
                    new_page = SitePages(
                        title=post_data['title'],
                        text=post_data['text'],
                        uri=post_data['uri'],
                        seo_description=post_data['description'],
                        seo_keywords=post_data['keywords'],
                        available=post_data['available'],
                        mainpage=post_data['mainpage'],
                        banner=post_data['banner'],
                        announcement=post_data['announcement']
                    )
                    if CmsStructure.query.filter(
                                (CmsStructure.id == post_data['section']['id'])
                                & (CmsStructure.left == CmsStructure.right - 1)
                            ).first():
                        new_page.structure_id = post_data['section']['id']

                        db.session.add(new_page)
                        db.session.commit()

                        response = Response(
                            response=json.dumps(
                                {'type': 'success',
                                 'text': 'Добавлена страница '
                                         '«'+str(new_page.uri)+'»!'}),
                            status=200,
                            mimetype='application/json'
                        )
                    else:
                        response = Response(
                            response=json.dumps({
                                'type': 'danger',
                                'text': 'Выбран несуществующий или '
                                        'не конечный раздел. '
                                        'Выберите другой раздел и '
                                        'отправьте форму заново!'
                            }),
                            status=422,
                            mimetype='application/json'
                        )
        else:
            response = Response(
                response=json.dumps({'type': 'danger',
                                     'text': 'Доступ запрещен (403)'}),
                status=403,
                mimetype='application/json'
            )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


@API0.route('/pages/<int:pid>', methods=['PUT'])
@token_required
def update_pages(current_user, pid):
    """ Изменение записи страницы в БД"""

    try:
        if CmsUsers.can(current_user.id, "put", "pages"):

            update_data = request.get_json()

            for pop_item in [
                    'files', 'gallery', 'cover', 'creation_date', 'id']:
                update_data.pop(pop_item, None)

            if not page_update_validator.is_valid(update_data):

                errors = []
                for error in sorted(page_update_validator.iter_errors(
                                    update_data), key=str):
                    errors.append(error.message)

                separator = '; '
                error_text = separator.join(errors)
                response = Response(
                        response=json.dumps({'type': 'danger',
                                             'text': error_text}),
                        status=422,
                        mimetype='application/json'
                    )

            else:
                if SitePages.query.filter(
                        (SitePages.uri == update_data['uri']) &
                        (SitePages.id != pid)).first():
                    response = Response(
                        response=json.dumps({
                            'type': 'danger',
                            'text': 'Страница с таким URI существует! '
                                    'Придумайте другой или '
                                    'сгенерируйте новый URI!'
                        }),
                        status=422,
                        mimetype='application/json'
                    )
                else:
                    old_data = SitePages.query.filter_by(id=pid)
                    old_uri = old_data.first().uri

                    new_structure = update_data.pop('structure', None)

                    if CmsStructure.query.filter(
                                (CmsStructure.id == new_structure['id'])
                                & (CmsStructure.left == CmsStructure.right - 1)
                            ).first():
                        update_data['structure_id'] = new_structure['id']

                        old_data.update(update_data)
                        db.session.commit()

                        response = Response(
                            response=json.dumps(
                                {'type': 'success',
                                 'text': 'Изменена страница '
                                         '/'+str(old_uri)+'!'}),
                            status=200,
                            mimetype='application/json'
                        )
                    else:
                        response = Response(
                            response=json.dumps({
                                'type': 'danger',
                                'text': 'Выбран несуществующий '
                                        'или не конечный раздел. '
                                        'Выберите другой раздел и '
                                        'отправьте форму заново!'
                            }),
                            status=422,
                            mimetype='application/json'
                        )
        else:
            response = Response(
                response=json.dumps({'type': 'danger',
                                     'text': 'Доступ запрещен (403)'}),
                status=403,
                mimetype='application/json'
            )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


@API0.route('/pages/<int:pid>/cover', methods=['DELETE'])
@token_required
def delete_page_cover(current_user, pid):
    """ Удаление обложки страницы """

    try:
        if CmsUsers.can(current_user.id, "put", "pages"):

            page = SitePages.query.get(pid)
            if page:
                if page.cover:

                    cover_filepath = os.path.join(
                        current_app.config['CMS_PAGE_COVERS'],
                        page.cover)

                    if os.path.isfile(cover_filepath):
                        os.remove(cover_filepath)

                    page.cover = None
                    db.session.commit()

                    response = Response(
                        response=json.dumps({'type': 'success',
                                             'text': 'Успешно удалена '
                                                     'обложка!'}),
                        status=200,
                        mimetype='application/json'
                    )
                else:
                    response = Response(
                        response=json.dumps({'type': 'danger',
                                             'text': 'К странице '
                                                     'не прикреплена '
                                                     'обложка!'}),
                        status=404,
                        mimetype='application/json'
                    )
            else:
                response = Response(
                    response=json.dumps({'type': 'danger',
                                         'text': 'Страница не существует!'}),
                    status=404,
                    mimetype='application/json'
                )
        else:
            response = Response(
                response=json.dumps({'type': 'danger',
                                     'text': 'Доступ запрещен (403)'}),
                status=403,
                mimetype='application/json'
            )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


@API0.route('/pages/<int:pid>/cover', methods=['PUT'])
@token_required
def update_page_cover(current_user, pid):
    """ Изменение обложки страницы"""

    try:
        page_query = SitePages.query.filter_by(id=pid)

        if request.files.getlist('cover'):

            if not len(request.files.getlist('cover')) > 1:

                cover_image = request.files['cover']

                if cover_image.content_type not in [
                            'image/jpeg',
                            'image/png',
                            'image/gif'
                        ]:
                    response = Response(
                        response=json.dumps({'type': 'danger',
                                             'text': 'Вы отправили'
                                                     'файл без расширения'
                                                     ' или это не изображение'
                                                     ' (jpeg, png, gif)!'}),
                        status=422,
                        mimetype='application/json'
                    )
                else:
                    if page_query.first().cover:
                        img_extension = cover_image.content_type.split('/')[1]
                        img_file_name = page_query.first().cover.split(
                            '.')[0] + \
                            '.' + img_extension
                        cover_filepath = os.path.join(
                            current_app.config['CMS_PAGE_COVERS'],
                            page_query.first().cover)
                        if os.path.isfile(cover_filepath):
                            os.remove(cover_filepath)
                    else:
                        img_extension = cover_image.content_type.split('/')[1]
                        img_file_name = uuid.uuid1().hex + '.' + img_extension

                    page_query.update(
                        {'cover': img_file_name})
                    db.session.commit()

                    cover_image.save(
                        os.path.join(
                            current_app.config['CMS_PAGE_COVERS'],
                            img_file_name))

                    response = Response(
                        response=json.dumps({'type': 'success',
                                             'text': 'Фотокарточка вклеена!'}),
                        status=200,
                        mimetype='application/json'
                    )
            else:
                response = Response(
                    response=json.dumps({'type': 'danger',
                                         'text': 'Вы отправили'
                                                 'более 1 файла!'}),
                    status=422,
                    mimetype='application/json'
                )
        else:
            response = Response(
                response=json.dumps({'type': 'danger',
                                     'text': 'Вы не отправили'
                                             ' файла!'}),
                status=422,
                mimetype='application/json'
            )

        return response

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


@API0.route('/pages/<int:pid>/files', methods=['POST'])
@token_required
def post_page_files(current_user, pid):
    """ Изменение файлов страницы"""

    try:
        page = SitePages.query.get(pid)
        if request.files.getlist('file[]'):

            page_files = request.files.getlist('file[]')
            na_files = []
            for pfile in page_files:
                fsize_b = get_fsize(pfile)
                # Еще можно считывать файл в память до заданного размера
                # Но появляется проблема при записи файла,
                # так как он уже считан
                # MAX_FILE_SIZE = 1024 * 1024 + 1
                # file_bytes = file.read(MAX_FILE_SIZE)
                fsize_mb = formatBytes(fsize_b, power=2)['number']
                if ((pfile.content_type not in [
                            'application/vnd.openxmlformats-officedocument'
                            '.wordprocessingml.document',
                            'application/vnd.oasis.opendocument.text',
                            'application/pdf',
                            'application/zip',
                            'application/msword'
                        ]) or (fsize_mb > 10)):
                    na_files.append("«" + pfile.filename + "»")
                else:
                    fsize = formatBytes(fsize_b)
                    extension = pfile.filename.split(".")[-1]
                    separator = ' '
                    new_file_name = uuid.uuid1().hex + '.' + extension
                    ud = {
                        "fid": str(uuid.uuid4().hex),
                        "name": separator.join(pfile.filename.split(".")[:-1]),
                        "size": str(fsize['number']) + ' ' + fsize['measure'],
                        "fname": new_file_name,
                        "extension": extension
                    }
                    page.files.append(ud)
                    pfile.save(
                        os.path.join(
                            current_app.config['CMS_PAGE_FILES'],
                            new_file_name))

            flag_modified(page, 'files')
            db.session.commit()

            rtext = 'Файлы добавлены!'
            rtype = 'success'
            if na_files:
                rtext = 'Файлы добавлены, но файлы: '
                separator = ', '
                rtext = rtext + separator.join(na_files)
                rtext = rtext + ' были проигнорированы, т.к. ' \
                    'либо превышен размер, либо не подходящий формат файла.'
                rtype = 'warning'

            response = Response(
                response=json.dumps({'type': rtype,
                                     'text': rtext}),
                status=200,
                mimetype='application/json'
            )
        else:
            response = Response(
                response=json.dumps({'type': 'danger',
                                     'text': 'Вы не отправили'
                                             ' ни одного файла!'}),
                status=422,
                mimetype='application/json'
            )

        return response

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


@API0.route('/pages/<int:pid>/files/<string:fid>', methods=['DELETE'])
@token_required
def delete_page_file(current_user, pid, fid):
    """ Удаление файла страницы """

    try:
        if CmsUsers.can(current_user.id, "put", "pages"):
            page = SitePages.query.get(pid)
            if page:
                if page.files:
                    file_found = next(
                        (pfile for pfile in page.files if pfile.get(
                            'fid', None) == fid),
                        None
                    )
                    if file_found:
                        page.files = [i for i in page.files if not (
                            i['fid'] == fid
                        )]
                        db.session.commit()

                        filepath = os.path.join(
                            current_app.config['CMS_PAGE_FILES'],
                            file_found.get("fname"))
                        if os.path.isfile(filepath):
                            os.remove(filepath)

                        response = Response(
                            response=json.dumps({'type': 'success',
                                                 'text': 'Успешно удален '
                                                         'файл!'}),
                            status=200,
                            mimetype='application/json'
                        )
                    else:
                        response = Response(
                            response=json.dumps({'type': 'danger',
                                                 'text': 'Указанный '
                                                         'файл '
                                                         'не существует!'}),
                            status=404,
                            mimetype='application/json'
                        )

                else:
                    response = Response(
                        response=json.dumps({'type': 'danger',
                                             'text': 'К странице '
                                                     'не прикреплены '
                                                     'файлы!'}),
                        status=404,
                        mimetype='application/json'
                    )
            else:
                response = Response(
                    response=json.dumps({'type': 'danger',
                                         'text': 'Страница не существует!'}),
                    status=404,
                    mimetype='application/json'
                )
        else:
            response = Response(
                response=json.dumps({'type': 'danger',
                                     'text': 'Доступ запрещен (403)'}),
                status=403,
                mimetype='application/json'
            )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


@API0.route('/pages/<int:pid>/files/<string:fid>', methods=['PUT'])
@token_required
def update_page_file_data(current_user, pid, fid):
    """ Удаление файла страницы """

    try:
        update_data = request.get_json()

        if not filepage_update_validator.is_valid(update_data):
            errors = []
            for error in sorted(filepage_update_validator.iter_errors(
                                update_data), key=str):
                errors.append(error.message)

            separator = '; '
            error_text = separator.join(errors)
            response = Response(
                    response=json.dumps({'type': 'danger',
                                         'text': error_text}),
                    status=422,
                    mimetype='application/json'
                )
        else:
            if CmsUsers.can(current_user.id, "put", "pages"):
                page = SitePages.query.get(pid)
                if page:
                    if page.files:
                        file_found = next(
                            (pfile for pfile in page.files if pfile.get(
                                'fid', None) == fid),
                            None
                        )
                        if file_found:
                            file_old_name = file_found.get('name', None)
                            file_found['name'] = update_data['name']
                            page.files = [i if not (
                                i['fid'] == fid
                            ) else file_found for i in page.files]
                            flag_modified(page, 'files')
                            db.session.commit()

                            response = Response(
                                response=json.dumps({
                                    'type': 'success',
                                    'text': 'Успешно изменен '
                                    'файл «'+str(file_old_name)+'»!'
                                }),
                                status=200,
                                mimetype='application/json'
                            )
                        else:
                            response = Response(
                                response=json.dumps({
                                    'type': 'danger',
                                    'text': 'Указанный '
                                            'файл '
                                            'не существует!'
                                }),
                                status=404,
                                mimetype='application/json'
                            )

                    else:
                        response = Response(
                            response=json.dumps({'type': 'danger',
                                                 'text': 'К странице '
                                                         'не прикреплены '
                                                         'файлы!'}),
                            status=404,
                            mimetype='application/json'
                        )
                else:
                    response = Response(
                        response=json.dumps({
                            'type': 'danger',
                            'text': 'Страница не существует!'
                        }),
                        status=404,
                        mimetype='application/json'
                    )
            else:
                response = Response(
                    response=json.dumps({'type': 'danger',
                                         'text': 'Доступ запрещен (403)'}),
                    status=403,
                    mimetype='application/json'
                )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


@API0.route('/pages/<int:pid>/images/<string:iid>', methods=['DELETE'])
@token_required
def delete_page_image(current_user, pid, iid):
    """ Удаление файла страницы """

    try:
        if CmsUsers.can(current_user.id, "put", "pages"):
            page = SitePages.query.get(pid)
            if page:
                if page.gallery:
                    image_found = next(
                        (pimage for pimage in page.gallery if pimage.get(
                            'iid', None) == iid),
                        None
                    )
                    if image_found:
                        page.gallery = [i for i in page.gallery if not (
                            i['iid'] == iid
                        )]
                        db.session.commit()

                        filepath = os.path.join(
                            current_app.config['CMS_PAGE_GALLERY'],
                            image_found.get("fname"))
                        if os.path.isfile(filepath):
                            os.remove(filepath)

                        response = Response(
                            response=json.dumps({'type': 'success',
                                                 'text': 'Успешно удалено '
                                                         'изображение!'}),
                            status=200,
                            mimetype='application/json'
                        )
                    else:
                        response = Response(
                            response=json.dumps({'type': 'danger',
                                                 'text': 'Указанное '
                                                         'изображение '
                                                         'не существует!'}),
                            status=404,
                            mimetype='application/json'
                        )

                else:
                    response = Response(
                        response=json.dumps({'type': 'danger',
                                             'text': 'К странице '
                                                     'не прикреплены '
                                                     'изображения!'}),
                        status=404,
                        mimetype='application/json'
                    )
            else:
                response = Response(
                    response=json.dumps({'type': 'danger',
                                         'text': 'Страница не существует!'}),
                    status=404,
                    mimetype='application/json'
                )
        else:
            response = Response(
                response=json.dumps({'type': 'danger',
                                     'text': 'Доступ запрещен (403)'}),
                status=403,
                mimetype='application/json'
            )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


@API0.route('/pages/<int:pid>/images', methods=['POST'])
@token_required
def post_page_images(current_user, pid):
    """ Изменение файлов страницы"""

    try:
        page = SitePages.query.get(pid)
        if request.files.getlist('image[]'):

            page_images = request.files.getlist('image[]')
            na_images = []
            for pimage in page_images:
                fsize_b = get_fsize(pimage)
                # Еще можно считывать файл в память до заданного размера
                # Но появляется проблема при записи файла,
                # так как он уже считан
                # MAX_FILE_SIZE = 1024 * 1024 + 1
                # file_bytes = file.read(MAX_FILE_SIZE)
                fsize_mb = formatBytes(fsize_b, power=2)['number']
                if ((pimage.content_type not in [
                            'image/gif',
                            'image/jpeg',
                            'image/pjpeg',
                            'image/png'
                        ]) or (fsize_mb > 10)):
                    na_images.append("«" + pimage.filename + "»")
                else:
                    fsize = formatBytes(fsize_b)
                    extension = pimage.filename.split(".")[-1]
                    separator = ' '
                    new_image_name = uuid.uuid1().hex + '.' + extension
                    ud = {
                        "iid": str(uuid.uuid4().hex),
                        "name": separator.join(
                            pimage.filename.split(".")[:-1]
                        ),
                        "fname": new_image_name
                    }
                    page.gallery.append(ud)
                    pimage.save(
                        os.path.join(
                            current_app.config['CMS_PAGE_GALLERY'],
                            new_image_name))

            flag_modified(page, 'gallery')
            db.session.commit()

            rtext = 'Изображения добавлены!'
            rtype = 'success'
            if na_images:
                rtext = 'Изображения добавлены, но изображения: '
                separator = ', '
                rtext = rtext + separator.join(na_images)
                rtext = rtext + ' были проигнорированы, т.к. ' \
                    'либо превышен размер, либо не подходящий формат файла.'
                rtype = 'warning'

            response = Response(
                response=json.dumps({'type': rtype,
                                     'text': rtext}),
                status=200,
                mimetype='application/json'
            )
        else:
            response = Response(
                response=json.dumps({'type': 'danger',
                                     'text': 'Вы не отправили'
                                             ' ни одного файла!'}),
                status=422,
                mimetype='application/json'
            )

        return response

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


@API0.route('/pages/<int:pid>/images/<string:iid>', methods=['PUT'])
@token_required
def update_page_image_data(current_user, pid, iid):
    """ Удаление файла страницы """

    try:
        update_data = request.get_json()

        if not imagepage_update_validator.is_valid(update_data):
            errors = []
            for error in sorted(imagepage_update_validator.iter_errors(
                                update_data), key=str):
                errors.append(error.message)

            separator = '; '
            error_text = separator.join(errors)
            response = Response(
                    response=json.dumps({'type': 'danger',
                                         'text': error_text}),
                    status=422,
                    mimetype='application/json'
                )
        else:
            if CmsUsers.can(current_user.id, "put", "pages"):
                page = SitePages.query.get(pid)
                if page:
                    if page.gallery:
                        image_found = next(
                            (pimage for pimage in page.gallery if pimage.get(
                                'iid', None) == iid),
                            None
                        )
                        if image_found:
                            file_old_name = image_found.get('name', None)
                            image_found['name'] = update_data['name']
                            page.gallery = [i if not (
                                i['iid'] == iid
                            ) else image_found for i in page.gallery]
                            flag_modified(page, 'gallery')
                            db.session.commit()

                            response = Response(
                                response=json.dumps({
                                    'type': 'success',
                                    'text': 'Успешно изменено '
                                    'файл «'+str(file_old_name)+'»!'
                                }),
                                status=200,
                                mimetype='application/json'
                            )
                        else:
                            response = Response(
                                response=json.dumps({
                                    'type': 'danger',
                                    'text': 'Указанное '
                                            'изображение '
                                            'не существует!'
                                }),
                                status=404,
                                mimetype='application/json'
                            )

                    else:
                        response = Response(
                            response=json.dumps({'type': 'danger',
                                                 'text': 'К странице '
                                                         'не прикреплены '
                                                         'изображения!'}),
                            status=404,
                            mimetype='application/json'
                        )
                else:
                    response = Response(
                        response=json.dumps({
                            'type': 'danger',
                            'text': 'Страница не существует!'
                        }),
                        status=404,
                        mimetype='application/json'
                    )
            else:
                response = Response(
                    response=json.dumps({'type': 'danger',
                                         'text': 'Доступ запрещен (403)'}),
                    status=403,
                    mimetype='application/json'
                )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


@API0.route('/pages/search', methods=['GET'])
def get_page_search():
    """ Поиск страницы по заголовку"""

    try:
        page_schema = SitePagesSchema(many=True)

        llimit = int(request.args.get('limit', 20))
        if (llimit % 20 != 0):
            while llimit % 20 != 0:
                llimit += 1

        query = request.args.get('q', None)

        if query:
            db_query = "%{}%".format(query)
            pages = SitePages.query.filter(
                ((SitePages.title.like(db_query)) |
                    (SitePages.seo_description.like(db_query))) &
                (SitePages.available)).order_by(
                    SitePages.creation_date.desc()).all()

            pdata = page_schema.dump(pages)
            pdata = pdata.data

            pdata = pagination_of_list(
                pdata,
                url_for('API0.get_page_search',
                        _external=True),
                start=request.args.get('start', 1),
                limit=llimit,
                q=query
            )

            response = Response(
                response=json.dumps(pdata),
                status=200,
                mimetype='application/json'
            )
        else:
            response = Response(
                response=json.dumps({
                    'type': 'danger',
                    'text': 'Данных по Вашему запросу не найдено!'
                }),
                status=404,
                mimetype='application/json'
            )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


# ------------------------------------------------------------
# Памятные даты
# ------------------------------------------------------------


@API0.route('/history/events/closest', methods=['GET'])
def get_history_events_closest():
    """ Получение полного списка страниц в json"""
    try:

        event_schema = HistoryEventsSchema(many=True)
        datef = datetime.today()
        further_date = datef + timedelta(days=14)
        if further_date.year > datetime.today().year:
            further_date = date(year=datetime.today().year, month=12, day=31)

        events = HistoryEvents.query.filter(
            extract('month', HistoryEvents.event_date) <= further_date.month,
            extract('month', HistoryEvents.event_date) >= datef.month,
            extract('day', HistoryEvents.event_date) <= further_date.day,
            extract('day', HistoryEvents.event_date) >= datef.day,
        )

        edata = event_schema.dump(events)
        edata = edata.data

        response = Response(
            response=json.dumps(edata),
            status=200,
            mimetype='application/json'
        )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


@API0.route('/history/events', methods=['GET'])
@token_required
def get_history_events(current_user):
    """ Получение полного списка страниц в json"""
    try:

        event_schema = HistoryEventsSchema(many=True)

        events = HistoryEvents.query.all()
        edata = event_schema.dump(events)
        edata = edata.data

        edata = pagination_of_list(
            edata,
            url_for('API0.get_history_events',
                    _external=True),
            start=request.args.get('start', 1),
            limit=request.args.get('limit',
                                   HistoryEvents.query.count())
        )

        response = Response(
            response=json.dumps(edata),
            status=200,
            mimetype='application/json'
        )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


@API0.route('/history/events/<int:eid>', methods=['GET'])
def get_history_event(eid):
    """ Получение информации о странице в json"""
    try:
        event_schema = HistoryEventsSchema()

        event = HistoryEvents.query.filter(HistoryEvents.id == eid).first()
        edata = event_schema.dump(event)
        edata = edata.data

        response = Response(
            response=json.dumps(edata),
            status=200,
            mimetype='application/json'
        )

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response
