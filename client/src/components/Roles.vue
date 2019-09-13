<template>
  <main class="container-fluid d-flex flex-column">
    <breadcumbs></breadcumbs>

    <b-row class="pb-4 m-0 w-100 flex-grow-1 blocker"
    v-if="!can(user_perms, 'get', 'roles')">
      <b-col class="align-self-center text-center">
        <font-awesome-icon :icon="['fa', 'lock']" fixed-width size="10x"/>
      </b-col>
    </b-row>

    <b-row class="pb-4 m-0 w-100" v-if="can(user_perms, 'get', 'roles')">
      <b-col align-self="start" class="text-center" sm="8">
        <b-row class="justify-content-start align-middle align-items-center">
          <span class="text-info pr-3">
            {{ $tc('rolesPermissions.counter', roles.count) }}
          </span>

          <b-button v-bind:title="$t('rolesPermissions.tooltips.newRoleButton')"
          v-if="can(user_perms, 'post', 'roles')"
          v-b-tooltip.hover class="mr-1" size="sm" variant="success"
          v-b-modal.new-modal>
            <font-awesome-icon icon="plus" fixed-width />
          </b-button>
          <b-button v-else class="mr-1"
          size="sm" v-bind:title="$t('rolesPermissions.tooltips.newRoleButton')"
          v-b-tooltip.hover>
            <font-awesome-icon :icon="['fa', 'lock']" fixed-width />
          </b-button>

          <b-dropdown size="sm" class="mr-1"
          v-bind:disabled="!selected.length"
          v-bind:class="!selected.length">
            <template slot="button-content">
              <font-awesome-icon icon="list" fixed-width />
            </template>
            <b-dropdown-item variant="danger" v-b-modal.delete-group-modal
            v-if="can(user_perms, 'delete', 'roles')">
              <font-awesome-icon icon="trash" fixed-width />
              {{ $t('rolesPermissions.titles.groupActions.deleteButton') }}
            </b-dropdown-item>
            <b-dropdown-item variant="dark"
            v-else>
              <font-awesome-icon icon="lock" fixed-width />
              {{ $t('rolesPermissions.titles.groupActions.deleteButton') }}
            </b-dropdown-item>
          </b-dropdown>
        </b-row>
      </b-col>

      <b-col sm="4" class="text-center">
        <b-row class="justify-content-end align-middle align-items-center">
          <b-col sm="4">
            <b-input-group :append="'/ ' + roles.pages" size="sm"
             v-bind:title="$t('rolesPermissions.tooltips.pageNavigation')"
             v-b-tooltip.hover>
              <b-form-input type="number" min=1 :max="roles.pages"
              autocomplete="off"
              v-model="listControl.page"
              v-on:input="listBegin(); listChange()"/>
            </b-input-group>
          </b-col>
          <b-col sm="4">
            <b-input-group :prepend="$t('rolesPermissions.tooltips.pageShowCountTitle')" size="sm"
             v-bind:title="$t('rolesPermissions.tooltips.pageShowCount')"
             v-b-tooltip.hover>
              <b-form-input type="number" min=1 :max="roles.count - listControl.start + 1"
              autocomplete="off"
              v-model="listControl.limit"
              v-on:input="listChange(); listControl.page = 1"/>
            </b-input-group>
          </b-col>
<!--
          <b-col sm="4">
            <b-input-group :prepend="$t('rolesPermissions.tooltips.pageShowFromTitle')" size="sm"
             v-bind:title="$t('rolesPermissions.tooltips.pageShowFrom')"
             v-b-tooltip.hover>
              <b-form-input type="number" min=1 :max="roles.count"
              autocomplete="off"
              v-model="listControl.start"
              v-on:input="listRows(); listChange()"/>
            </b-input-group>
          </b-col>
