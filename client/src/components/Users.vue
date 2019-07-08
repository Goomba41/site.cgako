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
            <b-dropdown-item variant="danger" v-b-modal.delete-group-modal>
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
            <th scope="col">
              <b-form-checkbox v-model="selectAll" @change="select"></b-form-checkbox>
            </th>
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
            <td>
              <b-form-checkbox
                v-if="uid != user.id"
                v-model="selected"
                :value="user.id"></b-form-checkbox>
            </td>
            <td class="column">
              <font-awesome-icon icon="shield-alt"
              fixed-width title="Подтверждение учетной записи" />
              <font-awesome-icon icon="power-off"
              fixed-width title="Отключить учетную запись" />
<!--
              <b-form-checkbox v-model="user.status" name="status" switch>
              </b-form-checkbox>
-->
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
            <td v-bind:title="user.last_login && user.last_login.datetime ?
            $options.filters.moment(user.last_login.datetime, 'dddd, MMMM Do YYYY, HH:mm:ss') :
            'Не входил'">
              {{user.last_login && user.last_login.datetime ?
                $options.filters.moment(user.last_login.datetime, 'from') : 'Не входил'}}
              <br>
              {{user.last_login && user.last_login.ip ?
                user.last_login.ip : ''}}
              <font-awesome-icon v-if="user.last_login && user.last_login.agent"
              :icon="['far', 'window-maximize']" fixed-width
              v-bind:title="user.last_login && user.last_login.browser ?
                user.last_login.browser : 'Неизвестный браузер'"/>

              <font-awesome-icon v-if="user.last_login && user.last_login.device
              && user.last_login.device==='pc'"
              v-bind:icon="['fa', 'desktop']" fixed-width
              v-bind:title="user.last_login && user.last_login.device ?
                'Компьютер': 'Неизвестное устройство'"/>
              <font-awesome-icon v-else-if="user.last_login && user.last_login.device
              && user.last_login.device==='tablet'"
              v-bind:icon="['fa', 'tablet-alt']" fixed-width
              v-bind:title="user.last_login && user.last_login.device ?
                'Планшет' : 'Неизвестное устройство'"/>
              <font-awesome-icon v-else-if="user.last_login && user.last_login.device
              && user.last_login.device==='mobile'"
              v-bind:icon="['fa', 'mobile-alt']" fixed-width
              v-bind:title="user.last_login && user.last_login.device ?
                'Телефон' : 'Неизвестное устройство'"/>

              <font-awesome-icon v-if="user.last_login && user.last_login.os
              && user.last_login.os.includes('Windows')"
              v-bind:icon="['fab', 'windows']" fixed-width
              class="text-primary"
              v-bind:title="user.last_login && user.last_login.os ?
                user.last_login.os: 'Неизвестное устройство'"/>
              <font-awesome-icon v-else-if="user.last_login && user.last_login.os
              && user.last_login.os.includes('Mac')"
              v-bind:icon="['fab', 'apple']" fixed-width
              v-bind:title="user.last_login && user.last_login.os ?
                user.last_login.os : 'Неизвестное устройство'"/>
              <font-awesome-icon v-else-if="user.last_login && user.last_login.os"
              v-bind:icon="['fab', 'linux']" fixed-width
              v-bind:title="user.last_login && user.last_login.os ?
                user.last_login.os : 'Неизвестное устройство'"/>

            </td>
            <td>
              <b-button size="sm" title="Изменить досье" variant="warning">
                <font-awesome-icon :icon="['fa', 'pencil-alt']" fixed-width />
              </b-button>

              <b-button size="sm" title="Экстренная связь" variant="info" v-b-modal.contacts-modal
              @click="selectUser(user.id)">
                <font-awesome-icon :icon="['fa', 'info']" fixed-width />
              </b-button>

              <b-button v-if="uid != user.id"
              size="sm" title="Уничтожить досье" variant="danger"
              @click="selectUser(user.id)"
              v-b-modal.delete-modal>
                <font-awesome-icon :icon="['fa', 'trash']" fixed-width />
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
      <p v-for="mail in this.user.email" v-bind:key="mail.value">
        <a v-if="mail.value" :href="`mailto:${mail.value}`" title="Написать на эту почту">
          <font-awesome-icon :title="'Личная почта'"
          v-if="mail.type==='personal'"
          v-bind:icon="['fa', 'user']" fixed-width/>
          <font-awesome-icon :title="'Основная почта'"
          v-else-if="mail.type==='primary'"
          v-bind:icon="['fa', 'at']" fixed-width/>
          <font-awesome-icon :title="'Рабочая почта'"
          v-else-if="mail.type==='work'"
          v-bind:icon="['fa', 'briefcase']" fixed-width/>
          <font-awesome-icon
          :title="mail.verified ? 'Подтверждена' : 'Не подтверждена'"
          v-bind:icon="['fa', 'check-circle']"
          :class="mail.verified ? 'text-success' : 'text-danger'" fixed-width/>
          {{mail.value}}
        </a>
      </p>
      <p>
        <font-awesome-icon :icon="['fa', 'phone']" fixed-width class="text-primary"/>
        {{this.user.phone}}
      </p>
    </b-modal>

    <b-modal id="delete-modal"
            @show="deletePassphrase=''"
            @hidden="deletePassphrase=''"
            @close="deletePassphrase=''"
             title="Уничтожение досье"
             hide-footer size="sm" centered
            :header-bg-variant="'danger'"
            :header-text-variant="'light'">

      <b-form class="w-100" @submit.prevent="deleteUser(user.id)">

        <b-form-group
        description="Введите позывной товарища, чтобы подтвердить утичтожение">
          <b-input-group>

            <b-form-input
              name="confirmation-passphrase"
              autofocus
              v-model="$v.deletePassphrase.$model"
              placeholder="Подтверждающая фраза"
              :state="$v.deletePassphrase.$dirty ? !$v.deletePassphrase.$error : null"
              @input="$v.deletePassphrase.$touch()">
            </b-form-input>
          </b-input-group>

        </b-form-group>
        <b-button type="submit" block
        variant="danger" title="Уничтожить досье товарища"
        :disabled="!$v.deletePassphrase.$anyDirty || $v.deletePassphrase.$invalid">
          <font-awesome-icon :icon="['fa', 'trash']" fixed-width />
        </b-button>

        <div class="row mx-auto pl-3 pr-3 pt-3 border-top">
          <span class="text-danger notation text-center">
              <font-awesome-icon :icon="['fa', 'exclamation-triangle']"
              size="1x" fixed-width />
  После удаления товарищ не сможет взаимодействовать с сайтом!
          </span>
        </div>

      </b-form>
    </b-modal>

    <b-modal id="delete-group-modal"
            @show="deleteGroupPassphrase=''"
            @hidden="deleteGroupPassphrase=''"
            @close="deleteGroupPassphrase=''"
             title="Уничтожение досье"
             hide-footer size="sm" centered
            :header-bg-variant="'danger'"
            :header-text-variant="'light'">

      <b-form class="w-100" @submit.prevent="deleteUser(selected)">
        <b-form-group
        description="Введите слово 'Удалить', чтобы подтвердить утичтожение">
          <b-input-group>

            <b-form-input
              name="confirmation-passphrase"
              autofocus
              v-model="$v.deleteGroupPassphrase.$model"
              placeholder="Подтверждающая фраза"
              :state="$v.deleteGroupPassphrase.$dirty ? !$v.deleteGroupPassphrase.$error : null"
              @input="$v.deleteGroupPassphrase.$touch()">
            </b-form-input>
          </b-input-group>

        </b-form-group>
        <b-button type="submit" block
        variant="danger" title="Уничтожить пачку досье"
        :disabled="!$v.deleteGroupPassphrase.$anyDirty || $v.deleteGroupPassphrase.$invalid">
          <font-awesome-icon :icon="['fa', 'trash']" fixed-width />
        </b-button>

        <div class="row mx-auto pl-3 pr-3 pt-3 border-top">
          <span class="text-danger notation text-center">
              <font-awesome-icon :icon="['fa', 'exclamation-triangle']"
              size="1x" fixed-width />
  После удаления товарищи не смогут взаимодействовать с сайтом!
          </span>
        </div>

      </b-form>
    </b-modal>

  </main>
