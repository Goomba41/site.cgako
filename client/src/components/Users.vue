<template>
  <main class="container-fluid">
    <breadcumbs></breadcumbs>

    <b-row class="pb-4 m-0 w-100">
      <b-col align-self="start" class="text-center">
        <b-row class="justify-content-start align-middle align-items-center">
          <span class="text-info pr-3">
            Всего {{ users.count }}
            {{ users.count | declension(["товарищ", "товарища", "товарищей"]) }}
          </span>
          <button type="button" title="Новое досье" class="btn btn-success btn-sm mr-1">
            <font-awesome-icon icon="plus" fixed-width />
          </button>
          <b-dropdown size="sm" class="mr-1"
          v-bind:disabled="!selected.length"
          v-bind:class="!selected.length">
            <template slot="button-content">
              <font-awesome-icon icon="list" fixed-width />
            </template>
            <b-dropdown-item disabled>
              <font-awesome-icon icon="trash" fixed-width />
              Удалить
            </b-dropdown-item>
            <b-dropdown-item disabled>
              <font-awesome-icon icon="power-off" fixed-width />
              Отключить
            </b-dropdown-item>
            <b-dropdown-item disabled>
              <font-awesome-icon icon="key" fixed-width />
              Блокировать пароль
            </b-dropdown-item>
          </b-dropdown>
        </b-row>
      </b-col>

      <b-col sm="4" class="text-center">
        <b-row class="justify-content-center align-middle align-items-center">
          <b-col sm="6">
            <b-input-group :append="'/ ' + users.pages + ' cтраниц'" size="sm">
              <b-form-input type="number" min=1 :max="users.pages"
              autocomplete="off"
              v-model="listControl.page"
              v-on:input="listBegin(); listChange()"/>
            </b-input-group>
          </b-col>
        </b-row>
      </b-col>

      <b-col sm="4" class="text-center">
        <b-row class="justify-content-end align-middle align-items-center">
          <b-col sm="6">
            <b-input-group prepend="Показывать:" size="sm">
              <b-form-input type="number" min=1 :max="users.count - listControl.start + 1"
              autocomplete="off"
              v-model="listControl.limit"
              v-on:input="listChange(); listControl.page = 1"/>
            </b-input-group>
          </b-col>
          <b-col sm="6">
            <b-input-group prepend="Начать с:" size="sm">
              <b-form-input type="number" min=1 :max="users.count"
              autocomplete="off"
              v-model="listControl.start"
              v-on:input="listRows(); listChange()"/>
            </b-input-group>
          </b-col>
        </b-row>
      </b-col>

    </b-row>

    <div class="row-fluid pb-3">
      <table class="table table-hover td-align-middle">
        <thead>
          <tr class="text-center">
            <th scope="col"><input type="checkbox" v-model="selectAll" @click="select"></th>
            <th scope="col">Статус</th>
            <th scope="col">Фотокарточка</th>
            <th scope="col">
              Пользователь
              <font-awesome-icon icon="sort"
              fixed-width
              @click="listControl.orderBy.field='surname';
              listControl.orderBy.asc=!listControl.orderBy.asc"/>
              </th>
            <th scope="col">Роль</th>
            <th scope="col">Cоц. сети</th>
            <th scope="col">
              Последний вход
              <font-awesome-icon icon="sort"
              fixed-width
              @click="listControl.orderBy.field='last_login';
              listControl.orderBy.asc=!listControl.orderBy.asc"/>
            </th>
            <th scope="col">Управление</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in orderedList" v-bind:key="user.id">
            <td><input type="checkbox" :value="user.id" v-model="selected"></td>
            <td class="column">
              <font-awesome-icon icon="shield-alt"
              fixed-width title="Подтверждение учетной записи" />
              <font-awesome-icon icon="power-off"
              fixed-width title="Отключить учетную запись" />
              <font-awesome-icon icon="key"
              fixed-width title="Пароль учетной записи" />
            </td>
            <td>
              <div class="card-profile-image mx-auto">
                <img v-if="user.photo" :src="'/static/profile_avatars/'+user.photo"
                alt="Фотокарточка" class="profile-image">
                <img v-else :src="'/static/profile_avatars/default.png'"
                alt="Фотокарточка" class="profile-image">
              </div>
            </td>
            <td v-bind:title="`${user.surname} ${user.name} ${user.patronymic}`">
              {{user.surname}} {{user.name.charAt(0)}}.{{user.patronymic.charAt(0)}}.
              <br><b>@{{user.login}}</b>
            </td>
            <td>Администратор</td>
            <td>
              <font-awesome-icon :icon="['fab', 'vk']" fixed-width />
              <font-awesome-icon :icon="['fab', 'odnoklassniki']" fixed-width />
              <font-awesome-icon :icon="['fab', 'yandex']" fixed-width />
              <font-awesome-icon :icon="['fab', 'google']" fixed-width />
            </td>
            <td v-bind:title="user.last_login |
            moment('subtract', '3 hours', 'dddd, MMMM Do YYYY, HH:mm:ss')">
              {{user.last_login | moment('subtract', '3 hours', 'from')}}
            </td>
            <td>
              <b-button size="sm" title="Изменить досье" variant="warning" v-b-modal.password-modal>
                <font-awesome-icon :icon="['fa', 'pencil-alt']" fixed-width />
              </b-button>
              <b-button size="sm" title="Удалить товарища" variant="danger">
                <font-awesome-icon :icon="['fa', 'trash']" fixed-width />
              </b-button>
              <b-button size="sm" title="Экстренная связь" variant="info" v-b-modal.contacts-modal
              @click="selectUser(user.id)">
                <font-awesome-icon :icon="['fa', 'info']" fixed-width />
              </b-button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <b-modal id="contacts-modal"
            title="Экстренная связь"
            hide-footer size="sm" centered
            header-bg-variant="info"
            header-text-variant="light">
      <p>
        <a :href="`mailto:${this.user.email}`" title="Написать на электронную почту">
          <font-awesome-icon :icon="['fa', 'at']" fixed-width /> {{this.user.email}}
        </a>
      </p>
      <p>
        <font-awesome-icon :icon="['fa', 'phone']" fixed-width />
        {{this.user.phone}}
      </p>
    </b-modal>

  </main>
