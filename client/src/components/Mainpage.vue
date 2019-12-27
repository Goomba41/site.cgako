<template>
  <main class="container-fluid d-flex flex-column">
    <breadcumbs></breadcumbs>

    <b-row class="pb-4 m-0 w-100 flex-grow-1 blocker"
    v-if="!can(user_perms, 'get', 'pages')">
      <b-col class="align-self-center text-center">
        <font-awesome-icon :icon="['fa', 'lock']" fixed-width size="10x"/>
      </b-col>
    </b-row>

    <div class="row p-3" v-if="can(user_perms, 'get', 'pages')">
      <b-card tag="article" class="shaded w-100"
        header-tag="header" footer-tag="footer" header-bg-variant="light">

          <h3 slot="header" class="mb-0 small text-dark">
            Памятные даты истории России
          </h3>
          <b-card-text class="text-center">

<!--
            <b-card
              no-body
              class="mb-3"
              v-for="(contact, cIndex) in building.employee_contacts.$each.$iter"
              v-bind:key="cIndex"
            >
              <b-card-header header-tag="header" class="p-0" role="tab">
                <b-button-group class="w-100">
                  <b-button
                    block
                    v-b-toggle="'contactAccordion-' + cIndex"
                    class="text-left"
                    variant="info"
                  >
                    <font-awesome-icon icon="address-book" fixed-width />
                    {{contact.surname.$model}}
                    <template v-if="contact.name.$model && contact.patronymic.$model">
                    {{contact.name.$model.slice(0, 1) + "."
                      + contact.patronymic.$model.slice(0, 1) + "."}}
                    </template>
                  </b-button>
                  <b-button
                    variant="danger"
                    v-if="can(user_perms, 'put', 'contacts')"
                    v-bind:title="$t(
                      'contacts.formEditBuildings.formFields.employee.deleteEmployeeButton')"
                    v-b-tooltip.hover
                    @click="buildings[bIndex].employee_contacts.splice(cIndex, 1);
                      building.$touch()"
                  >
                    <font-awesome-icon icon="trash" fixed-width />
                  </b-button>
                  <b-button
                    v-else
                    v-bind:title="$t(
                      'contacts.formEditBuildings.formFields.employee.deleteEmployeeButton')"
                    v-b-tooltip.hover
                  >
                    <font-awesome-icon :icon="['fa', 'lock']" fixed-width />
                  </b-button>
                </b-button-group>
              </b-card-header>
              <b-collapse
                :id="`contactAccordion-${cIndex}`"
                accordion="contact"
                role="tabpanel"
              >
                <b-list-group flush>
                  <b-list-group-item>
                    <b-row>
                      <b-col :cols="contact.$model.cid ? 9 : 12">
                        <b-form-group class="">
                          <b-form-input
                            :type="'text'"
                            v-model="contact.post.$model"
                            v-bind:placeholder="$t(
                              'contacts.formEditBuildings.'
                              +'formFields.employee.post.placeholder')"
                            :state="contact.post.$dirty ?
                              !contact.post.$error : null"
                          >
                          </b-form-input>

                          <b-form-invalid-feedback>
                            <span v-if="!contact.post.required">
                              {{$t('contacts.formEditBuildings'+
                                  '.formFields.employee.post.errors.required')}}
                            </span>
                            <span v-if="!contact.post.maxLength">
                              {{$t('contacts.formEditBuildings'+
                                  '.formFields.employee.post.errors.maxLength')}}
                            </span>
                            <span v-if="!contact.post.alpha">
                              {{$t('contacts.formEditBuildings'+
                                  '.formFields.employee.post.errors.alpha')}}
                            </span>
                          </b-form-invalid-feedback>
                        </b-form-group>

                        <b-form-group class="">
                          <b-input-group>
                            <b-form-input
                              :type="'text'"
                              v-model="contact.surname.$model"
                              v-bind:placeholder="$t(
                                'contacts.formEditBuildings.'
                                +'formFields.employee.surname.placeholder')"
                              :state="contact.surname.$dirty ?
                                !contact.surname.$error : null"
                            >
                            </b-form-input>
                            <b-form-input
                              :type="'text'"
                              v-model="contact.name.$model"
                              v-bind:placeholder="$t(
                                'contacts.formEditBuildings.'
                                +'formFields.employee.name.placeholder')"
                              :state="contact.name.$dirty ?
                                !contact.name.$error : null"
                            >
                            </b-form-input>
                            <b-form-input
                              :type="'text'"
                              v-model="contact.patronymic.$model"
                              v-bind:placeholder="$t(
                                'contacts.formEditBuildings.'
                                +'formFields.employee.patronymic.placeholder')"
                              :state="contact.patronymic.$dirty ?
                                !contact.patronymic.$error : null"
                            >
                            </b-form-input>
                          </b-input-group>

                          <b-form-invalid-feedback
                            :state="(
                              contact.patronymic.$dirty
                              || contact.name.$dirty
                              || contact.surname.$dirty) ?
                              !(contact.patronymic.$error
                              || contact.name.$error
                              || contact.surname.$error) : null">
                            <span v-if="!contact.name.required">
                              {{$t('contacts.formEditBuildings'+
                                  '.formFields.employee.name.errors.required')}}
                            </span>
                            <span v-if="!contact.name.maxLength">
                              {{$t('contacts.formEditBuildings'+
                                  '.formFields.employee.name.errors.maxLength')}}
                            </span>
                            <span v-if="!contact.name.alpha">
                              {{$t('contacts.formEditBuildings'+
                                  '.formFields.employee.name.errors.alpha')}}
                            </span>
                            <span v-if="!contact.surname.required">
                              {{$t('contacts.formEditBuildings'+
                                  '.formFields.employee.surname.errors.required')}}
                            </span>
                            <span v-if="!contact.surname.maxLength">
                              {{$t('contacts.formEditBuildings'+
                                  '.formFields.employee.surname.errors.maxLength')}}
                            </span>
                            <span v-if="!contact.surname.alpha">
                              {{$t('contacts.formEditBuildings'+
                                  '.formFields.employee.surname.errors.alpha')}}
                            </span>
                            <span v-if="!contact.patronymic.required">
                              {{$t('contacts.formEditBuildings'+
                                  '.formFields.employee.patronymic.errors.required')}}
                            </span>
                            <span v-if="!contact.patronymic.maxLength">
                              {{$t('contacts.formEditBuildings'+
                                  '.formFields.employee.patronymic.errors.maxLength')}}
                            </span>
                            <span v-if="!contact.patronymic.alpha">
                              {{$t('contacts.formEditBuildings'+
                                  '.formFields.employee.patronymic.errors.alpha')}}
                            </span>
                          </b-form-invalid-feedback>
                        </b-form-group>
                      </b-col>

                      <b-col cols="3" v-if="contact.$model.cid">
                        <div class="card-profile-image mx-auto mb-3">
                          <div
                            class="profile-image-overlay"
                            v-if="can(user_perms, 'put', 'contacts')"
                          >
                            <div
                              v-b-tooltip.hover
                              v-b-modal.employee-photo-modal
                              v-if="can(user_perms, 'put', 'contacts')"
                              @click="selectedContact = {
                                'cid':contact.$model.cid, 'bid':building.$model.id }"
                              v-bind:title="$t('contacts.formEditBuildings'
                                +'.formFields.employee.photo.updateEmployeePhoto')"
                            >
                              <font-awesome-icon :icon="['fa', 'upload']" fixed-width />
                            </div>
                            <div
                              v-b-tooltip.hover
                              v-else
                              v-bind:title="$t('contacts.formEditBuildings'
                                +'.formFields.employee.photo.updateEmployeePhoto')"
                            >
                              <font-awesome-icon :icon="['fa', 'lock']" fixed-width />
                            </div>
                            <div
                              v-if="contact.photo.$model
                                && can(user_perms, 'put', 'contacts')"
                              v-b-tooltip.hover
                              v-bind:title="$t('contacts.formEditBuildings'
                                +'.formFields.employee.photo.deleteEmployeePhoto')"
                              @click="deleteEmployeePhoto(
                                { 'cid':contact.$model.cid, 'bid':building.$model.id })"
                            >
                              <font-awesome-icon :icon="['fa', 'trash']" fixed-width />
                            </div>
                          </div>
                          <img
                            v-if="contact.photo.$model"
                            :src="'/static/contact_photos/'+contact.photo.$model"
                            alt="Фотокарточка"
                            class="profile-image"
                          >
                          <img v-else :src="'/static/contact_photos/default.png'"
                          alt="Фотокарточка" class="profile-image">
                        </div>
                      </b-col>
                    </b-row>

                    <b-form-group>
                      <b-form-input
                        :type="'text'"
                        v-model="contact.email.$model"
                        v-bind:placeholder="$t(
                          'contacts.formEditBuildings.'
                          +'formFields.employee.email.placeholder')"
                        :state="contact.email.$dirty ?
                          !contact.email.$error : null"
                      >
                      </b-form-input>

                      <b-form-invalid-feedback>
                        <span v-if="!contact.email.required">
                          {{$t('contacts.formEditBuildings'+
                              '.formFields.employee.email.errors.required')}}
                        </span>
                        <span v-if="!contact.email.email">
                          {{$t('contacts.formEditBuildings'+
                              '.formFields.employee.email.errors.email')}}
                        </span>
                      </b-form-invalid-feedback>
                    </b-form-group>
                    <b-form-group>
                      <vue-tel-input
                      autocomplete="off"
                      :onlyCountries="['RU']"
                      :disabledFetchingCountry="true"
                      :maxLen="16"
                      v-bind:placeholder="$t(
                        'contacts.formEditBuildings.formFields.employee.phone.placeholder')"
                      name="phone"
                      v-model="contact.phone.$model"
                      :wrapperClasses="contact.phone.$dirty ?
                      (!contact.phone.$error ?
                      'is-valid input-group' : 'is-invalid input-group') : 'input-group'"
                      :inputClasses="contact.phone.$dirty ?
                      (!contact.phone.$error ?
                      'is-valid form-control' : 'is-invalid form-control') : 'form-control'"

                      :is-valid="contact.phone.$dirty ? !contact.phone.$error : null"
                      />

                      <b-form-invalid-feedback>
                        <span v-if="!contact.phone.required">
                          {{$t('contacts.formEditBuildings'+
                              '.formFields.employee.phone.errors.required')}}
                        </span>
                        <span v-if="!contact.phone.maxLength">
                          {{$t('contacts.formEditBuildings'+
                              '.formFields.employee.phone.errors.maxLength')}}
                        </span>
                      </b-form-invalid-feedback>
                    </b-form-group>
                  </b-list-group-item>

                </b-list-group>
              </b-collapse>

            </b-card>
