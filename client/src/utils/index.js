import Vue from 'vue';
import moment from 'moment';
import VueI18n from 'vue-i18n';
import _ from 'lodash';
import ru from '../langs/ru.json';

Vue.use(VueI18n);

VueI18n.prototype.getChoiceIndex = function plur(choice, choicesLength) {
  if (choice === 0) {
    return 0;
  }

  const teen = choice > 10 && choice < 20;
  const endsWithOne = choice % 10 === 1;

  if (!teen && endsWithOne) {
    return 1;
  }

  if (!teen && choice % 10 >= 2 && choice % 10 <= 4) {
    return 2;
  }

  return (choicesLength < 4) ? 2 : 3;
};

export const i18n = new VueI18n({
  locale: 'ru',
  fallbackLocale: 'ru',
  messages: {
    ru,
  },
});

export const EventBus = new Vue();

// Проверка валидности токена по срокам и по структуре
export function isValidJwt(jwt) {
  if (!jwt || jwt.split('.').length < 3) {
    return false;
  }
  const data = JSON.parse(atob(jwt.split('.')[1]));
  const exp = new Date(data.exp * 1000);
  const now = new Date();
  return now < exp;
}

// Получение кода текущего пользователя из токена
export function currentUserLogin(jwt) {
  if (!jwt || jwt.split('.').length < 3) {
    return false;
  }
  const data = JSON.parse(atob(jwt.split('.')[1]));
  return data.uid;
}

// Ответ true/false на запрос прав пользователя
export function can(permissions, action, object) {
  if (_.find(permissions, { action, object })) {
    return true;
  }
  return false;
}

// Функция генерации пароля (необходимо модифицировать
// для указаний параметров генераций, выбора алфавитов)
export function passwordGenerator(size = 8) {
  const alphabet = 'abcdefghijklmnopqrstuvwxyz';
  const alphabetUpper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  const numeric = '0123456789';
  const special = '!@#$%^&*()_+~`|}{[]:;?><,./-=';

  const CharacterSet = alphabet + alphabetUpper + numeric + special;

  let password = '';

  for (let i = 0; i < size - 4; i += 1) {
    password += CharacterSet.charAt(Math.floor(Math.random() * CharacterSet.length));
  }

  password += alphabet.charAt(Math.floor(Math.random() * alphabet.length));
  password += alphabetUpper.charAt(Math.floor(Math.random() * alphabetUpper.length));
  password += numeric.charAt(Math.floor(Math.random() * numeric.length));
  password += special.charAt(Math.floor(Math.random() * special.length));

  password = password.split('');

  // алгоритм Фишера-Йетса для перемешивания символов
  let temp;
  let j;
  for (let i = password.length - 1; i > 0; i -= 1) {
    j = Math.floor(Math.random() * (i + 1));
    temp = password[j];
    password[j] = password[i];
    password[i] = temp;
  }

  password = password.join('');

  return password;
}

// Форматирование байтов в другие размеры
export function formatBytes(bytes, decimals = 2, power = null) {
  if (bytes === 0) return { number: 0, measure: 'Bytes' };

  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
  let i = 0;

  if (power) {
    i = power;
  } else {
    i = Math.floor(Math.log(bytes) / Math.log(k));
  }

  return { number: parseFloat((bytes / (k ** i)).toFixed(dm)), measure: sizes[i] };
}

export function dateDiffNow(date, period) {
  if (moment().diff(date, 'days') <= -period) {
    return false;
  }
  return true;
}

const API_ID = 5747691; // код свой;

export function injectVKOpenApi() {
  return new Promise((resolve, reject) => {
    try {
      const fjs = document.getElementsByTagName('script')[0];
      if (document.getElementById('vk_openapi_js')) {
        resolve();
        return;
      }
      const js = document.createElement('script');
      js.id = 'vk_openapi_js';
      js.src = '//vk.com/js/api/openapi.js?162';
      js.onload = resolve;
      js.onerror = reject;

      fjs.parentNode.insertBefore(js, fjs);
    } catch (err) {
      reject(err);
    }
  });
}

/* global VK */
export const initVK = (onlyWidgets = false) => () => VK.init({ apiId: API_ID, onlyWidgets });
