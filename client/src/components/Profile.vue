<template>
  <main class="container-fluid">
    <breadcumbs></breadcumbs>

    <div class="row w-100 mx-auto pb-3">

      <div class="col">
        <b-card tag="article" class="profile-form shaded"
        header-tag="header" footer-tag="footer" header-bg-variant="primary">

          <h3 slot="header" class="mb-0 small text-light">
            {{$t('userProfile.formEdit.formTitle')}}
          </h3>
          <b-card-text class="text-center">

            <b-form @submit="onSubmitData">

              <b-form-group>
                <b-form-input v-model="$v.profile.login.$model" name="login"
                  type="text"
                  autofocus
                  v-bind:placeholder="$t('userProfile.formEdit.formFields.login.placeholder')"
                  :state="$v.profile.login.$dirty ? !$v.profile.login.$error : null"
                  trim
                ></b-form-input>

                <b-form-invalid-feedback
                :state="$v.profile.login.$dirty ? !$v.profile.login.$error : null">
                  <span v-if="!$v.profile.login.required">
                    {{$t('userProfile.formEdit.formFields.login.errors.required')}}
                  </span>
                  <span v-if="!$v.profile.login.minLength">
                    {{$t('userProfile.formEdit.formFields.login.errors.minLength')}}
                  </span>
                  <span v-if="!$v.profile.login.maxLength">
                    {{$t('userProfile.formEdit.formFields.login.errors.maxLength')}}
                  </span>
                  <span v-if="!$v.profile.login.alphaNum">
                    {{$t('userProfile.formEdit.formFields.login.errors.alphaNum')}}
                  </span>
                </b-form-invalid-feedback>

              </b-form-group>

              <b-form-group>
                <b-input-group>
                  <b-form-input
                  v-bind:placeholder="$t('userProfile.formEdit.formFields.surname.placeholder')"
                  v-model="$v.profile.surname.$model"
                  :state="$v.profile.surname.$dirty ? !$v.profile.surname.$error : null"
                  name="surname" trim
                  @input="$v.profile.validationGroupFIO.$touch()">
                  </b-form-input>
                  <b-form-input
                  v-bind:placeholder="$t('userProfile.formEdit.formFields.name.placeholder')"
                  v-model="$v.profile.name.$model"
                  :state="$v.profile.name.$dirty ? !$v.profile.name.$error : null"
                  name="name" trim
                  @input="$v.profile.validationGroupFIO.$touch()">
                  </b-form-input>
                  <b-form-input
                  v-bind:placeholder="$t('userProfile.formEdit.formFields.patronymic.placeholder')"
                  v-model="$v.profile.patronymic.$model"
                  :state="$v.profile.patronymic.$dirty ? !$v.profile.patronymic.$error : null"
                  name="patronymic" trim
                  @input="$v.profile.validationGroupFIO.$touch()">
                  </b-form-input>
                </b-input-group>

                <b-form-invalid-feedback
                :state="$v.profile.validationGroupFIO.$dirty ?
                !$v.profile.validationGroupFIO.$anyError : null">
                  <span v-if="!$v.profile.surname.required">
                    {{$t('userProfile.formEdit.formFields.surname.errors.required')}}
                  </span>
                  <span v-if="!$v.profile.surname.minLength">
                    {{$t('userProfile.formEdit.formFields.surname.errors.minLength')}}
                  </span>
                  <span v-if="!$v.profile.surname.maxLength">
                    {{$t('userProfile.formEdit.formFields.surname.errors.maxLength')}}
                  </span>
                  <span v-if="!$v.profile.surname.alpha">
                    {{$t('userProfile.formEdit.formFields.surname.errors.alpha')}}
                  </span>
                  <span v-if="!$v.profile.name.required">
                    {{$t('userProfile.formEdit.formFields.name.errors.required')}}
                  </span>
                  <span v-if="!$v.profile.name.minLength">
                    {{$t('userProfile.formEdit.formFields.name.errors.minLength')}}
                  </span>
                  <span v-if="!$v.profile.name.maxLength">
                    {{$t('userProfile.formEdit.formFields.name.errors.maxLength')}}
                  </span>
                  <span v-if="!$v.profile.name.alpha">
                    {{$t('userProfile.formEdit.formFields.name.errors.alpha')}}
                  </span>
                  <span v-if="!$v.profile.patronymic.required">
                    {{$t('userProfile.formEdit.formFields.patronymic.errors.required')}}
                  </span>
                  <span v-if="!$v.profile.patronymic.minLength">
                    {{$t('userProfile.formEdit.formFields.patronymic.errors.minLength')}}
                  </span>
                  <span v-if="!$v.profile.patronymic.maxLength">
                    {{$t('userProfile.formEdit.formFields.patronymic.errors.maxLength')}}
                  </span>
                  <span v-if="!$v.profile.patronymic.alpha">
                    {{$t('userProfile.formEdit.formFields.patronymic.errors.alpha')}}
                  </span>
                </b-form-invalid-feedback>

              </b-form-group>

              <b-form-group class="text-justify"
              :description="$t('userProfile.formEdit.formFields.emails.description')">
                <b-form-group v-for="(v, index) in $v.profile.email.$each.$iter" v-bind:key="index">
                  <b-input-group>

                    <b-input-group-text slot="prepend" v-b-tooltip.hover
                    :title="$t('userProfile.formEdit.formFields.emails.titlePrimary')"
                    v-if="v.$model.type==='primary'">
                      <font-awesome-icon v-bind:icon="['fa', 'envelope']" fixed-width/>
                    </b-input-group-text>
                    <b-input-group-text slot="prepend" v-b-tooltip.hover
                    :title="$t('userProfile.formEdit.formFields.emails.titlePersonal')"
                    v-else-if="v.$model.type==='personal'">
                      <font-awesome-icon v-bind:icon="['fa', 'user']" fixed-width/>
                    </b-input-group-text>
                    <b-input-group-text slot="prepend" v-b-tooltip.hover
                    :title="$t('userProfile.formEdit.formFields.emails.titleWork')"
                    v-else-if="v.$model.type==='work'">
                      <font-awesome-icon v-bind:icon="['fa', 'briefcase']" fixed-width/>
                    </b-input-group-text>

                    <b-form-input
                      type="email"
                      v-bind:placeholder="$t('userProfile.formEdit.formFields.emails.placeholder')"
                      name="email"
                      v-model="v.value.$model"
                      trim
                      :state="v.value.$dirty ? !v.value.$error : null"
                    ></b-form-input>
                    <b-input-group-append>

                      <b-button v-if="v.$model.value && !v.value.$dirty &&
                      (dateDiffNow(v.$model.activeUntil, reactivationPeriod) || !v.$model.verified)"
                      variant="outline-secondary" v-b-tooltip.hover
                      :title="$t('userProfile.formEdit.formFields.emails.sendVerification')"
                      @click="onSubmitMailVerify(uid, v.$model.type, v.$model.value)"
                      :disabled="formPending">
                        <b-spinner small v-if="formPending"
                        :label="$t('pending')"></b-spinner>
                        <font-awesome-icon v-else v-bind:icon="['fa', 'envelope']" fixed-width/>
                      </b-button>

                      <b-input-group-text v-if="v.$model.value" v-b-tooltip.hover
                      :title="v.$model.verified ?
                      $t('userProfile.formEdit.formFields.emails.confirmationT') :
                      $t('userProfile.formEdit.formFields.emails.confirmationF')" >
                        <font-awesome-icon
                        v-bind:icon="['fa', 'check-circle']"
                        :class="v.$model.verified ? 'text-success' : 'text-danger'" fixed-width/>
                      </b-input-group-text>

                      <b-input-group-text v-if="v.$model.value" v-b-tooltip.hover
                       :title="v.$model.activeUntil ?
                        $t('userProfile.formEdit.formFields.emails.activity')+
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
                      {{$t('userProfile.formEdit.formFields.emails.errors.required')}}
                    </span>
                    <span v-if="!v.value.email">
                      {{$t('userProfile.formEdit.formFields.emails.errors.email')}}
                    </span>
                  </b-form-invalid-feedback>
                </b-form-group>
              </b-form-group>

              <b-form-group>
                <vue-tel-input
                autocomplete="off"
                :onlyCountries="['RU']"
                :disabledFetchingCountry="true"
                v-bind:placeholder="$t('userProfile.formEdit.formFields.phone.placeholder')"
                name="phone"
                v-model="$v.profile.phone.$model"
                :wrapperClasses="$v.profile.phone.$dirty ?
                (!$v.profile.phone.$error ?
                'is-valid input-group' : 'is-invalid input-group') : 'input-group'"
                :inputClasses="$v.profile.phone.$dirty ?
                (!$v.profile.phone.$error ?
                'is-valid form-control' : 'is-invalid form-control') : 'form-control'"

                :is-valid="$v.profile.phone.$dirty ? !$v.profile.phone.$error : null"
                />

                <b-form-invalid-feedback
                :state="$v.profile.phone.$dirty ? !$v.profile.phone.$error : null">
                  <span v-if="!$v.profile.phone.required">
                    {{$t('userProfile.formEdit.formFields.phone.errors.required')}}
                  </span>
                  <span v-if="!$v.profile.phone.format ">
                    {{$t('userProfile.formEdit.formFields.phone.errors.format')}}
                  </span>
                </b-form-invalid-feedback>
              </b-form-group>

              <b-form-group>
                <datepicker
                autocomplete="off"
                v-bind:placeholder="$t('userProfile.formEdit.formFields.birthDate.placeholder')"
                :format="dateFormatter" :bootstrap-styling="true"
                :language="russian" :typeable=false :required=true
                :monday-first=true :disabledDates="disabledDates"
                v-model="$v.profile.birth_date.$model" name="birth_date"
                :input-class="$v.profile.birth_date.$dirty ? 'is-valid' : null">
                </datepicker>

                <b-form-invalid-feedback
                :state="$v.profile.birth_date.$dirty ? !$v.profile.birth_date.$error : null">
                  <span v-if="!$v.profile.birth_date.required">
                    {{$t('userProfile.formEdit.formFields.birthDate.errors.required')}}
                  </span>
                </b-form-invalid-feedback>

              </b-form-group>

              <b-form-group>
                <b-form-textarea
                v-bind:placeholder="$t('userProfile.formEdit.formFields.aboutMe.placeholder')"
                autocomplete="off"
                rows="2" max-rows="6" no-resize
                v-model="$v.profile.about_me.$model" name="about_me"
                :state="$v.profile.about_me.$dirty ? !$v.profile.about_me.$error : null">
                </b-form-textarea>

                <b-form-invalid-feedback
                :state="$v.profile.about_me.$dirty ? !$v.profile.about_me.$error : null">
                  <span v-if="!$v.profile.about_me.maxLength">
                    {{$t('userProfile.formEdit.formFields.aboutMe.errors.maxLength')}}
                  </span>
                </b-form-invalid-feedback>

              </b-form-group>

              <b-button type="submit" variant="primary" class="float-left"
              :title="$t('userProfile.formEdit.submitButton')" v-b-tooltip.hover
              :disabled="!$v.profile.$anyDirty || $v.profile.$invalid">
                <font-awesome-icon v-if="!formPending"
                :icon="['fa', 'save']" fixed-width />
                <b-spinner small v-if="formPending"
                :label="$t('pending')"></b-spinner>
              </b-button>

            </b-form>

            <b-button variant="danger" class="float-right"
            :title="$t('userProfile.formEdit.changePasswordButton')" v-b-tooltip.hover
            @click="passwordUpdate.passwordNew = passwordGenerator(size=8)"
            v-b-modal.password-modal>
              <font-awesome-icon :icon="['fa', 'key']" fixed-width />
            </b-button>

          </b-card-text>

        </b-card>
      </div>

      <div class="col-3">
        <b-card tag="article" style="max-width: 20rem;" class="profile-card shaded text-center">
          <div class="card-profile-image mb-4 mx-auto">
            <div class="profile-image-overlay" v-b-tooltip.hover
            v-bind:title="$t('userProfile.tooltips.photoTitle')">
              <div v-b-modal.avatar-modal v-b-tooltip.hover
              v-bind:title="$t('userProfile.tooltips.photoUpdate')">
                <font-awesome-icon :icon="['fa', 'upload']" fixed-width />
              </div>
              <div @click="deleteProfileAvatar" v-b-tooltip.hover
              v-bind:title="$t('userProfile.tooltips.photoDelete')">
                <font-awesome-icon :icon="['fa', 'trash']" fixed-width />
              </div>
            </div>
            <img v-if="profile.photo" :src="'/static/profile_avatars/'+profile.photo"
            alt="Фотокарточка" class="profile-image">
            <img v-else :src="'/static/profile_avatars/default.png'"
            alt="Фотокарточка" class="profile-image">
          </div>
          <b-card-text class="text-center">
            <h3>{{profile.surname}}<br>
            {{profile.name}} {{profile.patronymic}}<br>
            @{{profile.login}}</h3>
            <h2 class="pb-4">Роль</h2>
            <p v-if=profile.about_me class="text-justify m-0 pt-3">{{profile.about_me}}</p>
          </b-card-text>
