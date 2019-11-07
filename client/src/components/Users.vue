<template>
  <main class="container-fluid d-flex flex-column">
    <breadcumbs></breadcumbs>

    <b-row class="pb-4 m-0 w-100 flex-grow-1 blocker"
    v-if="!can(user_perms, 'get', 'users')">
      <b-col class="align-self-center text-center">
        <font-awesome-icon :icon="['fa', 'lock']" fixed-width size="10x"/>
      </b-col>
    </b-row>

    <b-row class="pb-4 m-0 w-100" v-if="can(user_perms, 'get', 'users')">
      <b-col align-self="start" class="text-center" sm="8">
        <b-row class="justify-content-start align-middle align-items-center">
          <span class="text-info pr-3">
            {{ $tc('usersCMS.counter', users.count) }}
          </span>

          <b-button v-bind:title="$t('usersCMS.tooltips.newButton')"
          v-b-tooltip.hover class="mr-1" size="sm" variant="success"
          v-b-modal.new-modal v-if="can(user_perms, 'post', 'users')">
            <font-awesome-icon icon="plus" fixed-width />
          </b-button>
          <b-button v-else class="mr-1"
          size="sm" v-bind:title="$t('usersCMS.tooltips.newButton')"
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
            v-if="can(user_perms, 'delete', 'users')">
              <font-awesome-icon icon="trash" fixed-width />
              {{ $t('usersCMS.titles.groupActions.deleteButton') }}
            </b-dropdown-item>
            <b-dropdown-item variant="dark"
            v-else>
              <font-awesome-icon icon="lock" fixed-width />
              {{ $t('usersCMS.titles.groupActions.deleteButton') }}
            </b-dropdown-item>
<!--
            <b-dropdown-item disabled>
              <font-awesome-icon icon="power-off" fixed-width />
              Отключить
            </b-dropdown-item>

            <b-dropdown-item disabled>
              <font-awesome-icon icon="key" fixed-width />
              Блокировать пароль
            </b-dropdown-item>
-->
          </b-dropdown>
        </b-row>
      </b-col>

<!--
      <b-col sm="4" class="text-center">
        <b-row class="justify-content-center align-middle align-items-center">
          <b-col>
            <b-input-group size="sm">
              <b-input-group-text slot="prepend">
                <font-awesome-icon :icon="['fa', 'search']" fixed-width />
              </b-input-group-text>
              <b-form-input type="search"
              title="Найти" v-b-tooltip.hover
              autocomplete="off"
              v-model="searchPhrase"
              v-on:input="searchByText(users.results)"/>
            </b-input-group>
          </b-col>
        </b-row>
      </b-col>
-->

      <b-col sm="4" class="text-center">
        <b-row class="justify-content-end align-middle align-items-center">
          <b-col sm="4">
            <b-input-group :append="'/ ' + users.pages" size="sm"
              v-bind:title="$t('usersCMS.tooltips.pageNavigation')" v-b-tooltip.hover>
              <b-form-input type="number" min=1 :max="users.pages"
              autocomplete="off"
              v-model="listControl.page"
              v-on:input="listBegin(); listChange()"/>
            </b-input-group>
          </b-col>
          <b-col sm="4">
            <b-input-group :prepend="$t('usersCMS.tooltips.pageShowCountTitle')" size="sm"
              v-bind:title="$t('usersCMS.tooltips.pageShowCount')" v-b-tooltip.hover>
              <b-form-input type="number" min=1 :max="users.count - listControl.start + 1"
              autocomplete="off"
              v-model="listControl.limit"
              v-on:input="listChange(); listControl.page = 1"/>
            </b-input-group>
          </b-col>
<!--
          <b-col sm="4">
            <b-input-group :prepend="$t('usersCMS.tooltips.pageShowFromTitle')" size="sm"
              v-bind:title="$t('usersCMS.tooltips.pageShowFrom')" v-b-tooltip.hover>
              <b-form-input type="number" min=1 :max="users.count"
              autocomplete="off"
              v-model="listControl.start"
              v-on:input="listRows(); listChange()"/>
            </b-input-group>
          </b-col>