-->
        </b-row>
      </b-col>

    </b-row>

    <b-row class="p-3 justify-content-center" v-if="can(user_perms, 'get', 'roles')">
      <b-col sm="6">

        <table class="table table-hover td-align-middle">
          <thead>
            <tr class="text-center">
              <th scope="col">
                <b-form-checkbox v-model="selectAll" @change="select"></b-form-checkbox>
              </th>

              <th scope="col">
                {{ $t('rolesPermissions.titles.role') }}
                <font-awesome-icon icon="sort"
                fixed-width
                @click="listControl.orderBy.field='title';
                listControl.orderBy.asc=!listControl.orderBy.asc"/>
                </th>

              <th scope="col">{{ $t('rolesPermissions.titles.management') }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="role in orderedList" v-bind:key="role.id">
              <td>
                <b-form-checkbox
                  v-model="selected"
                  v-if="role.deletable"
                  :value="role.id"></b-form-checkbox>
              </td>
              <td>
                {{role.title}}
              </td>
              <td class="text-center">
                <b-button size="sm"
                v-bind:title="$t('rolesPermissions.tooltips.editRoleButton')"
                v-b-tooltip.hover variant="primary"
                v-if="can(user_perms, 'put', 'roles') && role.editable"
                v-b-modal.edit-modal @click="selectRole(role.id)">
                  <font-awesome-icon :icon="['fa', 'pencil-alt']" fixed-width />
                </b-button>
                <b-button v-else
                size="sm" v-bind:title="$t('usersCMS.tooltips.editButton')"
                v-b-tooltip.hover>
                  <font-awesome-icon :icon="['fa', 'lock']" fixed-width />
                </b-button>

                <b-button
                size="sm" variant="danger"
                v-bind:title="$t('rolesPermissions.tooltips.deleteRoleButton')"
                v-if="can(user_perms, 'delete', 'roles') && role.deletable"
                v-b-tooltip.hover
                @click="selectRole(role.id)"
                v-b-modal.delete-modal>
                  <font-awesome-icon :icon="['fa', 'trash']" fixed-width />
                </b-button>
                </b-button>
                <b-button v-else
                size="sm" v-bind:title="$t('rolesPermissions.tooltips.deleteRoleButton')"
                v-b-tooltip.hover>
                  <font-awesome-icon :icon="['fa', 'lock']" fixed-width />
                </b-button>

              </td>
            </tr>
          </tbody>
        </table>

      </b-col>
    </b-row>

    <b-modal id="delete-modal"
    v-if="can(user_perms, 'get', 'roles')"
    @show="deletePassphrase=''"
    @hidden="deletePassphrase=''"
    @close="deletePassphrase=''"
    v-bind:title="$t('rolesPermissions.deleteModal.title')"
     v-b-tooltip.hover
     hide-footer size="sm" centered
    :header-bg-variant="'danger'"
    :header-text-variant="'light'">

      <b-form class="w-100" @submit.prevent="deleteRole(role.id)">

        <b-form-group
        :description="$t('rolesPermissions.deleteModal.confirmationField.description')">
          <b-input-group>

            <b-form-input
              name="confirmation-passphrase"
              autofocus
              v-model="$v.deletePassphrase.$model"
              v-bind:placeholder="$t('rolesPermissions.deleteModal.confirmationField.placeholder')"
              :state="$v.deletePassphrase.$dirty ? !$v.deletePassphrase.$error : null"
              @input="$v.deletePassphrase.$touch()">
            </b-form-input>
          </b-input-group>

        </b-form-group>
        <b-button type="submit" block
        variant="danger" v-bind:title="$t('rolesPermissions.deleteModal.tooltips.deleteButton')"
        v-b-tooltip.hover
        :disabled="!$v.deletePassphrase.$anyDirty || $v.deletePassphrase.$invalid">
          <font-awesome-icon :icon="['fa', 'trash']" fixed-width />
        </b-button>

<!--
        <div class="row mx-auto pl-3 pr-3 pt-3 border-top">
          <span class="text-danger notation text-center">
              <font-awesome-icon :icon="['fa', 'exclamation-triangle']"
              size="1x" fixed-width />
  После удаления товарищ не сможет взаимодействовать с сайтом!
          </span>
        </div>
-->

      </b-form>
    </b-modal>


    <b-modal id="delete-group-modal"
    v-if="can(user_perms, 'get', 'roles')"
    @show="deleteGroupPassphrase=''"
    @hidden="deleteGroupPassphrase=''"
    @close="deleteGroupPassphrase=''"
    v-bind:title="$t('rolesPermissions.deleteGroupModal.title')"
     v-b-tooltip.hover
     hide-footer size="sm" centered
    :header-bg-variant="'danger'"
    :header-text-variant="'light'">

      <b-form class="w-100" @submit.prevent="deleteRole(selected)">
        <b-form-group
        :description="$t('rolesPermissions.deleteGroupModal.confirmationField.description')">
          <b-input-group>

            <b-form-input
              name="confirmation-passphrase"
              autofocus
              v-model="$v.deleteGroupPassphrase.$model"
              v-bind:placeholder="$t(
                'rolesPermissions.deleteGroupModal.confirmationField.placeholder')"
              :state="$v.deleteGroupPassphrase.$dirty ? !$v.deleteGroupPassphrase.$error : null"
              @input="$v.deleteGroupPassphrase.$touch()">
            </b-form-input>
          </b-input-group>

        </b-form-group>
        <b-button type="submit" block
        variant="danger" v-bind:title="$t(
          'rolesPermissions.deleteGroupModal.tooltips.deleteButton')"
        v-b-tooltip.hover
        :disabled="!$v.deleteGroupPassphrase.$anyDirty || $v.deleteGroupPassphrase.$invalid">
          <font-awesome-icon :icon="['fa', 'trash']" fixed-width />
        </b-button>