<!--
          <div slot="footer" class="text-left">
            <button type="button" title="Подключить ВКонтакте"
            class="mb-2 mr-2 btn"
            v-bind:class="[
                            { disabled: !profile.socials.vk },
                            { 'btn-outline-vk': !profile.socials.vk },
                            { 'btn-vk': profile.socials.vk }
                          ]">
                <font-awesome-icon :icon="['fab', 'vk']" fixed-width />
            </button>
            <button type="button" title="Подключить Одноклассники"
            class="mb-2 mr-2 btn"
            v-bind:class="[
                            { disabled: !profile.socials.ok },
                            { 'btn-outline-ok': !profile.socials.ok },
                            { 'btn-ok': profile.socials.ok }
                          ]">
                <font-awesome-icon :icon="['fab', 'odnoklassniki']" fixed-width />
            </button>
            <button type="button" title="Подключить Яндекс"
            class="mb-2 mr-2 btn"
            v-bind:class="[
                            { disabled: !profile.socials.yandex },
                            { 'btn-outline-yandex': !profile.socials.yandex },
                            { 'btn-yandex': profile.socials.yandex }
                          ]">
                <font-awesome-icon :icon="['fab', 'yandex']" fixed-width />
            </button>
            <button type="button" title="Подключить Google"
            class="mb-2 mr-2 btn"
            v-bind:class="[
                            { disabled: !profile.socials.google },
                            { 'btn-outline-google': !profile.socials.google },
                            { 'btn-google': profile.socials.google }
                          ]">
                <font-awesome-icon :icon="['fab', 'google']" fixed-width />
            </button>
          </div>