-->
        </b-row>
      </b-col>

    </b-row>

    <div class="row p-3" v-if="can(user_perms, 'get', 'users')">
      <table class="table table-hover td-align-middle">
        <thead>
          <tr class="text-center">
            <th scope="col">
              <b-form-checkbox v-model="selectAll" @change="select"></b-form-checkbox>
            </th>
            <th scope="col">{{ $t('usersCMS.titles.photo') }}</th>
            <th scope="col">
              {{ $t('usersCMS.titles.user') }}
              <font-awesome-icon icon="sort"
              fixed-width
              @click="listControl.orderBy.field='surname';
              listControl.orderBy.asc=!listControl.orderBy.asc"/>
              </th>
            <th scope="col">{{ $t('usersCMS.titles.permissions') }}</th>
            <th scope="col">{{ $t('usersCMS.titles.socials') }}</th>
            <th scope="col">
              {{ $t('usersCMS.titles.lastLogin') }}
              <font-awesome-icon icon="sort"
              fixed-width
              @click="listControl.orderBy.field='last_login';
              listControl.orderBy.asc=!listControl.orderBy.asc"/>
            </th>
            <th scope="col">{{ $t('usersCMS.titles.management') }}</th>
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
            <td>
              <div class="card-profile-image mx-auto">
                <div  v-if="uid != user.id" class="profile-image-overlay"
                v-b-tooltip.hover
                v-bind:title="$t('usersCMS.tooltips.photoTitle')">
                  <div v-b-modal.avatar-modal v-b-tooltip.hover
                  @click="selectUser(user.id)"
                  v-bind:title="$t('usersCMS.tooltips.photoUpdate')">
                    <font-awesome-icon :icon="['fa', 'upload']" fixed-width />
                  </div>
                  <div v-if="user.photo" v-b-tooltip.hover
                  v-bind:title="$t('usersCMS.tooltips.photoDelete')"
                  @click="deleteAvatar(user.id)">
                    <font-awesome-icon :icon="['fa', 'trash']" fixed-width />
                  </div>
                </div>
                <img v-if="user.photo" :src="'/static/profile_avatars/'+user.photo"
                alt="Фотокарточка" class="profile-image">
                <img v-else :src="'/static/profile_avatars/default.png'"
                alt="Фотокарточка" class="profile-image">
              </div>
            </td>
            <td v-bind:title="`${user.surname} ${user.name} ${user.patronymic}`" v-b-tooltip.hover>
              {{user.surname}} {{user.name.charAt(0)}}.{{user.patronymic.charAt(0)}}.
              <br><b>@{{user.login}}</b>
            </td>
            <td style="max-width:10rem;">
              <b-row class="justify-content-center noselect align-middle align-items-center">
                <b-badge variant="info" class="m-1"
                v-for="role in user.roles" v-bind:key="role.title">
                  {{role.title}}
                </b-badge>
              </b-row>
            </td>
            <td>
              <font-awesome-icon :icon="['fab', 'vk']" fixed-width />
              <font-awesome-icon :icon="['fab', 'odnoklassniki']" fixed-width />
              <font-awesome-icon :icon="['fab', 'yandex']" fixed-width />
              <font-awesome-icon :icon="['fab', 'google']" fixed-width />
            </td>
            <td v-bind:title="user.last_login && user.last_login.datetime ?
            $options.filters.moment(user.last_login.datetime, 'YYYY-MM-DD, HH:mm:ss') :
            'Не входил'" v-b-tooltip.hover>
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
              <span class="weight-100 small text-muted d-block mx-auto" v-if="uid==user.id">
                <i18n path="usersCMS.selfEdit.text">
                  <br slot="break">
                  <router-link slot="link" :to="{ name: 'UserProfile' }">
                    {{$t('usersCMS.selfEdit.linkText')}}
                  </router-link>
                </i18n>
              </span>
              <span v-else>
                <b-button size="sm" v-bind:title="$t('usersCMS.tooltips.editButton')"
                v-if="can(user_perms, 'put', 'users')"
                v-b-tooltip.hover variant="primary"
                v-b-modal.edit-modal @click="selectUser(user.id)"
                :disabled="!(can(user_perms, 'put', 'users'))">
                  <font-awesome-icon :icon="['fa', 'pencil-alt']" fixed-width />
                </b-button>
                <b-button v-else
                size="sm" v-bind:title="$t('usersCMS.tooltips.editButton')"
                v-b-tooltip.hover>
                  <font-awesome-icon :icon="['fa', 'lock']" fixed-width />
                </b-button>

                <b-button size="sm" v-bind:title="$t('usersCMS.tooltips.contactsButton')"
                v-b-tooltip.hover variant="info"
                v-b-modal.contacts-modal
                @click="selectUser(user.id)" v-if="uid!=user.id">
                  <font-awesome-icon :icon="['fa', 'info']" fixed-width />
                </b-button>

                <b-button v-if="can(user_perms, 'delete', 'users')"
                size="sm" v-bind:title="$t('usersCMS.tooltips.deleteButton')"
                variant="danger" v-b-tooltip.hover
                @click="selectUser(user.id)"
                v-b-modal.delete-modal>
                  <font-awesome-icon :icon="['fa', 'trash']" fixed-width />
                </b-button>
                <b-button v-else
                size="sm" v-bind:title="$t('usersCMS.tooltips.deleteButton')"
                v-b-tooltip.hover>
                  <font-awesome-icon :icon="['fa', 'lock']" fixed-width />
                </b-button>

              </span>

            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <b-modal id="contacts-modal"
            @hidden="user={}"
            @close="user={}"
            v-bind:title="$t('usersCMS.contactsModal.title')"
            v-b-tooltip.hover
            hide-footer size="sm" centered
            header-bg-variant="info"
            header-text-variant="light"
            v-if="can(user_perms, 'get', 'users')">
      <p v-for="mail in this.user.email" v-bind:key="mail.value">
        <a v-if="mail.value" :href="`mailto:${mail.value}`"
        v-bind:title="$t('usersCMS.contactsModal.tooltips.sendMail')"
        v-b-tooltip.hover>
          <font-awesome-icon v-bind:title="$t('usersCMS.contactsModal.tooltips.private')"
          v-b-tooltip.hover
          v-if="mail.type==='personal'"
          v-bind:icon="['fa', 'user']" fixed-width/>
          <font-awesome-icon v-bind:title="$t('usersCMS.contactsModal.tooltips.primary')"
          v-b-tooltip.hover
          v-else-if="mail.type==='primary'"
          v-bind:icon="['fa', 'at']" fixed-width/>
          <font-awesome-icon v-bind:title="$t('usersCMS.contactsModal.tooltips.work')"
          v-b-tooltip.hover
          v-else-if="mail.type==='work'"
          v-bind:icon="['fa', 'briefcase']" fixed-width/>
          <font-awesome-icon
          :title="mail.verified ? $t('usersCMS.contactsModal.tooltips.verifiedT')
          : $t('usersCMS.contactsModal.tooltips.verifiedF')"
          v-b-tooltip.hover
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
             v-bind:title="$t('usersCMS.deleteModal.title')"
             v-b-tooltip.hover
             hide-footer size="sm" centered
            :header-bg-variant="'danger'"
            :header-text-variant="'light'"
            v-if="can(user_perms, 'delete', 'users')">

      <b-form class="w-100" @submit.prevent="deleteUser(user.id)">

        <b-form-group
        :description="$t('usersCMS.deleteModal.confirmationField.description')">
          <b-input-group>

            <b-form-input
              name="confirmation-passphrase"
              autofocus
              v-model="$v.deletePassphrase.$model"
              v-bind:placeholder="$t('usersCMS.deleteModal.confirmationField.placeholder')"
              :state="$v.deletePassphrase.$dirty ? !$v.deletePassphrase.$error : null"
              @input="$v.deletePassphrase.$touch()">
            </b-form-input>
          </b-input-group>

        </b-form-group>
        <b-button type="submit" block
        variant="danger" v-bind:title="$t('usersCMS.deleteModal.tooltips.deleteButton')"
        v-b-tooltip.hover
        :disabled="!$v.deletePassphrase.$anyDirty || $v.deletePassphrase.$invalid">
          <font-awesome-icon :icon="['fa', 'trash']" fixed-width />
        </b-button>

        <div class="row mx-auto pl-3 pr-3 pt-3 border-top">
          <span class="text-danger notation text-center">
              <font-awesome-icon :icon="['fa', 'exclamation-triangle']"
              size="1x" fixed-width />
              {{$t('usersCMS.deleteModal.description')}}
          </span>
        </div>

      </b-form>
    </b-modal>

    <b-modal id="delete-group-modal"
            @show="deleteGroupPassphrase=''"
            @hidden="deleteGroupPassphrase=''"
            @close="deleteGroupPassphrase=''"
             v-bind:title="$t('usersCMS.deleteGroupModal.title')"
             v-b-tooltip.hover
             hide-footer size="sm" centered
            :header-bg-variant="'danger'"
            :header-text-variant="'light'"
            v-if="can(user_perms, 'delete', 'users')">

      <b-form class="w-100" @submit.prevent="deleteUser(selected)">
        <b-form-group
        :description="$t('usersCMS.deleteGroupModal.confirmationField.description')">
          <b-input-group>

            <b-form-input
              name="confirmation-passphrase"
              autofocus
              v-model="$v.deleteGroupPassphrase.$model"
              v-bind:placeholder="$t('usersCMS.deleteGroupModal.confirmationField.placeholder')"
              :state="$v.deleteGroupPassphrase.$dirty ? !$v.deleteGroupPassphrase.$error : null"
              @input="$v.deleteGroupPassphrase.$touch()">
            </b-form-input>
          </b-input-group>

        </b-form-group>
        <b-button type="submit" block
        variant="danger" v-bind:title="$t('usersCMS.deleteGroupModal.tooltips.deleteButton')"
        v-b-tooltip.hover
        :disabled="!$v.deleteGroupPassphrase.$anyDirty || $v.deleteGroupPassphrase.$invalid">
          <font-awesome-icon :icon="['fa', 'trash']" fixed-width />
        </b-button>

        <div class="row mx-auto pl-3 pr-3 pt-3 border-top">
          <span class="text-danger notation text-center">
              <font-awesome-icon :icon="['fa', 'exclamation-triangle']"
              size="1x" fixed-width />
              {{$t('usersCMS.deleteGroupModal.description')}}
          </span>
        </div>

      </b-form>
    </b-modal>

    <b-modal id="new-modal"
            v-bind:title="$t('usersCMS.formNew.formTitle')"
            hide-footer size="xl" centered
            @show="newUser.password=passwordGenerator(size=8)"
            :header-bg-variant="'success'"
            :header-text-variant="'light'"
            @hidden="onReset"
            v-if="can(user_perms, 'post', 'users')">

      <b-form class="w-100" @submit.prevent="onSubmitNewUser" @reset="onReset">

        <b-form-group>
          <b-form-input name="login"
            type="text"
            autofocus
            v-bind:placeholder="$t('usersCMS.formNew.formFields.login.placeholder')"
            trim
            v-model="$v.newUser.login.$model"
            :state="$v.newUser.login.$dirty ? !$v.newUser.login.$error : null"
          ></b-form-input>

          <b-form-invalid-feedback
          :state="$v.newUser.login.$dirty ? !$v.newUser.login.$error : null">
            <span v-if="!$v.newUser.login.required">
              {{$t('usersCMS.formNew.formFields.login.errors.required')}}
            </span>
            <span v-if="!$v.newUser.login.minLength">
              {{$t('usersCMS.formNew.formFields.login.errors.minLength')}}
            </span>
            <span v-if="!$v.newUser.login.maxLength">
              {{$t('usersCMS.formNew.formFields.login.errors.maxLength')}}
            </span>
            <span v-if="!$v.newUser.login.alphaNum">
              {{$t('usersCMS.formNew.formFields.login.errors.alphaNum')}}
            </span>
          </b-form-invalid-feedback>

        </b-form-group>

        <b-form-group>
          <b-input-group>
            <b-input-group-prepend>
              <b-button variant="outline-secondary"
              v-on:click='isActivePassword = !isActivePassword'>
                <font-awesome-icon fixed-width
                v-bind:icon="isActivePassword ? ['far', 'eye-slash'] : ['far', 'eye']"/>
              </b-button>
            </b-input-group-prepend>
            <b-form-input
              :state="!$v.newUser.password.$dirty ? !$v.newUser.password.$error : null"
              v-bind:type="isActivePassword ? 'text' : 'password'"
              name="password"
              readonly disabled
              v-model="$v.newUser.password.$model"
              v-bind:placeholder="$t('usersCMS.formNew.formFields.password.placeholder')">
            </b-form-input>
            <b-input-group-append>
              <b-button variant="outline-primary"
              v-bind:title="$t('usersCMS.formNew.tooltips.newPassGen')" v-b-tooltip.hover
              @click="newUser.password = passwordGenerator(size=8)">
                <font-awesome-icon :icon="['fa', 'key']" fixed-width />
              </b-button>
            </b-input-group-append>
          </b-input-group>

          <b-form-invalid-feedback
          :state="$v.newUser.password.$dirty ? !$v.newUser.password.$error : null">
            <span v-if="!$v.newUser.password.required">
              {{$t('usersCMS.formNew.formFields.password.errors.required')}}
            </span>
          </b-form-invalid-feedback>
           <b-form-text slot="description">
            <i18n path="usersCMS.formNew.formFields.password.description">
              <font-awesome-icon :icon="['fa', 'key']" fixed-width slot="key"/>
            </i18n>
          </b-form-text>
        </b-form-group>

        <b-form-group>
          <b-input-group>
            <b-form-input v-bind:placeholder="$t('usersCMS.formNew.formFields.surname.placeholder')"
            v-model="$v.newUser.surname.$model"
            :state="$v.newUser.surname.$dirty ? !$v.newUser.surname.$error : null"
            name="surname" trim
            @input="$v.newUser.validationGroupFIO.$touch()">
            </b-form-input>
            <b-form-input v-bind:placeholder="$t('usersCMS.formNew.formFields.name.placeholder')"
            v-model="$v.newUser.name.$model"
            :state="$v.newUser.name.$dirty ? !$v.newUser.name.$error : null"
            name="name" trim
            @input="$v.newUser.validationGroupFIO.$touch()">
            </b-form-input>
            <b-form-input
            v-bind:placeholder="$t('usersCMS.formNew.formFields.patronymic.placeholder')"
            v-model="$v.newUser.patronymic.$model"
            :state="$v.newUser.patronymic.$dirty ? !$v.newUser.patronymic.$error : null"
            name="patronymic" trim
            @input="$v.newUser.validationGroupFIO.$touch()">
            </b-form-input>
          </b-input-group>

          <b-form-invalid-feedback
          :state="$v.newUser.validationGroupFIO.$dirty ?
          !$v.newUser.validationGroupFIO.$anyError : null">
            <span v-if="!$v.newUser.surname.required">
              {{$t('usersCMS.formNew.formFields.surname.errors.required')}}
            </span>
            <span v-if="!$v.newUser.surname.minLength">
              {{$t('usersCMS.formNew.formFields.surname.errors.minLength')}}
            </span>
            <span v-if="!$v.newUser.surname.maxLength">
              {{$t('usersCMS.formNew.formFields.surname.errors.maxLength')}}
            </span>
            <span v-if="!$v.newUser.surname.alphaNum">
              {{$t('usersCMS.formNew.formFields.surname.errors.alpha')}}
            </span>
            <span v-if="!$v.newUser.name.required">
              {{$t('usersCMS.formNew.formFields.name.errors.required')}}
            </span>
            <span v-if="!$v.newUser.name.minLength">
              {{$t('usersCMS.formNew.formFields.name.errors.minLength')}}
            </span>
            <span v-if="!$v.newUser.name.maxLength">
              {{$t('usersCMS.formNew.formFields.name.errors.maxLength')}}
            </span>
            <span v-if="!$v.newUser.name.alphaNum">
              {{$t('usersCMS.formNew.formFields.name.errors.alpha')}}
            </span>
            <span v-if="!$v.newUser.patronymic.required">
              {{$t('usersCMS.formNew.formFields.patronymic.errors.required')}}
            </span>
            <span v-if="!$v.newUser.patronymic.minLength">
              {{$t('usersCMS.formNew.formFields.patronymic.errors.minLength')}}
            </span>
            <span v-if="!$v.newUser.patronymic.maxLength">
              {{$t('usersCMS.formNew.formFields.patronymic.errors.maxLength')}}
            </span>
            <span v-if="!$v.newUser.patronymic.alphaNum">
              {{$t('usersCMS.formNew.formFields.patronymic.errors.alpha')}}
            </span>
          </b-form-invalid-feedback>
        </b-form-group>

        <b-form-group class="text-justify">
          <b-form-group v-for="(v, index) in $v.newUser.email.$each.$iter" v-bind:key="index">
            <b-input-group>

              <b-input-group-text slot="prepend" v-b-tooltip.hover
                :title="$t('usersCMS.formNew.formFields.emails.titlePrimary')"
                v-if="v.$model.type==='primary'">
                  <font-awesome-icon v-bind:icon="['fa', 'envelope']" fixed-width/>
                </b-input-group-text>
                <b-input-group-text slot="prepend" v-b-tooltip.hover
                :title="$t('usersCMS.formNew.formFields.emails.titlePersonal')"
                v-else-if="v.$model.type==='personal'">
                  <font-awesome-icon v-bind:icon="['fa', 'user']" fixed-width/>
                </b-input-group-text>
                <b-input-group-text slot="prepend" v-b-tooltip.hover
                :title="$t('usersCMS.formNew.formFields.emails.titleWork')"
                v-else-if="v.$model.type==='work'">
                  <font-awesome-icon v-bind:icon="['fa', 'briefcase']" fixed-width/>
              </b-input-group-text>

              <b-form-input
                type="email"
                v-bind:placeholder="$t('usersCMS.formNew.formFields.emails.placeholder')"
                name="email"
                v-model="v.value.$model"
                trim
                :state="v.value.$dirty ? !v.value.$error : null"
              ></b-form-input>
            </b-input-group>

            <b-form-invalid-feedback
            :state="v.value.$dirty ? !v.value.$error : null">
              <span v-if="!v.value.required">
                {{$t('usersCMS.formNew.formFields.emails.errors.required')}}
              </span>
              <span v-if="!v.value.email">
                {{$t('usersCMS.formNew.formFields.emails.errors.email')}}
              </span>
            </b-form-invalid-feedback>
          </b-form-group>
          <b-form-text slot="description">
            {{$t('usersCMS.formNew.formFields.emails.description')}}
          </b-form-text>
        </b-form-group>

        <b-form-group>
          <vue-tel-input
          autocomplete="off"
          :onlyCountries="['RU']"
          :disabledFetchingCountry="true"
          v-bind:placeholder="$t('usersCMS.formNew.formFields.phone.placeholder')"
          name="phone"
          v-model="$v.newUser.phone.$model"
          :wrapperClasses="$v.newUser.phone.$dirty ?
          (!$v.newUser.phone.$error ?
          'is-valid input-group' : 'is-invalid input-group') : 'input-group'"
          :inputClasses="$v.newUser.phone.$dirty ?
          (!$v.newUser.phone.$error ?
          'is-valid form-control' : 'is-invalid form-control') : 'form-control'"

          :is-valid="$v.newUser.phone.$dirty ? !$v.newUser.phone.$error : null"
          />

          <b-form-invalid-feedback
          :state="$v.newUser.phone.$dirty ? !$v.newUser.phone.$error : null">
            <span v-if="!$v.newUser.phone.required">
              {{$t('usersCMS.formNew.formFields.phone.errors.required')}}
            </span>
            <span v-if="!$v.newUser.phone.format ">
              {{$t('usersCMS.formNew.formFields.phone.errors.format')}}
            </span>
          </b-form-invalid-feedback>
        </b-form-group>

        <b-form-group>
          <datepicker
          autocomplete="off"
          v-bind:placeholder="$t('usersCMS.formNew.formFields.birthDate.placeholder')"
          :format="dateFormatter" :bootstrap-styling="true"
          :language="russian" :typeable=false :required=true
          :monday-first=true :disabledDates="disabledDates"
          v-model="$v.newUser.birth_date.$model" name="birth_date"
          :input-class="($v.newUser.birth_date.$dirty) ?
          ((!$v.newUser.birth_date.$error) ? 'is-valid' : 'is-invalid') : null">
          </datepicker>

          <b-form-invalid-feedback
          :state="$v.newUser.birth_date.$dirty ? !$v.newUser.birth_date.$error : null">
            <span v-if="!$v.newUser.birth_date.required">
              {{$t('usersCMS.formNew.formFields.birthDate.errors.required')}}
            </span>
          </b-form-invalid-feedback>
        </b-form-group>

        <b-form-group>
          <b-form-textarea
          v-bind:placeholder="$t('usersCMS.formNew.formFields.aboutMe.placeholder')"
          autocomplete="off"
          rows="2" max-rows="6" no-resize
          v-model="$v.newUser.about_me.$model" name="about_me"
          :state="$v.newUser.about_me.$dirty ? !$v.newUser.about_me.$error : null">
          </b-form-textarea>

          <b-form-invalid-feedback
          :state="$v.newUser.about_me.$dirty ? !$v.newUser.about_me.$error : null">
            <span v-if="!$v.newUser.about_me.maxLength">
              {{$t('usersCMS.formNew.formFields.aboutMe.errors.maxLength')}}
            </span>
          </b-form-invalid-feedback>
        </b-form-group>

        <b-form-group>
          <multiselect v-model="$v.newUser.roles.$model"
          v-bind:placeholder="$t('usersCMS.formEdit.formFields.roles.placeholder')"
          label="title" track-by="title" :hideSelected="true"
          :options="roles.results" :multiple="true" :allowEmpty="false"
          :selectLabel="$t('usersCMS.formEdit.formFields.roles.selectLabel')"
          :selectedLabel="$t('usersCMS.formEdit.formFields.roles.selectedLabel')"
          :deselectLabel="$t('usersCMS.formEdit.formFields.roles.deselectLabel')">
            <span slot="noResult">
              {{$t('usersCMS.formEdit.formFields.roles.errors.search')}}
            </span>
          </multiselect>
        </b-form-group>

        <b-row>
          <b-col>
            <b-button type="submit" variant="success" block
            v-bind:title="$t('usersCMS.formNew.tooltips.submitButton')" v-b-tooltip.hover
            :disabled="!$v.newUser.$anyDirty || $v.newUser.$invalid">
              <font-awesome-icon v-if="!formPending"
              :icon="['fa', 'save']" fixed-width />
              <b-spinner small v-if="formPending"></b-spinner>
            </b-button>
          </b-col>
          <b-col>
            <b-button type="reset" variant="danger" block
            v-bind:title="$t('usersCMS.formNew.tooltips.clearButton')" v-b-tooltip.hover
            :disabled="!$v.newUser.$anyDirty">
              <font-awesome-icon v-if="!formPending"
              :icon="['fa', 'times']" fixed-width />
              <b-spinner small v-if="formPending"></b-spinner>
            </b-button>
          </b-col>
        </b-row>

        <div class="row mx-auto mt-3 pl-3 pr-3 pt-3 border-top">
          <span class="text-danger notation text-center">
              <font-awesome-icon :icon="['fa', 'exclamation-triangle']"
              size="1x" fixed-width />
              {{$t('usersCMS.formNew.description')}}
          </span>
        </div>

      </b-form>

    </b-modal>

    <b-modal id="edit-modal"
            @hidden="onResetEdit"
            @close="onResetImage"
            v-bind:title="$t('usersCMS.formEdit.formTitle')"
            hide-footer size="xl" centered
            :header-bg-variant="'primary'"
            :header-text-variant="'light'"
            v-if="can(user_perms, 'put', 'users')">

      <b-form class="w-100" @submit.prevent="onSubmitUpdateUser">
        <b-row>

          <b-col :cols="uid!=user.id? 7 : 12" >

            <b-form-group>
              <b-form-input name="login"
                type="text"
                autofocus
                v-bind:placeholder="$t('usersCMS.formEdit.formFields.login.placeholder')"
                trim
                v-model="$v.user.login.$model"
                :state="$v.user.login.$dirty ? !$v.user.login.$error : null"
              ></b-form-input>

              <b-form-invalid-feedback
              :state="$v.user.login.$dirty ? !$v.user.login.$error : null">
                <span v-if="!$v.user.login.required">
                  {{$t('usersCMS.formEdit.formFields.login.errors.required')}}
                </span>
                <span v-if="!$v.user.login.minLength">
                  {{$t('usersCMS.formEdit.formFields.login.errors.minLength')}}
                </span>
                <span v-if="!$v.user.login.maxLength">
                  {{$t('usersCMS.formEdit.formFields.login.errors.maxLength')}}
                </span>
                <span v-if="!$v.user.login.alphaNum">
                  {{$t('usersCMS.formEdit.formFields.login.errors.alphaNum')}}
                </span>
              </b-form-invalid-feedback>

            </b-form-group>

            <b-form-group>
              <b-input-group>
                <b-form-input
                v-bind:placeholder="$t('usersCMS.formEdit.formFields.surname.placeholder')"
                v-model="$v.user.surname.$model"
                :state="$v.user.surname.$dirty ? !$v.user.surname.$error : null"
                name="surname" trim
                @input="$v.user.validationGroupFIO.$touch()">
                </b-form-input>
                <b-form-input
                v-bind:placeholder="$t('usersCMS.formEdit.formFields.name.placeholder')"
                v-model="$v.user.name.$model"
                :state="$v.user.name.$dirty ? !$v.user.name.$error : null"
                name="name" trim
                @input="$v.user.validationGroupFIO.$touch()">
                </b-form-input>
                <b-form-input
                v-bind:placeholder="$t('usersCMS.formEdit.formFields.patronymic.placeholder')"
                v-model="$v.user.patronymic.$model"
                :state="$v.user.patronymic.$dirty ? !$v.user.patronymic.$error : null"
                name="patronymic" trim
                @input="$v.user.validationGroupFIO.$touch()">
                </b-form-input>
              </b-input-group>

              <b-form-invalid-feedback
              :state="$v.user.validationGroupFIO.$dirty ?
              !$v.user.validationGroupFIO.$anyError : null">
                <span v-if="!$v.user.surname.required">
                  {{$t('usersCMS.formEdit.formFields.surname.errors.required')}}
                </span>
                <span v-if="!$v.user.surname.minLength">
                  {{$t('usersCMS.formEdit.formFields.surname.errors.minLength')}}
                </span>
                <span v-if="!$v.user.surname.maxLength">
                  {{$t('usersCMS.formEdit.formFields.surname.errors.maxLength')}}
                </span>
                <span v-if="!$v.user.surname.alpha">
                  {{$t('usersCMS.formEdit.formFields.surname.errors.alpha')}}
                </span>
                <span v-if="!$v.user.name.required">
                  {{$t('usersCMS.formEdit.formFields.name.errors.required')}}
                </span>
                <span v-if="!$v.user.name.minLength">
                  {{$t('usersCMS.formEdit.formFields.name.errors.minLength')}}
                </span>
                <span v-if="!$v.user.name.maxLength">
                  {{$t('usersCMS.formEdit.formFields.name.errors.maxLength')}}
                </span>
                <span v-if="!$v.user.name.alpha">
                  {{$t('usersCMS.formEdit.formFields.name.errors.alpha')}}
                </span>
                <span v-if="!$v.user.patronymic.required">
                  {{$t('usersCMS.formEdit.formFields.patronymic.errors.required')}}
                </span>
                <span v-if="!$v.user.patronymic.minLength">
                  {{$t('usersCMS.formEdit.formFields.patronymic.errors.minLength')}}
                </span>
                <span v-if="!$v.user.patronymic.maxLength">
                  {{$t('usersCMS.formEdit.formFields.patronymic.errors.maxLength')}}
                </span>
                <span v-if="!$v.user.patronymic.alpha">
                  {{$t('usersCMS.formEdit.formFields.patronymic.errors.alpha')}}
                </span>
              </b-form-invalid-feedback>
            </b-form-group>

            <b-form-group class="text-justify">
              <b-form-group v-for="(v, index) in $v.user.email.$each.$iter" v-bind:key="index">
                <b-input-group>

                  <b-input-group-text slot="prepend" v-b-tooltip.hover
                    :title="$t('usersCMS.formEdit.formFields.emails.titlePrimary')"
                    v-if="v.$model.type==='primary'">
                      <font-awesome-icon v-bind:icon="['fa', 'envelope']" fixed-width/>
                    </b-input-group-text>
                    <b-input-group-text slot="prepend" v-b-tooltip.hover
                    :title="$t('usersCMS.formEdit.formFields.emails.titlePersonal')"
                    v-else-if="v.$model.type==='personal'">
                      <font-awesome-icon v-bind:icon="['fa', 'user']" fixed-width/>
                    </b-input-group-text>
                    <b-input-group-text slot="prepend" v-b-tooltip.hover
                    :title="$t('usersCMS.formEdit.formFields.emails.titleWork')"
                    v-else-if="v.$model.type==='work'">
                      <font-awesome-icon v-bind:icon="['fa', 'briefcase']" fixed-width/>
                  </b-input-group-text>

                  <b-form-input
                    type="email"
                    v-bind:placeholder="$t('usersCMS.formEdit.formFields.emails.placeholder')"
                    name="email"
                    v-model="v.value.$model"
                    trim
                    :state="v.value.$dirty ? !v.value.$error : null"
                  ></b-form-input>
                  <b-input-group-append>
                    <b-button v-if="v.$model.value && !v.value.$dirty &&
                    (dateDiffNow(v.$model.activeUntil, reactivationPeriod) || !v.$model.verified)"
                    variant="outline-secondary" v-b-tooltip.hover
                    v-bind:title="$t('usersCMS.formEdit.formFields.emails.sendVerification')"
                    @click="onSubmitMailVerify(user.id, v.$model.type, v.$model.value)"
                    :disabled="formPending">
                      <b-spinner small v-if="formPending"></b-spinner>
                      <font-awesome-icon v-else v-bind:icon="['fa', 'envelope']" fixed-width/>
                    </b-button>
                    <b-button
                    v-if="v.$model.value && (!v.value.$dirty &&
                      v.$model.verified && v.$model.type!=='primary')"
                    variant="outline-danger" v-b-tooltip.hover
                    v-bind:title="$t('usersCMS.formEdit.formFields.emails.resetActivation')"
                    @click="onSubmitMailReset(user.id, v.$model.type, v.$model.value)"
                    :disabled="formPending">
                      <b-spinner small v-if="formPending"></b-spinner>
                      <font-awesome-icon v-else v-bind:icon="['fa', 'ban']" fixed-width/>
                    </b-button>
                    <b-input-group-text v-if="v.$model.value" v-b-tooltip.hover
                      :title="v.$model.verified ?
                      $t('usersCMS.formEdit.formFields.emails.confirmationT') :
                      $t('usersCMS.formEdit.formFields.emails.confirmationF')" >
                        <font-awesome-icon
                        v-bind:icon="['fa', 'check-circle']"
                        :class="v.$model.verified ? 'text-success' : 'text-danger'" fixed-width/>
                      </b-input-group-text>

                      <b-input-group-text v-if="v.$model.value" v-b-tooltip.hover
                       :title="v.$model.activeUntil ?
                        $t('usersCMS.formEdit.formFields.emails.activity')+
                        $options.filters.moment(v.$model.activeUntil,
                                                'YYYY-MM-DD, HH:mm:ss') :
                        'Необходима активация'">
                        <font-awesome-icon
                        v-if="v.$model.activeUntil || v.$model.verified"
                        v-bind:icon="['fa', 'clock']" fixed-width class="text-primary"/>
                      </b-input-group-text>
                  </b-input-group-append>
                </b-input-group>

                <b-form-invalid-feedback
                :state="v.value.$dirty ? !v.value.$error : null">
                  <span v-if="!v.value.required">
                    {{$t('usersCMS.formEdit.formFields.emails.errors.required')}}
                  </span>
                  <span v-if="!v.value.email">
                    {{$t('usersCMS.formEdit.formFields.emails.errors.email')}}
                  </span>
                </b-form-invalid-feedback>
              </b-form-group>
              <b-form-text slot="description">
                {{$t('usersCMS.formEdit.formFields.emails.description')}}
              </b-form-text>
            </b-form-group>

            <b-form-group>
              <vue-tel-input
              autocomplete="off"
              :onlyCountries="['RU']"
              :disabledFetchingCountry="true"
              v-bind:placeholder="$t('usersCMS.formEdit.formFields.phone.placeholder')"
              name="phone"
              v-model="$v.user.phone.$model"
              :wrapperClasses="$v.user.phone.$dirty ?
              (!$v.user.phone.$error ?
              'is-valid input-group' : 'is-invalid input-group') : 'input-group'"
              :inputClasses="$v.user.phone.$dirty ?
              (!$v.user.phone.$error ?
              'is-valid form-control' : 'is-invalid form-control') : 'form-control'"

              :is-valid="$v.user.phone.$dirty ? !$v.user.phone.$error : null"
              />

              <b-form-invalid-feedback
              :state="$v.user.phone.$dirty ? !$v.user.phone.$error : null">
                <span v-if="!$v.user.phone.required">
                  {{$t('usersCMS.formEdit.formFields.phone.errors.required')}}
                </span>
                <span v-if="!$v.user.phone.format ">
                  {{$t('usersCMS.formEdit.formFields.phone.errors.format')}}
                </span>
              </b-form-invalid-feedback>
            </b-form-group>

            <b-form-group>
              <datepicker
              autocomplete="off"
              v-bind:placeholder="$t('usersCMS.formEdit.formFields.birthDate.placeholder')"
              :format="dateFormatter" :bootstrap-styling="true"
              :language="russian" :typeable=false :required=true
              :monday-first=true :disabledDates="disabledDates"
              v-model="$v.user.birth_date.$model" name="birth_date"
              :input-class="($v.user.birth_date.$dirty) ?
              ((!$v.user.birth_date.$error) ? 'is-valid' : 'is-invalid') : null">
              </datepicker>

              <b-form-invalid-feedback
              :state="$v.user.birth_date.$dirty ? !$v.user.birth_date.$error : null">
                <span v-if="!$v.user.birth_date.required">
                  {{$t('usersCMS.formEdit.formFields.birthDate.errors.required')}}
                </span>
              </b-form-invalid-feedback>
            </b-form-group>

            <b-form-group>
              <b-form-textarea
              v-bind:placeholder="$t('usersCMS.formEdit.formFields.aboutMe.placeholder')"
              autocomplete="off"
              rows="2" max-rows="6" no-resize
              v-model="$v.user.about_me.$model" name="about_me"
              :state="$v.user.about_me.$dirty ? !$v.user.about_me.$error : null">
              </b-form-textarea>

              <b-form-invalid-feedback
              :state="$v.user.about_me.$dirty ? !$v.user.about_me.$error : null">
                <span v-if="!$v.user.about_me.maxLength">
                  {{$t('usersCMS.formEdit.formFields.aboutMe.errors.maxLength')}}
                </span>
              </b-form-invalid-feedback>
            </b-form-group>

            <b-form-group>
              <multiselect v-model="$v.user.roles.$model"
              v-bind:placeholder="$t('usersCMS.formEdit.formFields.roles.placeholder')"
              label="title" track-by="title" :hideSelected="true"
              :options="roles.results" :multiple="true" :allowEmpty="false"
              :selectLabel="$t('usersCMS.formEdit.formFields.roles.selectLabel')"
              :selectedLabel="$t('usersCMS.formEdit.formFields.roles.selectedLabel')"
              :deselectLabel="$t('usersCMS.formEdit.formFields.roles.deselectLabel')">
                <span slot="noResult">
                  {{$t('usersCMS.formEdit.formFields.roles.errors.search')}}
                </span>
                <template slot="tag" slot-scope="props">
                  <div class="multiselect__tag" v-if="!props.option.reassignable">
                    <span>{{ props.option.title }}</span>
                  </div>
                </template>
              </multiselect>
            </b-form-group>

          </b-col>

          <b-col cols="5" v-if="uid!=user.id">
            <h4 class="text-danger">
              {{$t('usersCMS.formEdit.dangerZone.title')}}
            </h4>
            <b-card no-body
            border-variant="danger">
              <b-list-group flush>
                <b-list-group-item class="flex-column align-items-start align-middle">
                  <div class="d-flex w-100 pb-2 justify-content-between align-items-center">
                    <h6 class="m-0">
                      {{$t('usersCMS.formEdit.dangerZone.functions.resetPassword.title')}}
                    </h6>
                    <b-button @click="onSubmitPasswordReset(user.id)"
                    size="sm" variant="outline-danger">
                      {{$t('usersCMS.formEdit.dangerZone.functions.resetPassword.button')}}
                    </b-button>
                  </div>
                  <small class="text-muted">
                    {{$t('usersCMS.formEdit.dangerZone.functions.resetPassword.description')}}
                    </small>
                </b-list-group-item>
                <b-list-group-item class="flex-column align-items-start align-middle">
                  <div class="d-flex w-100 pb-2 justify-content-between align-items-center">
                    <h6 class="m-0">
                      {{$t('usersCMS.formEdit.dangerZone.functions.blockPassword.title')}}
                    </h6>
                    <b-button @click="onSubmitPasswordBlock(user.id)"
                    size="sm" variant="outline-danger">
                      {{$t('usersCMS.formEdit.dangerZone.functions.blockPassword.button')}}
                    </b-button>
                  </div>
                  <small class="text-muted">
                    {{$t('usersCMS.formEdit.dangerZone.functions.blockPassword.description')}}
                  </small>
                </b-list-group-item>
              </b-list-group>
            </b-card>
          </b-col>

        </b-row>

        <b-row>
          <b-col>
            <b-button type="submit" variant="primary" block
            v-bind:title="$t('usersCMS.formEdit.tooltips.submitButton')" v-b-tooltip.hover
            :disabled="!$v.user.$anyDirty || $v.user.$invalid || formPending">
              <font-awesome-icon v-if="!formPending"
              :icon="['fa', 'save']" fixed-width />
              <b-spinner small v-if="formPending"></b-spinner>
            </b-button>
          </b-col>
        </b-row>

        <div class="row mx-auto mt-3 pl-3 pr-3 pt-3 border-top">