<!--
        <div class="row mx-auto pl-3 pr-3 pt-3 border-top">
          <span class="text-danger notation text-center">
              <font-awesome-icon :icon="['fa', 'exclamation-triangle']"
              size="1x" fixed-width />
  После удаления товарищи не смогут взаимодействовать с сайтом!
          </span>
        </div>
-->

      </b-form>
    </b-modal>


    <b-modal id="new-modal"
    v-if="can(user_perms, 'get', 'roles')"
    v-bind:title="$t('rolesPermissions.formNew.formTitle')"
    hide-footer size="md" centered
    :header-bg-variant="'success'"
    :header-text-variant="'light'"
    @hidden="onReset">

      <b-form class="w-100" @submit.prevent="onSubmitNewRole" @reset="onReset">

        <b-form-group>
          <b-form-input name="title"
            type="text"
            autofocus
            v-bind:placeholder="$t('rolesPermissions.formNew.formFields.title.placeholder')"
            trim
            v-model="$v.newRole.title.$model"
            :state="$v.newRole.title.$dirty ? !$v.newRole.title.$error : null"
          ></b-form-input>

          <b-form-invalid-feedback
          :state="$v.newRole.title.$dirty ? !$v.newRole.title.$error : null">
            <span v-if="!$v.newRole.title.required">
              {{$t('rolesPermissions.formNew.formFields.title.errors.required')}}
            </span>
            <span v-if="!$v.newRole.title.minLength">
              {{$t('rolesPermissions.formNew.formFields.title.errors.minLength')}}
            </span>
            <span v-if="!$v.newRole.title.maxLength">
              {{$t('rolesPermissions.formNew.formFields.title.errors.maxLength')}}
            </span>
            <span v-if="!$v.newRole.title.alpha">
              {{$t('rolesPermissions.formNew.formFields.title.errors.alphaNum')}}
            </span>
          </b-form-invalid-feedback>

        </b-form-group>

        <b-form-group>
          <multiselect v-model="$v.newRole.permissions.$model" :options="permissions"
          v-bind:placeholder="$t(
            'rolesPermissions.formNew.formFields.permissions.placeholder')"
          :custom-label="namePermission"
          :multiple="true" :hideSelected="true"
          :close-on-select="false" :clear-on-select="false"
          :preserve-search="true" track-by="id"
          :selectLabel="$t('rolesPermissions.formNew.formFields.permissions.selectLabel')"
          :selectedLabel="$t('rolesPermissions.formNew.formFields.permissions.selectedLabel')"
          :deselectLabel="$t('rolesPermissions.formNew.formFields.permissions.deselectLabel')">
            <template slot="selection" slot-scope="{ values, search, isOpen }">
              <span class="multiselect__single" v-if="values.length &amp;&amp; !isOpen">
                {{ $tc(
                  'rolesPermissions.formNew.formFields.permissions.counter', values.length) }}
              </span>
            </template>
            <span slot="noResult">
              {{$t('rolesPermissions.formNew.formFields.permissions.errors.search')}}
            </span>
          </multiselect>
        </b-form-group>

        <b-row>
          <b-col>
            <b-button type="submit" variant="success" block
            v-bind:title="$t('rolesPermissions.formNew.tooltips.submitButton')"
            v-b-tooltip.hover
            :disabled="!$v.newRole.$anyDirty || $v.newRole.$invalid">
              <font-awesome-icon v-if="!formPending"
              :icon="['fa', 'save']" fixed-width />
              <b-spinner small v-if="formPending"></b-spinner>
            </b-button>
          </b-col>
          <b-col>
            <b-button type="reset" variant="danger" block
            v-bind:title="$t('rolesPermissions.formNew.tooltips.clearButton')"
            v-b-tooltip.hover
            :disabled="!$v.newRole.$anyDirty">
              <font-awesome-icon v-if="!formPending"
              :icon="['fa', 'times']" fixed-width />
              <b-spinner small v-if="formPending"></b-spinner>
            </b-button>
          </b-col>
        </b-row>