-->
        </b-card>

      </div>

    </div>

    <b-modal id="password-modal"
            v-bind:title="$t('userProfile.formPassword.formTitle')"
            hide-footer size="sm" centered
            :header-bg-variant="'danger'"
            :header-text-variant="'light'">

      <b-form class="w-100" @submit="onSubmitPassword">

        <b-form-group>
          <b-input-group>
            <b-input-group-prepend>
              <b-button variant="outline-secondary" v-on:click='isActiveOld = !isActiveOld'>
                <font-awesome-icon fixed-width
                v-bind:icon="isActiveOld ? ['far', 'eye-slash'] : ['far', 'eye']"
                v-bind:title="isActiveOld ? $t('userProfile.formPassword.activeButtonT') :
                $t('userProfile.formPassword.activeButtonF')"/>
              </b-button>
            </b-input-group-prepend>
            <b-form-input
              v-bind:type="isActiveOld ? 'text' : 'password'"
              v-bind:class="{ 'is-invalid': passwordError }"
              name="passwordOld"
              v-model="$v.passwordUpdate.passwordOld.$model"
              v-bind:placeholder="$t(
                'userProfile.formPassword.formFields.passwordOld.placeholder')">
            </b-form-input>
            <div class="invalid-feedback notation mt-2">
              <font-awesome-icon :icon="['fa', 'exclamation-triangle']"
              size="1x" fixed-width /> {{errorMsg}}
            </div>
          </b-input-group>
        </b-form-group>

        <b-form-group>
          <b-input-group>
            <b-input-group-prepend>
              <b-button variant="outline-secondary" v-on:click='isActiveNew = !isActiveNew'>
                <font-awesome-icon fixed-width
                v-bind:icon="isActiveNew ? ['far', 'eye-slash'] : ['far', 'eye']"
                v-bind:title="isActiveNew ? $t('userProfile.formPassword.activeButtonT') :
                $t('userProfile.formPassword.activeButtonF')"/>
              </b-button>
            </b-input-group-prepend>
            <b-form-input
              v-bind:type="isActiveNew ? 'text' : 'password'"
              v-model="passwordUpdate.passwordNew"
              name="passwordNew"
              readonly disabled
              v-bind:placeholder="$t(
                'userProfile.formPassword.formFields.passwordNew.placeholder')">
            </b-form-input>
            <b-input-group-append>
              <b-button variant="outline-primary"
              @click="passwordUpdate.passwordNew = passwordGenerator(size = 8)">
                <font-awesome-icon :icon="['fa', 'key']" fixed-width />
              </b-button>
            </b-input-group-append>
          </b-input-group>
          <b-form-text class="text-muted">
            <i18n path="userProfile.formPassword.formFields.passwordNew.description">
              <font-awesome-icon :icon="['fa', 'key']" fixed-width slot="key"/>
            </i18n>
          </b-form-text>
        </b-form-group>

        <b-form-group id="form-read-group">
          <b-form-checkbox name="passwordConfirm" required>
            <span class="notation noselect text-muted">
              {{$t('userProfile.formPassword.formFields.confirmation.text')}}
            </span>
          </b-form-checkbox>
        </b-form-group>

        <b-button class="mb-3" type="submit"
        block variant="primary" v-b-tooltip.hover
        v-bind:title="$t('userProfile.formPassword.saveButton')"
        :disabled="$v.passwordUpdate.$invalid">
          <font-awesome-icon :icon="['fa', 'save']" fixed-width />
        </b-button>

        <div class="row mx-auto pl-3 pr-3 pt-3 border-top">
          <span class="text-danger notation text-center">
              <font-awesome-icon :icon="['fa', 'exclamation-triangle']"
              size="1x" fixed-width />
            {{$t('userProfile.formPassword.formDescription')}}
          </span>
        </div>

      </b-form>
    </b-modal>

    <b-modal id="avatar-modal"
            v-bind:title="$t('userProfile.formAvatar.formTitle')"
            @hidden="onResetImage"
            @close="onResetImage"
            hide-footer size="md" centered
            :header-bg-variant="'primary'"
            :header-text-variant="'light'">

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

      <b-form class="w-100" @submit="onSubmitAvatar">

        <b-form-group
        :description="$t('userProfile.formAvatar.formDescription')">

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
              {{$t('userProfile.formAvatar.formFields.file.errors.maxValue')}}
            </span>
            <span v-if="!$v.imageUpdate.type.isImage">
              {{$t('userProfile.formAvatar.formFields.file.errors.isImage')}}
            </span>
          </b-form-invalid-feedback>

        </b-form-group>

        <b-button class="mb-3" type="submit" block variant="primary"
        v-bind:title="$t('userProfile.formAvatar.saveButton')" v-b-tooltip.hover
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
import VueTelInput from 'vue-tel-input';
import { ru } from 'vuejs-datepicker/dist/locale';
import moment from 'moment';
import { mapState } from 'vuex';
import {
  required, minLength, maxLength, alphaNum, email, maxValue, requiredIf,
} from 'vuelidate/lib/validators';
import Breadcumbs from './Breadcumbs';
import { EventBus, passwordGenerator, formatBytes } from '@/utils';
import { imageType } from '@/validators';

