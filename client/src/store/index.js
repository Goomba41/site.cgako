/* eslint no-shadow: ["error", { "allow": ["state"] }] */

import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';
import _ from 'lodash';
import {
  isValidJwt, EventBus, currentUserLogin, i18n,
} from '@/utils';

Vue.use(Vuex);

// Источник данных
const state = {
  roles: [], // список ролей CMS
  users: [], // список пользователей CMS
  uid: '', // id текущего пользователя
  profile: {}, // профиль текущего пользователя
  uploadProgress: 0,
  uploadProgressMax: 100,
  formPending: false,
  reactivationPeriod: 7,
  jwt: localStorage.getItem('token') || '', // Загрузить токен из хранилища, или инициировать пустой, если нет в хранилище
  locale: localStorage.getItem('locale') || 'ru',
  languages: {
    value: { locale: 'ru', class: 'ru', translation: 'rus' },
    options: [
      { locale: 'ru', class: 'ru', translation: 'rus' },
      { locale: 'su', class: 'su', translation: 'sul' },
      { locale: 'en', class: 'us', translation: 'eng' },
    ],
  },
};

const actions = {
  // Запрос токена с отсылкой авторизационных данных
  async login(context, userCreds) {
    context.commit('setFormPending');

    const userAgent = { agent: window.navigator.userAgent };
    let ip = { ip: 'unknown' };

    await axios.get('https://api.ipify.org/?format=json')
      .then((response) => { ip = response.data; })
      .catch((error) => {
        // eslint-disable-next-line
        console.log(error.response.data);
        context.commit('setFormPending');
      });

    const userData = _.assign({}, userCreds, userAgent, ip);
    return axios.post('/api/login', userData)
      .then((response) => {
        context.commit('setJwtToken', { jwt: response.data });
        context.commit('setFormPending');
      })
      .catch((error) => {
        EventBus.$emit('failedAuthentication', error.response.data);
        context.commit('setFormPending');
      });
  },
  // Выход с сайта с удалением токена из локального хранилища и хранилища состояния
  logout(context) {
    context.commit('unsetJwtToken');
  },
  // Информация о проекте Github API
  loadGithubInfo() {
    return axios.get('https://api.github.com/repos/Goomba41/site.cgako/languages')
      .then((response) => {
        // eslint-disable-next-line
        console.log(response.data);
      })
      .catch((error) => {
        // eslint-disable-next-line
        console.error(error);
      });
  },
  // Верификация почты, отсылка письма
  verifyMailSend(context, payload) {
    context.commit('setFormPending');
    return axios.get(`/api/profile/${payload.id}/mail/verify-send`,
      {
        headers: { Authorization: `Bearer: ${context.state.jwt}` },
        params: {
          value: payload.value,
          type: payload.type,
        },
      })
      .then((response) => {
        context.commit('setFormPending');
        EventBus.$emit('message', response.data);
      })
      .catch((error) => {
        EventBus.$emit('message', error.response.data);
        context.commit('setFormPending');
      });
  },
  // Сброс активации почты
  verifyMailReset(context, payload) {
    context.commit('setFormPending');
    return axios.get(`/api/users/${payload.id}/mail/verify-reset?dbg`,
      {
        headers: { Authorization: `Bearer: ${context.state.jwt}` },
        params: {
          value: payload.value,
          type: payload.type,
        },
      })
      .then((response) => {
        context.commit('setFormPending');
        EventBus.$emit('message', response.data);
      })
      .catch((error) => {
        EventBus.$emit('message', error.response.data);
        context.commit('setFormPending');
      });
  },
  // Блокирование пароля
  passwordBlock(context, payload) {
    context.commit('setFormPending');
    return axios.get(`/api/users/${payload.id}/password/block?dbg`,
      { headers: { Authorization: `Bearer: ${context.state.jwt}` } })
      .then((response) => {
        context.commit('setFormPending');
        EventBus.$emit('message', response.data);
      })
      .catch((error) => {
        EventBus.$emit('message', error.response.data);
        context.commit('setFormPending');
      });
  },
  // Сброс пароля с генерацией нового и отправкой на почту
  passwordReset(context, payload) {
    context.commit('setFormPending');
    return axios.get(`/api/users/${payload.id}/password/reset?dbg`,
      { headers: { Authorization: `Bearer: ${context.state.jwt}` } })
      .then((response) => {
        context.commit('setFormPending');
        EventBus.$emit('message', response.data);
      })
      .catch((error) => {
        EventBus.$emit('message', error.response.data);
        context.commit('setFormPending');
      });
  },
  // Верификация почты, ответ
  verifyMail(context, token) {
    return axios.get(`/api/verify/mail/${token}`)
      .then((response) => {
        EventBus.$emit('messageActivation', response.data);
      })
      .catch((error) => {
        // eslint-disable-next-line
        EventBus.$emit('messageActivation', error.response.data);
      });
  },
  // Загрузить данные профиля вошедшего пользователя
  loadProfile(context) {
    return axios.get(`/api/profile/${context.state.uid}`, { headers: { Authorization: `Bearer: ${context.state.jwt}` } })
      .then((response) => {
        context.commit('setProfile', { profile: response.data });
      })
      .catch((error) => {
        // eslint-disable-next-line
        console.error(error);
      });
  },
  // Обновить данные профиля вошедшего пользователя
  updateProfileData(context, dataUpdate) {
    context.commit('setFormPending');

    return axios.put(`/api/profile/${context.state.uid}/data?dbg`, dataUpdate,
      { headers: { Authorization: `Bearer: ${context.state.jwt}` } })
      .then((response) => {
        context.dispatch('loadProfile');
        EventBus.$emit('forceRerender');
        EventBus.$emit('message', response.data);
        context.commit('setFormPending');
      })
      .catch((error) => {
        EventBus.$emit('message', error.response.data);
        context.commit('setFormPending');
      });
  },
  // Обновить пароль вошедшего пользователя
  updateProfilePassword(context, dataUpdate) {
    return axios.put(`/api/profile/${context.state.uid}/password`, dataUpdate,
      { headers: { Authorization: `Bearer: ${context.state.jwt}` } })
      .then(() => { EventBus.$emit('logout'); })
      .catch((error) => {
        // eslint-disable-next-line
        EventBus.$emit('failedAuthentication', error.response.data);
      });
  },
  // Обновить аватар вошедшего пользователя
  updateProfileAvatar(context, dataUpdate) {
    return axios.put(`/api/profile/${context.state.uid}/avatar`, dataUpdate,
      {
        headers: {
          Authorization: `Bearer: ${context.state.jwt}`,
        },
        onUploadProgress: (progressEvent) => {
          // eslint-disable-next-line
          state.uploadProgress = (progressEvent.loaded / progressEvent.total)*100;
        },
      })
      .then((response) => {
        context.dispatch('loadProfile');
        state.uploadProgress = 0;
        EventBus.$emit('forceRerender');
        EventBus.$emit('message', response.data);
      })
      .catch((error) => {
        // eslint-disable-next-line
        console.log(error);
      });
  },
  // Удалить фотокарточку профиля
  deleteProfileAvatar(context) {
    return axios.delete(`/api/profile/${context.state.uid}/avatar?dbg`, { headers: { Authorization: `Bearer: ${context.state.jwt}` } })
      .then((response) => {
        EventBus.$emit('forceRerender');
        EventBus.$emit('message', response.data);
      })
      .catch((error) => {
        EventBus.$emit('message', error.response.data);
      });
  },
  // Загрузить пользователей
  loadUsers(context, payload) {
    context.commit('setFormPending');

    return axios.get('/api/users',
      {
        headers: { Authorization: `Bearer: ${context.state.jwt}` },
        params: {
          limit: payload.limit || 20,
          start: payload.start || 1,
        },
      })
      .then((response) => {
        context.commit('setUsers', { users: response.data });
        context.commit('setFormPending');
      })
      .catch((error) => {
        // eslint-disable-next-line
        console.error(error);
        context.commit('setFormPending');
      });
  },
  // Создать нового пользователя
  newUser(context, dataNew) {
    context.commit('setFormPending');

    return axios.post('/api/users?dbg', dataNew,
      { headers: { Authorization: `Bearer: ${context.state.jwt}` } })
      .then((response) => {
        EventBus.$emit('message', response.data);
        context.commit('setFormPending');
      })
      .catch((error) => {
        EventBus.$emit('message', error.response.data);
        context.commit('setFormPending');
      });
  },
  // Изменение пользователя
  updateUser(context, dataUpdate) {
    context.commit('setFormPending');

    return axios.put(`/api/users/${dataUpdate.id}?dbg`, dataUpdate,
      { headers: { Authorization: `Bearer: ${context.state.jwt}` } })
      .then((response) => {
        EventBus.$emit('message', response.data);
        context.commit('setFormPending');
      })
      .catch((error) => {
        EventBus.$emit('message', error.response.data);
        context.commit('setFormPending');
      });
  },
  // Обновить аватар пользователя
  updateUserAvatar(context, dataUpdate) {
    return axios.put(`/api/users/${dataUpdate.id}/avatar?dbg`, dataUpdate.formData,
      {
        headers: {
          Authorization: `Bearer: ${context.state.jwt}`,
        },
        onUploadProgress: (progressEvent) => {
          state.uploadProgress = (progressEvent.loaded / progressEvent.total) * 100;
        },
      })
      .then((response) => {
        state.uploadProgress = 0;
        EventBus.$emit('forceRerender');
        EventBus.$emit('message', response.data);
      })
      .catch((error) => {
        EventBus.$emit('message', error.response.data);
      });
  },
  // Удалить фотокарточку пользователя
  deleteUserAvatar(context, payload) {
    return axios.delete(`/api/users/${payload.id}/avatar?dbg`, { headers: { Authorization: `Bearer: ${context.state.jwt}` } })
      .then((response) => {
        EventBus.$emit('forceRerender');
        EventBus.$emit('message', response.data);
      })
      .catch((error) => {
        EventBus.$emit('message', error.response.data);
      });
  },
  // Удалить пользователя
  deleteUser(context, payload) {
    return axios.delete(`/api/users/${payload.id}`, { headers: { Authorization: `Bearer: ${context.state.jwt}` } })
      .then((response) => {
        EventBus.$emit('forceRerender');
        EventBus.$emit('message', response.data);
      })
      .catch((error) => {
        // eslint-disable-next-line
        EventBus.$emit('message', error.response.data);
      });
  },
  // Загрузить роли
  loadRoles(context, payload) {
    context.commit('setFormPending');

    return axios.get('/api/roles?dbg',
      {
        headers: { Authorization: `Bearer: ${context.state.jwt}` },
        params: {
          limit: payload.limit || 20,
          start: payload.start || 1,
        },
      })
      .then((response) => {
        context.commit('setRoles', { roles: response.data });
        context.commit('setFormPending');
      })
      .catch((error) => {
        // eslint-disable-next-line
        console.error(error);
        context.commit('setFormPending');
        EventBus.$emit('message', error.response.data);
      });
  },
  // Смена локали
  changeLocale(context, value) {
    const lang = value.locale;
    context.commit('setLocale', { lang, value });
    import(`../langs/${lang}.json`).then((msgs) => {
      i18n.setLocaleMessage(lang, msgs);
      i18n.locale = lang;
    });
  },
  // Предустановка локали в селекторе после перезагрузки
  presetLocale(context, value) {
    state.languages.value = _.find(state.languages.options, { locale: value });
  },
};

// Мутации данных
const mutations = {
  // Установка статуса отправки формы
  setFormPending(state) {
    state.formPending = !state.formPending;
  },
  // Установка токена аутентификации
  setJwtToken(state, payload) {
    localStorage.token = payload.jwt;
    state.jwt = payload.jwt;
  },
  // Установка локали
  setLocale(state, payload) {
    localStorage.locale = payload.lang;
    state.locale = payload.lang;
    state.languages.value = payload.value;
  },
  // Очистка токена аутентификации
  unsetJwtToken(state) {
    localStorage.removeItem('token');
    state.jwt = '';
  },
  // Установка списка пользователей
  setUsers(state, payload) {
    state.users = payload.users;
  },
  // Установка списка ролей
  setRoles(state, payload) {
    state.roles = payload.roles;
  },
  // Установка профиля пользователя
  setProfile(state, payload) {
    state.profile = payload.profile;
  },
};

// Переиспользуемые "получатели" данных
const getters = {
  // Проверка аутентикации путем верификации токена
  isAuthenticated(state) {
    return isValidJwt(state.jwt);
  },
  currentUser(state) {
    return currentUserLogin(state.jwt);
  },
};

const store = new Vuex.Store({
  state,
  actions,
  mutations,
  getters,
});

export default store;