<!--
        <div class="row mx-auto mt-3 pl-3 pr-3 pt-3 border-top">
          <span class="text-danger notation text-center">
              <font-awesome-icon :icon="['fa', 'exclamation-triangle']"
              size="1x" fixed-width />
  Авторизационные данные будут отправлены пользователю
  на основную почту. Будьте внимательны при её заполнении,
  чтобы данные для входа не попали в чужие руки!
          </span>
        </div>
-->

      </b-form>

    </b-modal>

    <b-modal id="edit-modal"
    v-if="can(user_perms, 'get', 'roles')"
    @hidden="role={}"
    @close="role={}"
    v-bind:title="$t('rolesPermissions.formEdit.formTitle')"
    hide-footer size="md" centered
    :header-bg-variant="'primary'"
    :header-text-variant="'light'">

      <b-form class="w-100" @submit.prevent="onSubmitUpdateRole">
        <b-row>

          <b-col>
            <b-form-group>
              <b-form-input name="title"
                type="text"
                autofocus
                v-bind:placeholder="$t('rolesPermissions.formEdit.formFields.title.placeholder')"
                trim
                v-model="$v.role.title.$model"
                :state="$v.role.title.$dirty ? !$v.role.title.$error : null"
              ></b-form-input>

              <b-form-invalid-feedback
              :state="$v.role.title.$dirty ? !$v.role.title.$error : null">
                <span v-if="!$v.role.title.required">
                  {{$t('rolesPermissions.formEdit.formFields.title.errors.required')}}
                </span>
                <span v-if="!$v.role.title.minLength">
                  {{$t('rolesPermissions.formEdit.formFields.title.errors.minLength')}}
                </span>
                <span v-if="!$v.role.title.maxLength">
                  {{$t('rolesPermissions.formEdit.formFields.title.errors.maxLength')}}
                </span>
                <span v-if="!$v.role.title.alpha">
                  {{$t('rolesPermissions.formEdit.formFields.title.errors.alpha')}}
                </span>
              </b-form-invalid-feedback>
            </b-form-group>

            <b-form-group>
              <multiselect v-model="$v.role.permissions.$model" :options="permissions"
              v-bind:placeholder="$t(
                'rolesPermissions.formEdit.formFields.permissions.placeholder')"
              :custom-label="namePermission"
              :multiple="true" :hideSelected="true"
              :close-on-select="false" :clear-on-select="false"
              :preserve-search="true" track-by="id"
              :selectLabel="$t('rolesPermissions.formEdit.formFields.permissions.selectLabel')"
              :selectedLabel="$t('rolesPermissions.formEdit.formFields.permissions.selectedLabel')"
              :deselectLabel="$t('rolesPermissions.formEdit.formFields.permissions.deselectLabel')">
                <template slot="selection" slot-scope="{ values, search, isOpen }">
                  <span class="multiselect__single" v-if="values.length &amp;&amp; !isOpen">
                    {{ $tc(
                      'rolesPermissions.formEdit.formFields.permissions.counter', values.length) }}
                  </span>
                </template>
                <span slot="noResult">
                  {{$t('rolesPermissions.formEdit.formFields.permissions.errors.search')}}
                </span>
              </multiselect>
            </b-form-group>
          </b-col>

        </b-row>

        <b-row>
          <b-col>
            <b-button type="submit" variant="primary" block
            v-bind:title="$t('rolesPermissions.formEdit.tooltips.submitButton')"
            v-b-tooltip.hover
            :disabled="!$v.role.$anyDirty || $v.role.$invalid || formPending">
              <font-awesome-icon v-if="!formPending"
              :icon="['fa', 'save']" fixed-width />
              <b-spinner small v-if="formPending"></b-spinner>
            </b-button>
          </b-col>
        </b-row>