-->
            <b-card
              no-body
              class="mb-3"
              v-for="(event, eIndex) in historyEvents.results"
              v-bind:key="eIndex"
            >
              <b-card-header header-tag="header" class="p-0" role="tab">
                <b-button-group class="w-100">
                  <b-button
                    block
                    v-b-toggle="'eventAccordion-' + eIndex"
                    class="text-left"
                    variant="info"
                  >
                    <font-awesome-icon icon="calendar" fixed-width />
                    {{event.event_title}}
                  </b-button>
                  <b-button
                    variant="danger"
                    v-if="can(user_perms, 'put', 'mainpage')"
                    v-bind:title="$t(
                      'contacts.formEditBuildings.formFields.employee.deleteEmployeeButton')"
                    v-b-tooltip.hover
                  >
                    <font-awesome-icon icon="trash" fixed-width />
                  </b-button>
                  <b-button
                    v-else
                    v-bind:title="$t(
                      'contacts.formEditBuildings.formFields.employee.deleteEmployeeButton')"
                    v-b-tooltip.hover
                  >
                    <font-awesome-icon :icon="['fa', 'lock']" fixed-width />
                  </b-button>
                </b-button-group>
              </b-card-header>
              <b-collapse
                :id="`eventAccordion-${eIndex}`"
                accordion="event"
                role="tabpanel"
              >
                <b-list-group flush>
                  <b-list-group-item>

                    <b-form-group>
                      <b-form-input
                        :type="'text'"
                        v-model="event.title"
                        v-bind:placeholder="$t(
                          'contacts.formEditBuildings.'
                          +'formFields.employee.email.placeholder')"
                      >
                      </b-form-input>

