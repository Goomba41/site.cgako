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

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from itsdangerous import TimedJSONWebSignatureSerializer
from sqlalchemy import func
from urllib.parse import urljoin
from user_agents import parse
from flask import current_app, json, Blueprint, \
    request, Response, url_for, render_template
from flask_mail import Message
from functools import wraps


from app import bcrypt, db, mail
from app.models import CmsUsers, CmsUsersSchema, CmsProfileSchema, \
    CmsRoles, CmsRolesSchema, SystemObjects, SystemObjectsActions, \
    AssociationPermission, AssociationPermissionSchema, user_role
from app.json_validation import profile_validator, password_validator, \
    user_validator, user_update_validator

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
def pagination_of_list(query_result, url, start, limit):
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
        response_obj['previous'] = urljoin(url,
                                           '?start=%d&limit=%d'
                                           % (start_copy, limit_copy))

    # Создаем URL на следующую страницу
    if start + limit > records_count:
        response_obj['next'] = ''
    else:
        start_copy = start + limit
        response_obj['next'] = urljoin(url,
                                       '?start=%d&limit=%d'
                                       % (start_copy, limit))

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
                confirm_url = 'http://192.168.0.91:8080/verify' \
                              '/mail/' + token.decode("utf-8")
                html = render_template(
                    'confirmation_mail.html',
                    confirm_url=confirm_url,
                    active_time="1 час")
                subject = 'Подтверждение адреса электронной ' \
                          'почты в CMS сайта ЦГАКО'
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
                            confirm_url = 'http://192.168.0.91:8080/verify' \
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
                confirm_url = 'http://192.168.0.91:8080/verify' \
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

        post_data = request.get_json()

        if not user_validator.is_valid(post_data):
            errors = []
            for error in sorted(user_validator.iter_errors(
                                post_data), key=str):
                errors.append(error.message)

            separator = '; '
            error_text = separator.join(errors)
            print(error_text)
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
                        if role_exist is not None:
                            user.roles.append(role_exist)
                    if not user.roles:
                        user.roles.append(
                            CmsRoles.query.filter_by(id=4).first())
                else:
                    user.roles.append(CmsRoles.query.filter_by(id=4).first())

                db.session.add(user)
                db.session.commit()

                password = post_data['password']
                login = post_data['login']
                additional_mails = []
                for mail_item in post_data['email']:
                    if mail_item['value'] and mail_item['type'] != "primary":
                        additional_mails.append(mail_item['value'])

                token = generate_confirmation_token(
                    {
                     "uid": user.id,
                     "value": primary_mail,
                     "type": "primary"
                    }, expiration=3600)
                confirm_url = 'http://192.168.0.91:8080/verify' \
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

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


@API0.route('/users/<int:uid>', methods=['PUT'])
@token_required
def update_users(current_user, uid):
    """ Изменение записи пользователя в БД"""

    try:

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
            for pop_item in ['id', 'socials', 'photo', 'last_login', 'status']:
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
                        response=json.dumps({'type': 'danger',
                                             'text': 'Пользователь с такими'
                                                     ' данными существует!'}),
                        status=422,
                        mimetype='application/json'
                    )
                else:
                    #  Составить попарный список предыдущих и полученных почт
                    previous = CmsUsers.query.filter_by(id=uid).first().email
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
                                confirm_url = 'http://192.168.0.91:8080/' \
                                              'verify/mail/' + token.decode(
                                                "utf-8")
                                html = render_template(
                                    'confirmation_mail.html',
                                    confirm_url=confirm_url,
                                    active_time="1 час")
                                subject = 'Подтверждение адреса электронной ' \
                                          'почты в CMS сайта ЦГАКО'
                                send_email(mail_item['value'], subject, html)

                    old_data = CmsUsers.query.filter_by(id=uid)
                    old_login = old_data.first().login

                    #  Обработка списка ролей
                    new_roles = update_data.pop('roles', None)

                    if new_roles is not None:
                        old_roles = old_data.first()
                        old_roles.roles.clear()
                        for role in new_roles:
                            #  Проверить, существует ли роль в базе,
                            #  если нет, то ничего
                            #  иначе добавить пользователю роль
                            role_exist = CmsRoles.query.filter_by(
                                id=role['id']).first()
                            if role_exist is not None:
                                old_roles.roles.append(role_exist)
                        if not old_roles.roles:
                            old_roles.roles.append(
                                CmsRoles.query.filter_by(id=4).first())

                    old_data.update(update_data)
                    db.session.commit()

                    response = Response(
                        response=json.dumps({'type': 'success',
                                             'text': 'Изменен пользователь '
                                                     '@'+str(old_login)+'!',
                                             'link': url_for('.get_user_by_id',
                                                             uid=uid,
                                                             _external=True)}),
                        status=200,
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

    except Exception:

        response = server_error(request.args.get("dbg"))

    return response


@API0.route('/users/<int:uid>/password/reset', methods=['GET'])
@token_required
def users_password_reset(current_user, uid):
    """Блокирование пароля пользователя"""

    try:

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
                response=json.dumps({'type': 'success',
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

        #  test_schema = AssociationPermissionSchema(exclude=['roles'])
        #  test = AssociationPermission.query.first()
        #  testdata = test_schema.dump(test)
        #  print(testdata.data)

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


# ------------------------------------------------------------
# Новости
# ------------------------------------------------------------