<!--
        <div class="row mx-auto mt-3 pl-3 pr-3 pt-3 border-top">
          <span class="text-danger notation text-center">
              <font-awesome-icon :icon="['fa', 'exclamation-triangle']"
              size="1x" fixed-width />
  <b>При сбросе основной почты</b> и выходе из CMS, пользователь больше не сможет войти!
  Будьте осторожны!
          </span>
        </div>
-->

      </b-form>

    </b-modal>

  </main>
</template>

<script>
import { mapState } from 'vuex';
import _ from 'lodash';
import {
  required, sameAs, minLength, maxLength,
} from 'vuelidate/lib/validators';
import Multiselect from 'vue-multiselect';
import Breadcumbs from './Breadcumbs';
import { EventBus, can } from '@/utils';


export default {
  name: 'Roles',
  data() {
    return {
      role: {},
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
      newRole: {
        title: '',
        permissions: [],
      },
      can,
    };
  },
  validations: {
    deletePassphrase: {
      required,
      sameAsTitle: sameAs(function sameTitle() {
        return this.role.title;
      }),
    },
    deleteGroupPassphrase: {
      required,
      sameAsPassphrase: sameAs(function samePassphrase() {
        return this.$t('rolesPermissions.deleteGroupModal.confirmationField.passphrase');
      }),
    },
    newRole: {
      title: {
        required,
        minLength: minLength(4),
        maxLength: maxLength(50),
        alpha: val => /^[а-яёa-zА-ЯЁA-Z0-9\s]*$/i.test(val),
      },
      permissions: {},
    },
    role: {
      title: {
        required,
        minLength: minLength(4),
        maxLength: maxLength(50),
        alpha: val => /^[а-яёa-zА-ЯЁA-Z0-9\s]*$/i.test(val),
      },
      permissions: {},
    },
  },
  components: { Breadcumbs, Multiselect },
  computed: mapState({
    user_perms: state => state.user_perms,
    roles: state => state.roles,
    permissions: state => state.permissions,
    uid: state => state.uid,
    orderedList() {
      return _.orderBy(this.roles.results,
        this.listControl.orderBy.field,
        this.listControl.orderBy.asc ? 'asc' : 'desc');
    },
    formPending: state => state.formPending,
  }),
  beforeMount() {
    if (can(this.user_perms, 'get', 'roles')) {
      this.$store.dispatch('loadRoles', { start: this.listControl.start, limit: this.listControl.limit });
      this.$store.dispatch('loadPermissions');
    }
  },
  methods: {
    namePermission({ actions, objects }) {
      return `${actions.title} «${objects.title}»`;
    },
    select() {
      this.selected = [];
      if (!this.selectAll) {
        for (let i = 0; i < this.roles.results.length; i += 1) {
          if (this.roles.results[i].deletable) {
            this.selected.push(this.roles.results[i].id);
          }
        }
      }
    },
    selectRole(id) {
      this.role = _.find(this.roles.results, { id });
    },
    onReset(evt) {
      evt.preventDefault();
      this.$v.newRole.$reset();

      this.newRole.title = '';

      // Trick to reset/clear native browser form validation state
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
      EventBus.$emit('forceRerender');
    },
    onSubmitNewRole() {
      this.$v.$touch();

      if (!this.$v.newRole.$invalid) {
        this.$store.dispatch('newRole', this.newRole);
      }
    },
    async onSubmitUpdateRole() {
      this.$v.role.$touch();

      if (!this.$v.role.$invalid) {
        await this.$store.dispatch('updateRole', this.role);
        this.$v.role.$reset();
        EventBus.$emit('forceRerender');
      }
    },
    deleteRole(id) {
      if (Array.isArray(id)) {
        for (let i = 0; i < id.length; i += 1) {
          this.$store.dispatch('deleteRole', { id: id[i] });
        }
      } else if (!Number.isNaN(id)) {
        this.$store.dispatch('deleteRole', { id });
      }
    },
    listRows() {
      // Просчет количества показываемых строк в зависимости от индекса начальной
      const newLimit = parseInt(parseInt(this.roles.count, 10)
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
      if (newBegin > this.roles.count) {
        this.listControl.start = this.roles.count;
      } else {
        this.listControl.start = newBegin;
      }
    },
    listChange() {
      this.$store.dispatch('loadRoles', { start: this.listControl.start, limit: this.listControl.limit });
    },
  },
};
</script>
