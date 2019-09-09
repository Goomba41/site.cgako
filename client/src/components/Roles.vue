<template>
  <main class="container-fluid">
    <breadcumbs></breadcumbs>

    <b-row class="pb-4 m-0 w-100">
      <b-col align-self="start" class="text-center" sm="8">
        <b-row class="justify-content-start align-middle align-items-center">
          <span class="text-info pr-3">
            {{ $tc('rolesPermissions.counter', roles.count) }}
          </span>
          <b-button v-bind:title="$t('rolesPermissions.tooltips.newRoleButton')"
          v-b-tooltip.hover class="mr-1" size="sm" variant="success"
          v-b-modal.new-modal>
            <font-awesome-icon icon="plus" fixed-width />
          </b-button>
          <b-dropdown size="sm" class="mr-1"
          v-bind:disabled="!selected.length"
          v-bind:class="!selected.length">
            <template slot="button-content">
              <font-awesome-icon icon="list" fixed-width />
            </template>
            <b-dropdown-item variant="danger" v-b-modal.delete-group-modal>
              <font-awesome-icon icon="trash" fixed-width />
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
        </b-row>
      </b-col>

    </b-row>
<!--
{{roles.results}}<br><br>
{{role}}<br><br>
-->
    <b-row class="p-3">
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
              <td class="text-left">
                <b-button size="sm"
                v-bind:title="$t('rolesPermissions.tooltips.editRoleButton')"
                v-b-tooltip.hover variant="primary"
                v-b-modal.edit-modal @click="selectRole(role.id)">
                  <font-awesome-icon :icon="['fa', 'pencil-alt']" fixed-width />
                </b-button>

                <b-button
                size="sm" variant="info"
                v-bind:title="$t('rolesPermissions.tooltips.permissionsRoleButton')"
                v-b-tooltip.hover
                v-if="role.permissions.length"
                @click="selectRole(role.id)">
                  <font-awesome-icon :icon="['fa', 'user-check']" fixed-width />
                </b-button>

                <b-button
                size="sm" variant="danger"
                v-bind:title="$t('rolesPermissions.tooltips.deleteRoleButton')"
                v-b-tooltip.hover
                v-if="role.deletable"
                @click="selectRole(role.id)"
                v-b-modal.delete-modal>
                  <font-awesome-icon :icon="['fa', 'trash']" fixed-width />
                </b-button>

              </td>
            </tr>
          </tbody>
        </table>

      </b-col>
      <b-col sm="6">
        <b-card no-body header-tag="header">
          <h3 slot="header" class="mb-0 small">
            {{ $t('rolesPermissions.titles.rolePermissionsTitle') }}
          </h3>
          <b-list-group flush v-if="Object.keys(role).length===0">
            <b-list-group-item class="flex-column align-items-start">
               <b-form-text slot="description">
                <i18n path="rolesPermissions.titles.rolePermissionsDesc">
                  <font-awesome-icon :icon="['fa', 'user-check']" fixed-width slot="icon"/>
                </i18n>
              </b-form-text>
            </b-list-group-item>
          </b-list-group>

          <b-list-group flush v-else>
            <b-list-group-item class="flex-column align-items-start"
            v-for="permission in role.permissions" :key="permission.id">
                <span title="Объект" v-b-tooltip.hover><b>{{permission.objects.title}}</b></span>
                <span title="Разрешение" v-b-tooltip.hover>{{permission.actions.title}}</span>
            </b-list-group-item>

          </b-list-group>
        </b-card>
      </b-col>
    </b-row>

    <b-modal id="delete-modal"
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
            v-bind:title="$t('rolesPermissions.formNew.formTitle')"
            hide-footer size="sm" centered
            :header-bg-variant="'success'"
            :header-text-variant="'light'"
            @hidden="onReset">

      <b-form class="w-100" @submit.prevent="" @reset="onReset">

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
<!--
    <b-modal id="edit-modal"
            @hidden="user={}"
            @close="user={}"
            title="Исправить досье"
            hide-footer size="xl" centered
            :header-bg-variant="'primary'"
            :header-text-variant="'light'">

      <b-form class="w-100" @submit.prevent="onSubmitUpdateUser">
        <b-row>

          <b-col :cols="uid!=user.id? 7 : 12" >

            <b-form-group>
              <b-form-input name="login"
                type="text"
                autofocus
                placeholder="Логин"
                trim
                v-model="$v.user.login.$model"
                :state="$v.user.login.$dirty ? !$v.user.login.$error : null"
              ></b-form-input>

              <b-form-invalid-feedback
              :state="$v.user.login.$dirty ? !$v.user.login.$error : null">
                <span v-if="!$v.user.login.required">
                  Поле обязательно для заполнения!
                </span>
                <span v-if="!$v.user.login.minLength">
                  Поле должно содержать минимум 4 символа!
                </span>
                <span v-if="!$v.user.login.maxLength">
                  Поле может содержать максимум 20 символов!
                </span>
                <span v-if="!$v.user.login.alphaNum">
                  Поле может содержать только латинские буквы и цифры!
                </span>
              </b-form-invalid-feedback>

            </b-form-group>

            <b-form-group>
              <b-input-group>
                <b-form-input placeholder="Фамилия"
                v-model="$v.user.surname.$model"
                :state="$v.user.surname.$dirty ? !$v.user.surname.$error : null"
                name="surname" trim
                @input="$v.user.validationGroupFIO.$touch()">
                </b-form-input>
                <b-form-input placeholder="Имя"
                v-model="$v.user.name.$model"
                :state="$v.user.name.$dirty ? !$v.user.name.$error : null"
                name="name" trim
                @input="$v.user.validationGroupFIO.$touch()">
                </b-form-input>
                <b-form-input placeholder="Отчество"
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
                  Фамилия обязательна для заполнения!
                </span>
                <span v-if="!$v.user.surname.minLength">
                  Фамилия должна содержать минимум 4 символа!
                </span>
                <span v-if="!$v.user.surname.maxLength">
                  Фамилия может содержать максимум 20 символов!
                </span>
                <span v-if="!$v.user.surname.alpha">
                  Фамилия может содержать только русские буквы!
                </span>
                <span v-if="!$v.user.name.required">
                  Имя обязательно для заполнения!
                </span>
                <span v-if="!$v.user.name.minLength">
                  Имя должно содержать минимум 4 символа!
                </span>
                <span v-if="!$v.user.name.maxLength">
                  Имя может содержать максимум 20 символов!
                </span>
                <span v-if="!$v.user.name.alpha">
                  Имя может содержать только русские буквы!
                </span>
                <span v-if="!$v.user.patronymic.required">
                  Отчество обязательно для заполнения!
                </span>
                <span v-if="!$v.user.patronymic.minLength">
                  Отчество должно содержать минимум 4 символа!
                </span>
                <span v-if="!$v.user.patronymic.maxLength">
                  Отчество может содержать максимум 20 символов!
                </span>
                <span v-if="!$v.user.patronymic.alpha">
                  Отчество может содержать русские только буквы!
                </span>
              </b-form-invalid-feedback>
            </b-form-group>

            <b-form-group class="text-justify">
              <b-form-group v-for="(v, index) in $v.user.email.$each.$iter" v-bind:key="index">
                <b-input-group>
                  <b-input-group-text slot="prepend">
                    <font-awesome-icon v-b-tooltip.hover title="Личная почта"
                    v-if="v.$model.type==='personal'"
                    v-bind:icon="['fa', 'user']" fixed-width/>
                    <font-awesome-icon v-b-tooltip.hover title="Основная почта"
                    v-else-if="v.$model.type==='primary'"
                    v-bind:icon="['fa', 'envelope']" fixed-width/>
                    <font-awesome-icon v-b-tooltip.hover title="Рабочая почта"
                    v-else-if="v.$model.type==='work'"
                    v-bind:icon="['fa', 'briefcase']" fixed-width/>
                  </b-input-group-text>
                  <b-form-input
                    type="email"
                    placeholder="Email"
                    name="email"
                    v-model="v.value.$model"
                    trim
                    :state="v.value.$dirty ? !v.value.$error : null"
                  ></b-form-input>
                  <b-input-group-append>
                    <b-button v-if="v.$model.value && !v.value.$dirty &&
                    (dateDiffNow(v.$model.activeUntil, reactivationPeriod) || !v.$model.verified)"
                    variant="outline-secondary" v-b-tooltip.hover
                    title="Послать письмо подтверждения"
                    @click="onSubmitMailVerify(user.id, v.$model.type, v.$model.value)"
                    :disabled="formPending">
                      <b-spinner small v-if="formPending"
                      label="Идет отправка..."></b-spinner>
                      <font-awesome-icon v-else v-bind:icon="['fa', 'envelope']" fixed-width/>
                    </b-button>
                    <b-button v-if="v.$model.value && (!v.value.$dirty && v.$model.verified)"
                    variant="outline-danger" v-b-tooltip.hover
                    title="Сбросить активацию почты"
                    @click="onSubmitMailReset(user.id, v.$model.type, v.$model.value)"
                    :disabled="formPending">
                      <b-spinner small v-if="formPending"
                      label="Обработка..."></b-spinner>
                      <font-awesome-icon v-else v-bind:icon="['fa', 'ban']" fixed-width/>
                    </b-button>
                    <b-input-group-text v-if="v.$model.value">

                      <font-awesome-icon
                      :title="v.$model.verified ? 'Подтверждена' : 'Не подтверждена'"
                      v-bind:icon="['fa', 'check-circle']"
                      :class="v.$model.verified ? 'text-success' : 'text-danger'" fixed-width/>

                      <font-awesome-icon :title="v.$model.activeUntil ?
                      'Активен до: '+
                      $options.filters.moment(v.$model.activeUntil,
                                              'dddd, MMMM Do YYYY, HH:mm:ss') :
                      'Необходима активация'"
                      v-if="v.$model.activeUntil || v.$model.verified"
                      v-bind:icon="['fa', 'clock']" fixed-width class="text-primary"/>

                    </b-input-group-text>
                  </b-input-group-append>
                </b-input-group>

                <b-form-invalid-feedback
                :state="v.value.$dirty ? !v.value.$error : null">
                  <span v-if="!v.value.required">
                    Поле обязательно для заполнения!
                  </span>
                  <span v-if="!v.value.email">
                    Поле может содержать только email-адрес (example@example.ru)!
                  </span>
                </b-form-invalid-feedback>
              </b-form-group>
              <b-form-text slot="description">
                Основная почта
                <font-awesome-icon :icon="['fa', 'envelope']" fixed-width />
                обязательна для заполнения.
                На добавленную или измененную почту будет отправлено письмо с ссылкой подтверждения.
              </b-form-text>
            </b-form-group>

            <b-form-group>
              <vue-tel-input
              autocomplete="off"
              :onlyCountries="['RU']"
              :disabledFetchingCountry="true"
              :placeholder="'Номер телефона'"
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
                  Поле обязательно для заполнения!
                </span>
                <span v-if="!$v.user.phone.format ">
                  Неправильное количество цифр в номере!
                </span>
              </b-form-invalid-feedback>
            </b-form-group>

            <b-form-group>
              <datepicker
              autocomplete="off"
              :placeholder="'Дата рождения (ГГГГ-MM-ДД)'"
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
                  Поле обязательно для заполнения!
                </span>
              </b-form-invalid-feedback>
            </b-form-group>

            <b-form-group>
          <b-form-textarea placeholder="О себе"
          autocomplete="off"
          rows="2" max-rows="6" no-resize
          v-model="$v.user.about_me.$model" name="about_me"
          :state="$v.user.about_me.$dirty ? !$v.user.about_me.$error : null">
          </b-form-textarea>

          <b-form-invalid-feedback
          :state="$v.user.about_me.$dirty ? !$v.user.about_me.$error : null">
            <span v-if="!$v.user.about_me.maxLength">
              Поле может содержать максимум 140 символов!
            </span>
          </b-form-invalid-feedback>
        </b-form-group>
          </b-col>

          <b-col cols="5" v-if="uid!=user.id">
            <h4 class="text-danger">Опасная зона</h4>
            <b-card no-body
            border-variant="danger">
              <b-list-group flush>
                <b-list-group-item class="flex-column align-items-start align-middle">
                  <div class="d-flex w-100 pb-2 justify-content-between align-items-center">
                    <h6 class="m-0">Сбросить пароль</h6>
                    <b-button @click="onSubmitPasswordReset(user.id)"
                    size="sm" title="Сбросить пароль" variant="outline-danger"
                    v-b-tooltip.hover>Сделать сброс</b-button>
                  </div>
                  <small class="text-muted">Эта функция сгенерирует одноразовый
                  пароль и пошлет его на основную почту пользователя</small>
                </b-list-group-item>
                <b-list-group-item class="flex-column align-items-start align-middle">
                  <div class="d-flex w-100 pb-2 justify-content-between align-items-center">
                    <h6 class="m-0">Блокировать пароль</h6>
                    <b-button @click="onSubmitPasswordBlock(user.id)"
                    size="sm" title="Блокировать пароль" variant="outline-danger"
                    v-b-tooltip.hover>Заблокировать</b-button>
                  </div>
                  <small class="text-muted">Эта функция заблокирует пароль
                  пользователя и он не сможет войти в систему</small>
                </b-list-group-item>
              </b-list-group>
            </b-card>
          </b-col>

        </b-row>

        <b-row>
          <b-col>
            <b-button type="submit" variant="primary" block
            title="Внести новое досье" v-b-tooltip.hover
            :disabled="!$v.user.$anyDirty || $v.user.$invalid || formPending">
              <font-awesome-icon v-if="!formPending"
              :icon="['fa', 'save']" fixed-width />
              <b-spinner small v-if="formPending"
              label="Идет отправка досье..."></b-spinner>
            </b-button>
          </b-col>
        </b-row>

        <div class="row mx-auto mt-3 pl-3 pr-3 pt-3 border-top">
          <span class="text-danger notation text-center">
              <font-awesome-icon :icon="['fa', 'exclamation-triangle']"
              size="1x" fixed-width />
  <b>При сбросе основной почты</b> и выходе из CMS, пользователь больше не сможет войти!
  Будьте осторожны!
          </span>
        </div>

      </b-form>

    </b-modal>
