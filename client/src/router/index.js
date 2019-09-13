import Vue from 'vue';
import Router from 'vue-router';
import NProgress from 'nprogress';
import Activation from '@/components/Activation';
import Users from '@/components/Users';
import Roles from '@/components/Roles';
import Login from '@/components/Login';
import Dashboard from '@/components/Dashboard';
import AdminPanel from '@/components/AdminPanel';
import Profile from '@/components/Profile';
import Index from '@/components/Index';
import store from '@/store';
import { i18n } from '@/utils';

Vue.use(Router);

// Объявление роутера с маршрутами
const router = new Router({
  saveScrollPosition: true,
  linkExactActiveClass: 'active',
  routes: [
    {
      path: '/admin-panel',
      component: AdminPanel,
      meta: {
        requiresAuth: true,
        breadCrumb: 'home',
        title: 'CMS',
      },
      children: [
        {
          path: 'dashboard',
          name: 'Dashboard',
          component: Dashboard,
          meta: {
            requiresAuth: true,
            breadCrumb: 'dashboard',
            title: 'CMS - Главная панель',
          },
        },
        {
          path: 'users',
          name: 'Users',
          component: Users,
          meta: {
            requiresAuth: true,
            breadCrumb: 'users',
            title: 'CMS - Оргсовет',
          },
        },
        {
          path: 'profile',
          name: 'UserProfile',
          component: Profile,
          meta: {
            requiresAuth: true,
            breadCrumb: 'userProfile',
            title: 'CMS - Досье',
          },
        },
        {
          path: 'roles',
          name: 'Roles',
          component: Roles,
          meta: {
            requiresAuth: true,
            breadCrumb: 'permissions',
            title: 'CMS - Полномочия',
          },
        },
        {
          path: '',
          component: Dashboard,
        },
      ],
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
      meta: {
        title: 'Авторизация',
      },
      beforeEnter(to, from, next) {
        if (store.getters.isAuthenticated) {
          if (to.query.redirect) {
            next(to.query.redirect);
          } else {
            next('/admin-panel/dashboard');
          }
        } else {
          next();
        }
      },
    },
    {
      path: '/verify/mail/:token',
      name: 'Activation',
      component: Activation,
      props: true,
      meta: {
        title: 'Верификация почты',
      },
    },
    {
      path: '/index',
      name: 'Index',
      component: Index,
      meta: {
        title: 'Главная',
      },
    },
    {
      path: '*',
      component: Index,
      beforeEnter(to, from, next) {
        next('/index');
      },
    },
  ],
  mode: 'history',
});

// Перед каждым переходом проверять, требуется ли аутентификация для маршрута,
// если да, то проверить статус аутентификации,
// если не аутентифицирован, редирект на логин, иначе перейти по маршруту
router.beforeEach((to, from, next) => {
  document.title = `ЦГАКО - ${to.meta.title}`;
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!store.getters.isAuthenticated) {
      next({
        path: '/login',
        query: {
          redirect: to.fullPath,
        },
      });
    } else {
      store.state.uid = store.getters.currentUser;
      store.dispatch('loadProfile');
      next();
    }
  } else {
    store.dispatch('loadProfile');
    next();
  }
  import(`../langs/${store.state.locale}.json`).then((msgs) => {
    i18n.setLocaleMessage(`${store.state.locale}`, msgs);
    i18n.locale = store.state.locale;
    store.dispatch('presetLocale', store.state.locale);
  });
});

// Перед загрузкой страницы старт прогресс-бара
router.beforeResolve((to, from, next) => {
  if (to.name) {
    NProgress.start();
  }
  next();
});

// После загрузки завершить отсчет прогресс-бара
// eslint-disable-next-line
router.afterEach((to, from) => {
  NProgress.done();
});

export default router;