</template>

<script>
import { mapState } from 'vuex';
import _ from 'lodash';
import {
  required, sameAs,
} from 'vuelidate/lib/validators';
import Breadcumbs from './Breadcumbs';


export default {
  name: 'Users',
  data() {
    return {
      user: {},
      deletePassphrase: '',
      deleteGroupPassphrase: '',
      selected: [],
      selectAll: false,
      listControl: {
        page: 1,
        start: 1,
        limit: 20,
        orderBy: {
          field: 'id',
          asc: true,
        },
      },
    };
  },
  validations: {
    deletePassphrase: {
      required,
      sameAsLogin: sameAs(function sameLogin() {
        return this.user.login;
      }),
    },
    deleteGroupPassphrase: {
      required,
      sameAsPassphrase: sameAs(() => 'Удалить'),
    },
  },
  components: { Breadcumbs },
  computed: mapState({
    users: state => state.users,
    uid: state => state.uid,
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
          if (this.uid !== this.users.results[i].id) {
            this.selected.push(this.users.results[i].id);
          }
        }
      }
    },
    deleteUser(id) {
      if (Array.isArray(id)) {
        for (let i = 0; i < id.length; i += 1) {
          this.$store.dispatch('deleteUser', { id: id[i] });
        }
      } else if (!Number.isNaN(id)) {
        this.$store.dispatch('deleteUser', { id });
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