</template>

<script>
import { mapState } from 'vuex';
import _ from 'lodash';
import Breadcumbs from './Breadcumbs';

export default {
  name: 'Users',
  data() {
    return {
      user: {},
      selected: [],
      selectAll: false,
      listControl: {
        page: 1,
        start: 1,
        limit: 20,
        orderBy: {
          field: 'surname',
          asc: true,
        },
      },
    };
  },
  components: { Breadcumbs },
  computed: mapState({
    users: state => state.users,
    orderedList() {
      return _.orderBy(this.users.results,
        this.listControl.orderBy.field,
        this.listControl.orderBy.asc ? 'asc' : 'desc');
    },
  }),
  beforeMount() {
    this.$store.dispatch('loadUsers', { start: this.listControl.start, limit: this.listControl.limit });
  },
  methods: {
    select() {
      this.selected = [];
      if (!this.selectAll) {
        for (let i = 0; i < this.users.results.length; i += 1) {
          this.selected.push(this.users.results[i].id);
        }
      }
    },
    selectUser(id) {
      this.user = _.find(this.users.results, { id });
    },
    listRows() {
      // Просчет количества показываемых строк в зависимости от индекса начальной
      const newLimit = parseInt(parseInt(this.users.count, 10)
      - parseInt(this.listControl.start, 10) + 1, 10);
      const limit = parseInt(this.listControl.limit, 10);
      if (limit > newLimit) {
        this.listControl.limit = newLimit;
      }
    },
    listBegin() {
      /* Расчет новой начальной строки в зависимости от выбранной страницы
      Получаем индекс последней строки на странице
      Затем для получения индекса первой строки страницы
      вычитаем количество ненужных строк (из количества на странице - сама строка) */
      const newBegin = parseInt(parseInt(this.listControl.limit, 10)
      * parseInt(this.listControl.page, 10) - (parseInt(this.listControl.limit - 1, 10)), 10);
      if (newBegin > this.users.count) {
        this.listControl.start = this.users.count;
      } else {
        this.listControl.start = newBegin;
      }
    },
    listChange() {
      this.$store.dispatch('loadUsers', { start: this.listControl.start, limit: this.listControl.limit });
    },
  },
};
</script>
