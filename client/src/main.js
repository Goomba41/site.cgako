// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import 'vue-tel-input/dist/vue-tel-input.css';
import 'vue-multiselect/dist/vue-multiselect.min.css';

import BootstrapVue from 'bootstrap-vue';
import BootstrapVueTreeview from 'bootstrap-vue-treeview';
import Vuelidate from 'vuelidate';
import VueLodash from 'vue-lodash';
import FlagIcon from 'vue-flag-icon';
import LoadScript from 'vue-plugin-load-script';
import UUID from 'vue-uuid';

// import jQuery from 'jquery';

// import '../static/js/jquery.min';
// import '../static/js/jquery.scrollex.min';
// import '../static/js/jquery.scrolly.min';
// import '../static/js/browser.min';
// import '../static/js/breakpoints.min';
// import '../static/js/util';
// import '../static/js/main';
// import '../static/js/to-top';
// import '../static/js/anchors';
// import '../static/js/search';
// import '../static/js/underscore-min';
// import '../static/js/moment-with-locales';
// import '../static/js/clndr';
// import '../static/js/slider';
// import '../static/js/sticky-nav';

// Импортирование fontawesome и отдельных иконок из него
import { library } from '@fortawesome/fontawesome-svg-core';
import {
  faTrash, faPencilAlt, faInfo, faPlus, faPowerOff, faShieldAlt, faUser, faLock,
  faExclamationTriangle, faSignInAlt, faSignOutAlt, faQuestion, faUserShield,
  faBars, faBell, faCog, faUserCircle, faCircle, faSearch, faThLarge, faFolder, faGlobeEurope,
  faChevronDown, faNewspaper, faAt, faSyncAlt, faHeart, faSave, faKey, faTimes, faUpload, faCheck,
  faListOl, faListUl, faList, faUsers, faSort, faPhone, faBan, faDesktop, faMobileAlt, faTabletAlt,
  faBriefcase, faClock, faCheckCircle, faEnvelope, faIdCard, faUserCheck, faHome, faFileImage,
  faLanguage, faLongArrowAltRight, faProjectDiagram, faAddressBook, faMoneyCheckAlt,
  faBusinessTime, faBuilding,
} from '@fortawesome/free-solid-svg-icons';
import {
  faCopyright as farCopyright, faEye as farEye, faEyeSlash as farEyeSlash, faEdit as farEdit,
  faWindowMaximize as farWindowMaximize, faFile as farFile,
} from '@fortawesome/free-regular-svg-icons';
import {
  faVk, faYandex, faOdnoklassniki, faGoogle, faGithub, faTrello,
  faLinux, faWindows, faApple,
} from '@fortawesome/free-brands-svg-icons';
import { FontAwesomeIcon, FontAwesomeLayers, FontAwesomeLayersText } from '@fortawesome/vue-fontawesome';

import Vue from 'vue';
import App from './App';
import router from './router';
import store from './store';

import { i18n } from '@/utils';

// Добавление иконок в библиотеку
library.add(faTrash, faPencilAlt, faInfo, faPlus, faPowerOff,
  faShieldAlt, faVk, faYandex, faOdnoklassniki, faGoogle, faUser, faLock,
  faExclamationTriangle, faSignInAlt, faSignOutAlt, faQuestion,
  faUserShield, faBars, faGithub, faBell, faTrello, faCog, faUserCircle,
  faCircle, faSearch, faThLarge, faFolder, faGlobeEurope, faChevronDown, faNewspaper,
  faAt, farCopyright, faSyncAlt, faHeart, faSave, faKey, faTimes, farEye, farEyeSlash,
  faUpload, farEdit, faCheck, faListOl, faListUl, faList, faUsers, faSort, faPhone,
  faBan, farWindowMaximize, faDesktop, faTabletAlt, faMobileAlt, faLinux, faWindows,
  faApple, faBriefcase, faClock, faCheckCircle, faEnvelope, farFile, faIdCard, faUserCheck,
  faHome, faFileImage, faLanguage, faLongArrowAltRight, faProjectDiagram, faAddressBook,
  faMoneyCheckAlt, faBusinessTime, faBuilding);
Vue.component('font-awesome-icon', FontAwesomeIcon);
Vue.component('font-awesome-layers', FontAwesomeLayers);
Vue.component('font-awesome-layers-text', FontAwesomeLayersText);

Vue.config.productionTip = false;

Vue.use(BootstrapVue);
Vue.use(BootstrapVueTreeview);
Vue.use(VueLodash);
Vue.use(Vuelidate);
Vue.use(FlagIcon);
Vue.use(LoadScript);
Vue.use(UUID);

// window.jQuery = jQuery;
// window.$ = jQuery;

// Объявление moment.js с русской локалью
const moment = require('moment');
require('moment/locale/ru');

Vue.use(require('vue-moment'), {
  moment,
});

// Фильтр для обработки склонений чисел
Vue.filter('declension', (value, words) => {
  if (!value) return '';

  let word;
  let iinumber;
  const inumber = value % 100;

  if (inumber >= 11 && inumber <= 19) {
    word = words['2'];
  } else {
    iinumber = inumber % 10;
    if (iinumber === 1) {
      word = words['0'];
    } else if (iinumber === 2 || iinumber === 3 || iinumber === 4) {
      word = words['1'];
    } else {
      word = words['2'];
    }
  }
  return word;
});

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  i18n,
  components: { App },
  template: '<App/>',
});