export default {
  name: 'Profile',
  data() {
    return {
      date: null,
      russian: ru,
      disabledDates: {
        from: new Date(),
      },
      file: null,
      preloadValue: 0,
      isActiveProgress: false,
      isActiveOld: false,
      isActiveNew: true,
      passwordUpdate: {
        passwordNew: '',
        passwordOld: '',
        login: this.$store.state.profile.login,
      },
      imageUpdate: {
        type: '',
        size: 0,
        imageData: '',
      },
      passwordError: false,
      errorMsg: '',
      passwordGenerator,
    };
  },
  validations: {
    profile: {
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
      validationGroupFIO: ['profile.name', 'profile.surname', 'profile.patronymic'],
    },
    passwordUpdate: {
      passwordOld: {
        required,
      },
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
  methods: {
    dateFormatter(date) {
      return moment(date).format('YYYY-MM-DD');
    },
    dateDiffNow(date, period) {
      if (moment().diff(date, 'days') <= -period) {
        return false;
      }
      return true;
    },
    onSubmitMailVerify(id, type, value) {
      this.$store.dispatch('verifyMailSend', { id, value, type });
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
    onSubmitData(evt) {
      evt.preventDefault();
      this.$v.$touch();

      if (!this.$v.profile.$invalid) {
        this.profile.birth_date = moment(this.profile.birth_date).format('YYYY-MM-DD');
        this.$store.dispatch('updateProfileData', this.profile);
      }
    },
    onSubmitPassword(evt) {
      evt.preventDefault();
      this.$v.passwordUpdate.$touch();
      if (!this.$v.passwordUpdate.$invalid) {
        this.passwordError = false;
        this.$store.dispatch('updateProfilePassword', this.passwordUpdate);
      }
    },
    onSubmitAvatar(evt) {
      evt.preventDefault();
      this.$v.imageUpdate.$touch();

      if (!this.$v.imageUpdate.$invalid) {
        const formData = new FormData();
        if (this.file) {
          formData.append('avatar', this.file[0]);
        }
        this.isActiveProgress = true;
        this.$store.dispatch('updateProfileAvatar', formData);
      }
    },
    deleteProfileAvatar() {
      this.$store.dispatch('deleteProfileAvatar');
    },
    onResetImage(evt) {
      evt.preventDefault();
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
  },
  computed: mapState({
    uid: state => state.uid,
    profile: state => state.profile,
    progressValue: state => state.uploadProgress,
    progressMax: state => state.uploadProgressMax,
    formPending: state => state.formPending,
    reactivationPeriod: state => state.reactivationPeriod,
  }),
  mounted() {
    EventBus.$on('failedAuthentication', (msg) => {
      if (msg.field === 'password') {
        this.passwordError = true;
      }
      this.errorMsg = msg.text;
    });
  },
  beforeDestroy() {
    EventBus.$off('failedAuthentication');
  },
};
</script>
