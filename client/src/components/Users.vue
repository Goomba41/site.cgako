<template>
  <main class="container-fluid">
    <breadcumbs></breadcumbs>

    <b-row class="pb-4 m-0 w-100">
      <b-col align-self="start" class="text-center" sm="8">
        <b-row class="justify-content-start align-middle align-items-center">
          <span class="text-info pr-3">
            Всего {{ users.count }}
            {{ users.count | declension(["товарищ", "товарища", "товарищей"]) }}
          </span>
          <b-button title="Новое досье" v-b-tooltip.hover class="mr-1" size="sm" variant="success"
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
              Удалить
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
             title="Навигация по страницам" v-b-tooltip.hover>
              <b-form-input type="number" min=1 :max="users.pages"
              autocomplete="off"
              v-model="listControl.page"
              v-on:input="listBegin(); listChange()"/>
            </b-input-group>
          </b-col>
          <b-col sm="4">
            <b-input-group prepend="По:" size="sm"
             title="Показывать на странице" v-b-tooltip.hover>
              <b-form-input type="number" min=1 :max="users.count - listControl.start + 1"
              autocomplete="off"
              v-model="listControl.limit"
              v-on:input="listChange(); listControl.page = 1"/>
            </b-input-group>
          </b-col>
          <b-col sm="4">
            <b-input-group prepend="С:" size="sm"
             title="Начать с записи" v-b-tooltip.hover>
              <b-form-input type="number" min=1 :max="users.count"
              autocomplete="off"
              v-model="listControl.start"
              v-on:input="listRows(); listChange()"/>
            </b-input-group>
          </b-col>
        </b-row>
      </b-col>

    </b-row>

    <div class="row p-3">
      <table class="table table-hover td-align-middle">
        <thead>
          <tr class="text-center">
            <th scope="col">
              <b-form-checkbox v-model="selectAll" @change="select"></b-form-checkbox>
            </th>
            <th scope="col">Фотокарточка</th>
            <th scope="col">
              Пользователь
              <font-awesome-icon icon="sort"
              fixed-width
              @click="listControl.orderBy.field='surname';
              listControl.orderBy.asc=!listControl.orderBy.asc"/>
              </th>
            <th scope="col">Роли</th>
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
            <td>
              <div class="card-profile-image mx-auto">
                <div  v-if="uid != user.id" class="profile-image-overlay"
                v-b-tooltip.hover title="Фотокарточка">
                  <div v-b-modal.avatar-modal v-b-tooltip.hover
                  @click="selectUser(user.id)" title="Вклеить новую">
                    <font-awesome-icon :icon="['fa', 'upload']" fixed-width />
                  </div>
                  <div v-if="user.photo" v-b-tooltip.hover
                  title="Вырезать" @click="deleteAvatar(user.id)">
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
            $options.filters.moment(user.last_login.datetime, 'dddd, MMMM Do YYYY, HH:mm:ss') :
            'Не входил'" v-b-tooltip.hover>
              {{user.last_login && user.last_login.datetime ?
                $options.filters.moment(user.last_login.datetime, 'from') : 'Не входил'}}
              <br>
              {{user.last_login && user.last_login.ip ?
                user.last_login.ip : ''}}
              <font-awesome-icon v-if="user.last_login && user.last_login.agent"
              :icon="['far', 'window-maximize']" fixed-width
              v-bind:title="user.last_login && user.last_login.browser ?
                user.last_login.browser : 'Неизвестный браузер'" v-b-tooltip.hover/>

              <font-awesome-icon v-if="user.last_login && user.last_login.device
              && user.last_login.device==='pc'"
              v-bind:icon="['fa', 'desktop']" fixed-width
              v-bind:title="user.last_login && user.last_login.device ?
                'Компьютер': 'Неизвестное устройство'" v-b-tooltip.hover/>
              <font-awesome-icon v-else-if="user.last_login && user.last_login.device
              && user.last_login.device==='tablet'"
              v-bind:icon="['fa', 'tablet-alt']" fixed-width
              v-bind:title="user.last_login && user.last_login.device ?
                'Планшет' : 'Неизвестное устройство'" v-b-tooltip.hover/>
              <font-awesome-icon v-else-if="user.last_login && user.last_login.device
              && user.last_login.device==='mobile'"
              v-bind:icon="['fa', 'mobile-alt']" fixed-width
              v-bind:title="user.last_login && user.last_login.device ?
                'Телефон' : 'Неизвестное устройство'" v-b-tooltip.hover/>

              <font-awesome-icon v-if="user.last_login && user.last_login.os
              && user.last_login.os.includes('Windows')"
              v-bind:icon="['fab', 'windows']" fixed-width
              class="text-primary"
              v-bind:title="user.last_login && user.last_login.os ?
                user.last_login.os: 'Неизвестное устройство'" v-b-tooltip.hover/>
              <font-awesome-icon v-else-if="user.last_login && user.last_login.os
              && user.last_login.os.includes('Mac')"
              v-bind:icon="['fab', 'apple']" fixed-width
              v-bind:title="user.last_login && user.last_login.os ?
                user.last_login.os : 'Неизвестное устройство'" v-b-tooltip.hover/>
              <font-awesome-icon v-else-if="user.last_login && user.last_login.os"
              v-bind:icon="['fab', 'linux']" fixed-width
              v-bind:title="user.last_login && user.last_login.os ?
                user.last_login.os : 'Неизвестное устройство'" v-b-tooltip.hover/>

            </td>
            <td>
              <span class="weight-100 small text-muted d-block mx-auto" v-if="uid==user.id">
                Для управления <br> собственным досье <br> воспользуйтесь
                <router-link :to="{ name: 'UserProfile' }">профилем</router-link>
              </span>
              <b-button size="sm" title="Изменить досье" v-b-tooltip.hover variant="primary"
              v-b-modal.edit-modal @click="selectUser(user.id)" v-if="uid!=user.id">
                <font-awesome-icon :icon="['fa', 'pencil-alt']" fixed-width />
              </b-button>

              <b-button size="sm" title="Экстренная связь" v-b-tooltip.hover variant="info"
              v-b-modal.contacts-modal
              @click="selectUser(user.id)" v-if="uid!=user.id">
                <font-awesome-icon :icon="['fa', 'info']" fixed-width />
              </b-button>

              <b-button v-if="uid != user.id"
              size="sm" title="Уничтожить досье" variant="danger"
              v-b-tooltip.hover
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
            @hidden="user={}"
            @close="user={}"
            title="Экстренная связь"
            v-b-tooltip.hover
            hide-footer size="sm" centered
            header-bg-variant="info"
            header-text-variant="light">
      <p v-for="mail in this.user.email" v-bind:key="mail.value">
        <a v-if="mail.value" :href="`mailto:${mail.value}`" title="Написать на эту почту"
        v-b-tooltip.hover>
          <font-awesome-icon title="Личная почта" v-b-tooltip.hover
          v-if="mail.type==='personal'"
          v-bind:icon="['fa', 'user']" fixed-width/>
          <font-awesome-icon title="Основная почта" v-b-tooltip.hover
          v-else-if="mail.type==='primary'"
          v-bind:icon="['fa', 'at']" fixed-width/>
          <font-awesome-icon title="Рабочая почта" v-b-tooltip.hover
          v-else-if="mail.type==='work'"
          v-bind:icon="['fa', 'briefcase']" fixed-width/>
          <font-awesome-icon
          :title="mail.verified ? 'Подтверждена' : 'Не подтверждена'"
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
             title="Уничтожение досье"
             v-b-tooltip.hover
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
        v-b-tooltip.hover
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
             v-b-tooltip.hover
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
        v-b-tooltip.hover
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

    <b-modal id="new-modal"
            title="Новое досье"
            hide-footer size="xl" centered
            @show="newUser.password=passwordGenerator(size=8)"
            :header-bg-variant="'success'"
            :header-text-variant="'light'"
            @hidden="onReset">

      <b-form class="w-100" @submit.prevent="onSubmitNewUser" @reset="onReset">

        <b-form-group>
          <b-form-input name="login"
            type="text"
            autofocus
            placeholder="Логин"
            trim
            v-model="$v.newUser.login.$model"
            :state="$v.newUser.login.$dirty ? !$v.newUser.login.$error : null"
          ></b-form-input>

          <b-form-invalid-feedback
          :state="$v.newUser.login.$dirty ? !$v.newUser.login.$error : null">
            <span v-if="!$v.newUser.login.required">
              Поле обязательно для заполнения!
            </span>
            <span v-if="!$v.newUser.login.minLength">
              Поле должно содержать минимум 4 символа!
            </span>
            <span v-if="!$v.newUser.login.maxLength">
              Поле может содержать максимум 20 символов!
            </span>
            <span v-if="!$v.newUser.login.alphaNum">
              Поле может содержать только латинские буквы и цифры!
            </span>
          </b-form-invalid-feedback>

        </b-form-group>

        <b-form-group>
          <b-input-group>
            <b-input-group-prepend>
              <b-button variant="outline-secondary"
              v-on:click='isActivePassword = !isActivePassword'>
                <font-awesome-icon fixed-width
                v-bind:icon="isActivePassword ? ['far', 'eye-slash'] : ['far', 'eye']"
                v-bind:title="isActivePassword ? 'Скрыть' : 'Показать'" v-b-tooltip.hover/>
              </b-button>
            </b-input-group-prepend>
            <b-form-input
              :state="!$v.newUser.password.$dirty ? !$v.newUser.password.$error : null"
              v-bind:type="isActivePassword ? 'text' : 'password'"
              name="password"
              readonly disabled
              v-model="$v.newUser.password.$model"
              placeholder="Новый пароль">
            </b-form-input>
            <b-input-group-append>
              <b-button variant="outline-primary"
              title="Сгенерировать" v-b-tooltip.hover
              @click="newUser.password = passwordGenerator(size=8)">
                <font-awesome-icon :icon="['fa', 'key']" fixed-width />
              </b-button>
            </b-input-group-append>
          </b-input-group>

          <b-form-invalid-feedback
          :state="$v.newUser.password.$dirty ? !$v.newUser.password.$error : null">
            <span v-if="!$v.newUser.password.required">
              Поле обязательно для заполнения!
            </span>
          </b-form-invalid-feedback>
           <b-form-text slot="description">
            Пароль генерируется автоматически. Нажмите кнопку
            <font-awesome-icon :icon="['fa', 'key']" fixed-width />
            чтобы сгенерировать новый.
          </b-form-text>
        </b-form-group>

        <b-form-group>
          <b-input-group>
            <b-form-input placeholder="Фамилия"
            v-model="$v.newUser.surname.$model"
            :state="$v.newUser.surname.$dirty ? !$v.newUser.surname.$error : null"
            name="surname" trim
            @input="$v.newUser.validationGroupFIO.$touch()">
            </b-form-input>
            <b-form-input placeholder="Имя"
            v-model="$v.newUser.name.$model"
            :state="$v.newUser.name.$dirty ? !$v.newUser.name.$error : null"
            name="name" trim
            @input="$v.newUser.validationGroupFIO.$touch()">
            </b-form-input>
            <b-form-input placeholder="Отчество"
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
              Фамилия обязательна для заполнения!
            </span>
            <span v-if="!$v.newUser.surname.minLength">
              Фамилия должна содержать минимум 4 символа!
            </span>
            <span v-if="!$v.newUser.surname.maxLength">
              Фамилия может содержать максимум 20 символов!
            </span>
            <span v-if="!$v.newUser.surname.alpha">
              Фамилия может содержать только русские буквы!
            </span>
            <span v-if="!$v.newUser.name.required">
              Имя обязательно для заполнения!
            </span>
            <span v-if="!$v.newUser.name.minLength">
              Имя должно содержать минимум 4 символа!
            </span>
            <span v-if="!$v.newUser.name.maxLength">
              Имя может содержать максимум 20 символов!
            </span>
            <span v-if="!$v.newUser.name.alpha">
              Имя может содержать только русские буквы!
            </span>
            <span v-if="!$v.newUser.patronymic.required">
              Отчество обязательно для заполнения!
            </span>
            <span v-if="!$v.newUser.patronymic.minLength">
              Отчество должно содержать минимум 4 символа!
            </span>
            <span v-if="!$v.newUser.patronymic.maxLength">
              Отчество может содержать максимум 20 символов!
            </span>
            <span v-if="!$v.newUser.patronymic.alpha">
              Отчество может содержать русские только буквы!
            </span>
          </b-form-invalid-feedback>
        </b-form-group>

        <b-form-group class="text-justify">
          <b-form-group v-for="(v, index) in $v.newUser.email.$each.$iter" v-bind:key="index">
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
            Для неё будет отправлено письмо с авторизационными данными и
            ссылкой подтверждения.
          </b-form-text>
        </b-form-group>

        <b-form-group>
          <vue-tel-input
          autocomplete="off"
          :onlyCountries="['RU']"
          :disabledFetchingCountry="true"
          :placeholder="'Номер телефона'"
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
              Поле обязательно для заполнения!
            </span>
            <span v-if="!$v.newUser.phone.format ">
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
          v-model="$v.newUser.birth_date.$model" name="birth_date"
          :input-class="($v.newUser.birth_date.$dirty) ?
          ((!$v.newUser.birth_date.$error) ? 'is-valid' : 'is-invalid') : null">
          </datepicker>

          <b-form-invalid-feedback
          :state="$v.newUser.birth_date.$dirty ? !$v.newUser.birth_date.$error : null">
            <span v-if="!$v.newUser.birth_date.required">
              Поле обязательно для заполнения!
            </span>
          </b-form-invalid-feedback>
        </b-form-group>

        <b-form-group>
          <b-form-textarea placeholder="О себе"
          autocomplete="off"
          rows="2" max-rows="6" no-resize
          v-model="$v.newUser.about_me.$model" name="about_me"
          :state="$v.newUser.about_me.$dirty ? !$v.newUser.about_me.$error : null">
          </b-form-textarea>

          <b-form-invalid-feedback
          :state="$v.newUser.about_me.$dirty ? !$v.newUser.about_me.$error : null">
            <span v-if="!$v.newUser.about_me.maxLength">
              Поле может содержать максимум 140 символов!
            </span>
          </b-form-invalid-feedback>
        </b-form-group>

        <b-row>
          <b-col>
            <b-button type="submit" variant="success" block
            title="Внести новое досье" v-b-tooltip.hover
            :disabled="!$v.newUser.$anyDirty || $v.newUser.$invalid">
              <font-awesome-icon v-if="!formPending"
              :icon="['fa', 'save']" fixed-width />
              <b-spinner small v-if="formPending"
              label="Идет отправка досье..."></b-spinner>
            </b-button>
          </b-col>
          <b-col>
            <b-button type="reset" variant="danger" block
            title="Стереть данные" v-b-tooltip.hover
            :disabled="!$v.newUser.$anyDirty">
              <font-awesome-icon v-if="!formPending"
              :icon="['fa', 'times']" fixed-width />
              <b-spinner small v-if="formPending"
              label="Идет отправка досье..."></b-spinner>
            </b-button>
          </b-col>
        </b-row>

        <div class="row mx-auto mt-3 pl-3 pr-3 pt-3 border-top">
          <span class="text-danger notation text-center">
              <font-awesome-icon :icon="['fa', 'exclamation-triangle']"
              size="1x" fixed-width />
  Авторизационные данные будут отправлены пользователю
  на основную почту. Будьте внимательны при её заполнении,
  чтобы данные для входа не попали в чужие руки!
          </span>
        </div>

      </b-form>

    </b-modal>

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
import Breadcumbs from './Breadcumbs';
import {
  EventBus, passwordGenerator, dateDiffNow, formatBytes,
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
      sameAsPassphrase: sameAs(() => 'Удалить'),
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
  components: { Breadcumbs, Datepicker, VueTelInput },
  computed: mapState({
    users: state => state.users,
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
  beforeMount() {
    this.$store.dispatch('loadUsers', { start: this.listControl.start, limit: this.listControl.limit });
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