<!--
          <span class="text-danger notation text-center">
              <font-awesome-icon :icon="['fa', 'exclamation-triangle']"
              size="1x" fixed-width />
  <b>При сбросе основной почты</b> и выходе из CMS, пользователь больше не сможет войти!
  Будьте осторожны!
          </span>
-->
        </div>

      </b-form>

    </b-modal>

    <b-modal id="avatar-modal"
            @hidden="onResetImage"
            @close="onResetImage"
            v-bind:title="$t('usersCMS.formAvatar.formTitle')"
            hide-footer size="md" centered
            :header-bg-variant="'primary'"
            :header-text-variant="'light'"
            v-if="can(user_perms, 'put', 'users')">

      <div class=" row w-100 mx-auto pb-3 justify-content-center align-items-center">
        <img v-bind:src="imageUpdate.imageData ?
        imageUpdate.imageData : '/static/profile_avatars/default.png'"
        class="profile-image-preview preview-md preview-square mr-4">

        <img v-bind:src="imageUpdate.imageData ?
        imageUpdate.imageData : '/static/profile_avatars/default.png'"
        class="profile-image-preview preview-md mr-4">

        <img v-bind:src="imageUpdate.imageData ?
        imageUpdate.imageData : '/static/profile_avatars/default.png'"
        class="profile-image-preview preview-sm mr-4">

      </div>

      <b-form class="w-100" @submit.prevent="onSubmitAvatar(user.id)">
        <b-form-group
        :description="$t('usersCMS.formAvatar.formDescription')">

          <b-form-file
            ref="imageInput"
            @input="onSelectImage"
            lang="ru"
            v-bind:placeholder="$t('userProfile.formAvatar.formFields.file.placeholder')"
            v-bind:browse-text="$t('userProfile.formAvatar.formFields.file.browseButton')"
            accept="image/jpeg, image/png, image/gif"
            :state="$v.imageUpdate.$dirty ? !$v.imageUpdate.$anyError : null"
          ></b-form-file>
          <b-form-invalid-feedback
          :state="$v.imageUpdate.$dirty ? !$v.imageUpdate.$anyError : null">
            <span v-if="!$v.imageUpdate.size.maxValue">
              {{$t('usersCMS.formAvatar.formFields.file.errors.maxValue')}}
            </span>
            <span v-if="!$v.imageUpdate.type.isImage">
              {{$t('usersCMS.formAvatar.formFields.file.errors.isImage')}}
            </span>
          </b-form-invalid-feedback>

        </b-form-group>

        <b-button class="mb-3" type="submit" block variant="primary"
        v-bind:title="$t('usersCMS.formAvatar.saveButton')" v-b-tooltip.hover
        :disabled="!$v.imageUpdate.$anyDirty || $v.imageUpdate.$invalid || this.file == null">
          <font-awesome-icon :icon="['fa', 'save']" fixed-width />
        </b-button>

        <div class="row mx-auto pt-3 border-top">
          <b-progress v-if="isActiveProgress" :max="100" show-progress animated class="w-100">
            <b-progress-bar :value="progressValue" variant="success"
            :label="`${((progressValue / progressMax) * 100).toFixed(2)}%`">
            </b-progress-bar>
            <b-progress-bar :value="preloadValue" variant="primary"
            :label="`${preloadValue.toFixed(2)}%`">
            </b-progress-bar>
          </b-progress>
        </div>
      </b-form>
    </b-modal>

  </main>