-->
<!--
    <b-modal id="avatar-modal"
            @hidden="onResetImage"
            @close="onResetImage"
            title="Вклеить фотокарточку"
            hide-footer size="md" centered
            :header-bg-variant="'primary'"
            :header-text-variant="'light'">

      <div class=" row w-100 mx-auto pb-3 justify-content-center align-items-center">
        <img v-bind:src="imageUpdate.imageData ?
        imageUpdate.imageData : '/static/profile_avatars/default.png'"
        alt="Предпросмотр средний квадрат"
        class="profile-image-preview preview-md preview-square mr-4">

        <img v-bind:src="imageUpdate.imageData ?
        imageUpdate.imageData : '/static/profile_avatars/default.png'"
        alt="Предпросмотр средний"
        class="profile-image-preview preview-md mr-4">

        <img v-bind:src="imageUpdate.imageData ?
        imageUpdate.imageData : '/static/profile_avatars/default.png'"
        alt="Предпросмотр маленький"
        class="profile-image-preview preview-sm mr-4">

      </div>

      <b-form class="w-100" @submit.prevent="onSubmitAvatar(user.id)">
        <b-form-group
        description="Товарищам будет проще узнать Вас, если Вы вклеите свою настоящую фотокарточку.
Она должна соответствовать ГОСТам ДЖиПег, ГиФ или ПэНГэ. Размер ГОСТ 3МБ">

          <b-form-file
            ref="imageInput"
            @input="onSelectImage"
            lang="ru"
            placeholder="Выберите фотокарточку..."
            drop-placeholder="Бросьте сюда..."
            accept="image/jpeg, image/png, image/gif"
            :state="$v.imageUpdate.$dirty ? !$v.imageUpdate.$anyError : null"
          ></b-form-file>
          <b-form-invalid-feedback
          :state="$v.imageUpdate.$dirty ? !$v.imageUpdate.$anyError : null">
            <span v-if="!$v.imageUpdate.size.maxValue">
              Превышен лимит в 3 МБ для фотокарточки!
            </span>
            <span v-if="!$v.imageUpdate.type.isImage">
              Фотокарточка не соответствует ГОСТам ДЖиПег, ГиФ или ПэНГэ!
            </span>
          </b-form-invalid-feedback>

        </b-form-group>

        <b-button class="mb-3" type="submit" block variant="primary"
        title="Установить новую фотокарточку" v-b-tooltip.hover
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
-->

  </main>
</template>

<script>
import { mapState } from 'vuex';
import _ from 'lodash';
import {
  required, sameAs, minLength, maxLength,
} from 'vuelidate/lib/validators';
import Breadcumbs from './Breadcumbs';
import { EventBus } from '@/utils';


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
      },
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
        // alphaNum,
        alpha: val => /^[а-яёa-zА-ЯЁA-Z0-9]*$/i.test(val),
      },
    },
  },
  components: { Breadcumbs },
  computed: mapState({
    roles: state => state.roles,
    uid: state => state.uid,
    orderedList() {
      return _.orderBy(this.roles.results,
        this.listControl.orderBy.field,
        this.listControl.orderBy.asc ? 'asc' : 'desc');
    },
    formPending: state => state.formPending,
  }),
  beforeMount() {
    this.$store.dispatch('loadRoles', { start: this.listControl.start, limit: this.listControl.limit });
  },
  methods: {
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