<!--
                      <b-form-invalid-feedback>
                        <span v-if="!contact.email.required">
                          {{$t('contacts.formEditBuildings'+
                              '.formFields.employee.email.errors.required')}}
                        </span>
                        <span v-if="!contact.email.email">
                          {{$t('contacts.formEditBuildings'+
                              '.formFields.employee.email.errors.email')}}
                        </span>
                      </b-form-invalid-feedback>
-->
                    </b-form-group>

                  </b-list-group-item>

                </b-list-group>
              </b-collapse>

            </b-card>


          </b-card-text>

        </b-card>
    </div>
  </main>
</template>

<script>
import moment from 'moment';
import { mapState } from 'vuex';
// import _ from 'lodash';
// import {
// required, sameAs, minLength, maxLength, maxValue,
// } from 'vuelidate/lib/validators';
import Breadcumbs from './Breadcumbs';
import {
  can,
} from '@/utils';

export default {
  name: 'Mainpage',
  data() {
    return {
      can,
    };
  },
  validations: {

  },
  components: {
    Breadcumbs,
  },
  computed: mapState({
    user_perms: state => state.user_perms,
    historyEvents: state => state.historyEvents,
    uid: state => state.uid,
    formPending: state => state.formPending,
  }),
  watch: {
    user_perms() {
      if (can(this.user_perms, 'get', 'mainpage')) {
        this.$store.dispatch('loadHistoryEvents', { start: 1, limit: 10 });
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
        for (let i = 0; i < this.pages.results.length; i += 1) {
          this.selected.push(this.pages.results[i].id);
        }
      }
    },
  },
};
</script>