</template>

<script>
import Datepicker from 'vuejs-datepicker';
import { ru } from 'vuejs-datepicker/dist/locale';
import VueTelInput from 'vue-tel-input';
import moment from 'moment';
import { mapState } from 'vuex';
import _ from 'lodash';
import {
  required, sameAs, minLength, maxLength, alphaNum, email, requiredIf,
  maxValue,
} from 'vuelidate/lib/validators';
import Multiselect from 'vue-multiselect';
import Breadcumbs from './Breadcumbs';
import {
  EventBus, passwordGenerator, dateDiffNow, formatBytes, can,
} from '@/utils';
import { imageType } from '@/validators';


export default {
  name: 'Users',
  data() {
    return {
      dateDiffNow,
      user: {},
      deletePassphrase: '',
      deleteGroupPassphrase: '',
      selected: [],
      selectAll: false,
      preloadValue: 0,
      isActiveProgress: false,
      listControl: {
        page: 1,
        start: 1,
        limit: 20,
        orderBy: {
          field: 'id',
          asc: true,
        },
      },
      disabledDates: {
        from: new Date(),
      },
      russian: ru,
      passwordGenerator,
      can,
      isActivePassword: false,
      newUser: {
        login: '',
        password: '',
        name: '',
        surname: '',
        patronymic: '',
        email: [
          {
            type: 'primary',
            value: '',
          },
          {
            type: 'work',
            value: '',
          },
          {
            type: 'personal',
            value: '',
          },
        ],
        phone: '',
        birth_date: '',
        about_me: '',
        roles: '',
      },
      file: null,
      imageUpdate: {
        type: '',
        size: 0,
        imageData: '',
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
      sameAsPassphrase: sameAs(function samePassphrase() {
        return this.$t('usersCMS.deleteGroupModal.confirmationField.passphrase');
      }),
    },
    newUser: {
      login: {
        required,
        minLength: minLength(4),
        maxLength: maxLength(20),
        alphaNum,
      },
      password: {
        required,
      },
      name: {
        required,
        minLength: minLength(4),
        maxLength: maxLength(20),
        alpha: val => /^[а-яё]*$/i.test(val),
      },
      surname: {
        required,
        minLength: minLength(4),
        maxLength: maxLength(20),
        alpha: val => /^[а-яё]*$/i.test(val),
      },
      patronymic: {
        required,
        minLength: minLength(4),
        maxLength: maxLength(20),
        alpha: val => /^[а-яё]*$/i.test(val),
      },
      email: {
        $each: {
          value: {
            email,
            required: requiredIf((value) => {
              if (!value) return true;
              if (value.type === 'primary') {
                return true;
              }
              return false;
            }),
          },
        },
      },
      phone: {
        required,
        format: val => (val != null && val.length === 16),
      },
      birth_date: {
        required,
      },
      about_me: {
        maxLength: maxLength(140),
      },
      roles: {
        required,
      },
      validationGroupFIO: ['newUser.name', 'newUser.surname', 'newUser.patronymic'],
    },
    user: {
      login: {
        required,
        minLength: minLength(4),
        maxLength: maxLength(20),
        alphaNum,
      },
      name: {
        required,
        minLength: minLength(4),
        maxLength: maxLength(20),
        alpha: val => /^[а-яё]*$/i.test(val),
      },
      surname: {
        required,
        minLength: minLength(4),
        maxLength: maxLength(20),
        alpha: val => /^[а-яё]*$/i.test(val),
      },
      patronymic: {
        required,
        minLength: minLength(4),
        maxLength: maxLength(20),
        alpha: val => /^[а-яё]*$/i.test(val),
      },
      email: {
        $each: {
          value: {
            email,
            required: requiredIf((value) => {
              if (!value) return true;
              if (value.type === 'primary') {
                return true;
              }
              return false;
            }),
          },
        },
      },
      phone: {
        required,
        format: val => (val != null && val.length === 16),
      },
      birth_date: {
        required,
      },
      roles: {
        required,
      },
      about_me: {
        maxLength: maxLength(140),
      },
      validationGroupFIO: ['user.name', 'user.surname', 'user.patronymic'],
    },
    imageUpdate: {
      size: {
        maxValue: maxValue(3),
      },
      type: {
        isImage: imageType,
      },
    },
  },
  components: {
    Breadcumbs, Datepicker, VueTelInput, Multiselect,
  },
  computed: mapState({
    users: state => state.users,
    user_perms: state => state.user_perms,
    roles: state => state.roles,
    uid: state => state.uid,
    reactivationPeriod: state => state.reactivationPeriod,
    orderedList() {
      return _.orderBy(this.users.results,
        this.listControl.orderBy.field,
        this.listControl.orderBy.asc ? 'asc' : 'desc');
    },
    progressValue: state => state.uploadProgress,
    progressMax: state => state.uploadProgressMax,
    formPending: state => state.formPending,
  }),
  watch: {
    user_perms() {
      if (can(this.user_perms, 'get', 'users')) {
        this.$store.dispatch('loadUsers', { start: this.listControl.start, limit: this.listControl.limit });
        this.$store.dispatch('loadRoles', {});
      }
    },
  },
  methods: {
    dateFormatter(date) {
      return moment(date).format('YYYY-MM-DD');
    },
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
    onSelectImage() {
      const { files } = this.$refs.imageInput.$refs.input;
      if (files && files[0]) {
        this.imageUpdate.type = files[0].type;
        this.imageUpdate.size = formatBytes(files[0].size, 2, 2).number;
        this.$v.imageUpdate.$touch();

        if (!this.$v.imageUpdate.$invalid) {
          const reader = new FileReader();
          reader.onprogress = (e) => {
            if (e.lengthComputable) {
              this.isActiveProgress = true;
              this.preloadValue = Math.round((e.loaded / e.total) * 100);
            }
          };
          reader.onload = (e) => {
            this.imageUpdate.imageData = e.target.result;
            this.file = files;
          };
          reader.readAsDataURL(files[0]);
          this.$emit('input', files[0]);
        }
      }
    },
    onResetImage(evt) {
      evt.preventDefault();
      this.user = {};
      this.file = null;
      this.imageUpdate.type = '';
      this.imageUpdate.size = 0;
      this.imageUpdate.imageData = '';
      this.isActiveProgress = false;
      // Trick to reset/clear native browser form validation state
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
      EventBus.$emit('forceRerender');
    },
    onSubmitAvatar(id) {
      this.$v.imageUpdate.$touch();

      if (!this.$v.imageUpdate.$invalid) {
        const formData = new FormData();
        if (this.file) {
          formData.append('avatar', this.file[0]);
        }
        this.isActiveProgress = true;
        this.$store.dispatch('updateUserAvatar', { formData, id });
      }
    },
    deleteAvatar(id) {
      this.$store.dispatch('deleteUserAvatar', { id });
    },
    onReset(evt) {
      evt.preventDefault();
      this.$v.newUser.$reset();

      this.newUser.login = '';
      this.newUser.password = passwordGenerator(8);
      this.newUser.name = '';
      this.newUser.surname = '';
      this.newUser.patronymic = '';
      this.newUser.phone = '';
      this.newUser.birth_date = '';
      this.newUser.about_me = '';
      this.newUser.email = [
        {
          type: 'primary',
          value: '',
        },
        {
          type: 'work',
          value: '',
        },
        {
          type: 'personal',
          value: '',
        },
      ];
      // Trick to reset/clear native browser form validation state
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
      EventBus.$emit('forceRerender');
    },
    onResetEdit(evt) {
      evt.preventDefault();
      this.$v.user.$reset();
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
      EventBus.$emit('forceRerender');
    },
    onSubmitPasswordReset(id) {
      this.$store.dispatch('passwordReset', { id });
    },
    onSubmitPasswordBlock(id) {
      this.$store.dispatch('passwordBlock', { id });
    },
    onSubmitMailVerify(id, type, value) {
      this.$store.dispatch('verifyMailSend', { id, value, type });
      EventBus.$emit('forceRerender');
    },
    onSubmitMailReset(id, type, value) {
      this.$store.dispatch('verifyMailReset', { id, value, type });
      EventBus.$emit('forceRerender');
    },
    onSubmitNewUser() {
      this.$v.$touch();

      if (!this.$v.newUser.$invalid) {
        this.newUser.birth_date = moment(this.newUser.birth_date).format('YYYY-MM-DD');
        this.$store.dispatch('newUser', this.newUser);
      }
    },
    async onSubmitUpdateUser() {
      this.$v.user.$touch();

      if (!this.$v.user.$invalid) {
        this.user.birth_date = moment(this.user.birth_date).format('YYYY-MM-DD');
        await this.$store.dispatch('updateUser', this.user);
        this.$v.user.$reset();
        EventBus.$emit('forceRerender');
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
