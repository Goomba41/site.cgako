<template>
  <main class="container-fluid d-flex flex-column">
    <breadcumbs></breadcumbs>

    <b-row class="pb-4 m-0 w-100 flex-grow-1 blocker"
    v-if="!can(user_perms, 'get', 'contacts')">
      <b-col class="align-self-center text-center">
        <font-awesome-icon :icon="['fa', 'lock']" fixed-width size="10x"/>
      </b-col>
    </b-row>

    <template v-else>
      <b-row class="pb-4">
        <b-col>

          <b-card class="shaded"
            header-bg-variant="primary">

            <h3 slot="header" class="mb-0 small text-light">
              {{$t('contacts.formEditCompanyInfo.formTitle')}}
            </h3>
            <b-card-text class="text-center">
              <b-form @submit.prevent="updateCompany">
                <b-form-group id="input-group-1">
                  <b-form-input
                    id="input-1"
                    type="text"
                    v-model="$v.organization.full_company_name.$model"
                    v-bind:placeholder="$t(
                      'contacts.formEditCompanyInfo.formFields.fullCompanyName.placeholder')"
                    :state="$v.organization.full_company_name.$dirty ?
                      !$v.organization.full_company_name.$error : null"
                  ></b-form-input>
                  <b-form-invalid-feedback>
                    <span v-if="!$v.organization.full_company_name.required">
                      {{$t('contacts.formEditCompanyInfo.'
                        +'formFields.fullCompanyName.errors.required')}}
                    </span>
                    <span v-if="!$v.organization.full_company_name.maxLength">
                      {{$t('contacts.formEditCompanyInfo.'
                        +'formFields.fullCompanyName.errors.maxLength')}}
                    </span>
                    <span v-if="!$v.organization.full_company_name.alpha">
                      {{$t('contacts.formEditCompanyInfo.formFields.fullCompanyName.errors.alpha')}}
                    </span>
                  </b-form-invalid-feedback>
                </b-form-group>

                <b-form-group>
                  <b-form-input
                    id="input-2"
                    v-model="$v.organization.company_name.$model"
                    v-bind:placeholder="$t(
                      'contacts.formEditCompanyInfo.formFields.companyName.placeholder')"
                    :state="$v.organization.company_name.$dirty ?
                      !$v.organization.company_name.$error : null"
                  ></b-form-input>
                  <b-form-invalid-feedback>
                    <span v-if="!$v.organization.company_name.required">
                      {{$t('contacts.formEditCompanyInfo.formFields.companyName.errors.required')}}
                    </span>
                    <span v-if="!$v.organization.company_name.maxLength">
                      {{$t('contacts.formEditCompanyInfo.formFields.companyName.errors.maxLength')}}
                    </span>
                    <span v-if="!$v.organization.company_name.alpha">
                      {{$t('contacts.formEditCompanyInfo.formFields.companyName.errors.alpha')}}
                    </span>
                  </b-form-invalid-feedback>
                </b-form-group>

                <b-card no-body class="mb-3">
                  <b-card-header header-tag="header" class="p-0" role="tab">
                    <b-button
                      block
                      v-b-toggle.requisitesAccordion
                      variant="info"
                      v-bind:title="$t('contacts.formEditCompanyInfo.'
                      +'formFields.requisites.buttonTitle')"
                      v-b-tooltip.hover
                    >
                      <font-awesome-icon icon="money-check-alt" fixed-width />
                      {{$t('contacts.formEditCompanyInfo.formFields.requisites.buttonTitle')}}
                    </b-button>
                  </b-card-header>
                  <b-collapse id="requisitesAccordion" accordion="requisites" role="tabpanel">
                    <b-list-group flush>
                      <b-list-group-item
                        v-for="(requisite, rIndex) in $v.organization.requisites.$each.$iter"
                        v-bind:key="rIndex"
                      >
                        <b-form-group class="m-0">
                          <b-input-group>
                            <b-form-input
                              :type="'text'"
                              v-model="requisite.title.$model"
                              v-bind:placeholder="$t(
                                'contacts.formEditCompanyInfo.'
                                +'formFields.requisites.title.placeholder')"
                              :state="requisite.title.$dirty ?
                                !requisite.title.$error : null"
                            >
                            </b-form-input>
                            <b-form-input
                              :type="'text'"
                              v-model="requisite.value.$model"
                              v-bind:placeholder="$t(
                                'contacts.formEditCompanyInfo.'
                                +'formFields.requisites.value.placeholder')"
                              :state="requisite.value.$dirty ?
                                !requisite.value.$error : null"
                            >
                            </b-form-input>

                            <b-input-group-append>
                              <b-button
                                variant="danger"
                                v-if="can(user_perms, 'put', 'contacts')"
                                @click="organization.requisites.splice(rIndex, 1);
                                  $v.organization.requisites.$touch()"
                                v-bind:title="$t(
                                  'contacts.formEditCompanyInfo.'
                                  +'formFields.requisites.buttonDelete')"
                                v-b-tooltip.hover
                              >
                                <font-awesome-icon icon="trash" fixed-width />
                              </b-button>
                              <b-button
                                v-else
                                v-bind:title="$t(
                                  'contacts.formEditCompanyInfo.'
                                  +'formFields.requisites.buttonDelete')"
                                v-b-tooltip.hover
                              >
                                <font-awesome-icon :icon="['fa', 'lock']" fixed-width />
                              </b-button>
                            </b-input-group-append>
                            <b-form-invalid-feedback>
                              <span v-if="!requisite.title.required">
                                {{$t('contacts.formEditCompanyInfo'+
                                    '.formFields.requisites.title.errors.required')}}
                              </span>
                              <span v-if="!requisite.title.minLength">
                                {{$t('contacts.formEditCompanyInfo'+
                                    '.formFields.requisites.title.errors.minLength')}}
                              </span>
                              <span v-if="!requisite.title.maxLength">
                                {{$t('contacts.formEditCompanyInfo'+
                                    '.formFields.requisites.title.errors.maxLength')}}
                              </span>
                              <span v-if="!requisite.title.alpha">
                                {{$t('contacts.formEditCompanyInfo'+
                                    '.formFields.requisites.title.errors.alpha')}}
                              </span>
                              <span v-if="!requisite.value.required">
                                {{$t('contacts.formEditCompanyInfo'+
                                    '.formFields.requisites.title.errors.required')}}
                              </span>
                              <span v-if="!requisite.value.minLength">
                                {{$t('contacts.formEditCompanyInfo'+
                                    '.formFields.requisites.title.errors.minLength')}}
                              </span>
                              <span v-if="!requisite.value.maxLength">
                                {{$t('contacts.formEditCompanyInfo'+
                                    '.formFields.requisites.title.errors.maxLength')}}
                              </span>
                              <span v-if="!requisite.value.alpha">
                                {{$t('contacts.formEditCompanyInfo'+
                                    '.formFields.requisites.title.errors.alpha')}}
                              </span>
                            </b-form-invalid-feedback>
                          </b-input-group>
                        </b-form-group>
                      </b-list-group-item>
                      <b-list-group-item class="p-0">
                        <b-button
                          block
                          v-if="can(user_perms, 'put', 'contacts')"
                          variant="success"
                          @click="organization.requisites.push({title: '', value: ''})"
                          v-bind:title="$t(
                            'contacts.formEditCompanyInfo.formFields.requisites.buttonAdd')"
                          v-b-tooltip.hover
                        >
                          <font-awesome-icon icon="plus" fixed-width />
                          <font-awesome-icon icon="money-check-alt" fixed-width />
                        </b-button>
                        <b-button
                          v-else
                          block
                          v-bind:title="$t(
                            'contacts.formEditCompanyInfo.formFields.requisites.buttonAdd')"
                          v-b-tooltip.hover
                        >
                          <font-awesome-icon :icon="['fa', 'lock']" fixed-width />
                        </b-button>
                      </b-list-group-item>
                    </b-list-group>
                  </b-collapse>
                </b-card>

                <b-button-group class="w-100">
                  <b-button
                    v-if="can(user_perms, 'put', 'contacts')"
                    type="submit"
                    variant="primary"
                    :disabled="!$v.organization.$anyDirty ||
                      $v.organization.$invalid || formPending"
                    v-bind:title="$t(
                      'contacts.formEditCompanyInfo.tooltips.submitCompanyNamesButton')"
                  >
                    <font-awesome-icon v-if="!formPending"
                      :icon="['fa', 'save']" fixed-width />
                    <b-spinner small v-if="formPending"></b-spinner>
                  </b-button>
                  <b-button
                    v-else
                    block
                    v-bind:title="$t(
                      'contacts.formEditCompanyInfo.tooltips.submitCompanyNamesButton')"
                    v-b-tooltip.hover
                  >
                    <font-awesome-icon :icon="['fa', 'lock']" fixed-width />
                  </b-button>
                </b-button-group>

              </b-form>
            </b-card-text>

          </b-card>
        </b-col>

      </b-row>

      <b-card
        no-body
        class="shaded"
      >
        <b-tabs fill card pills>
          <b-tab
            v-for="(building, bIndex) in $v.buildings.$each.$iter"
            :key="bIndex"
            title-link-class="h-100"
            class="m-3"
          >
            <b-form @submit.prevent="">
              <b-row>
                <b-col>
                  <b-form-group>
                    <b-form-input
                      id="input-1"
                      type="text"
                      v-model="building.name.$model"
                      v-bind:placeholder="$t(
                        'contacts.formEditBuildings.formFields.name.placeholder')"
                      :state="building.name.$dirty ?
                        !building.name.$error : null"
                    ></b-form-input>
                    <b-form-invalid-feedback>
                      <span v-if="!building.name.required">
                        {{$t('contacts.formEditBuildings.formFields.name.errors.required')}}
                      </span>
                      <span v-if="!building.name.maxLength">
                        {{$t('contacts.formEditBuildings.formFields.name.errors.maxLength')}}
                      </span>
                      <span v-if="!building.name.alpha">
                        {{$t('contacts.formEditBuildings.formFields.name.errors.alpha')}}
                      </span>
                    </b-form-invalid-feedback>
                  </b-form-group>
                </b-col>
                <b-col>
                  <b-form-group>
                    <b-form-input
                      id="input-1"
                      type="text"
                      v-model="building.road_map.$model"
                      v-bind:placeholder="$t(
                        'contacts.formEditBuildings.formFields.roadmap.placeholder')"
                      :state="building.road_map.$dirty ?
                        !building.road_map.$error : null"
                    ></b-form-input>
                    <b-form-invalid-feedback>
                      <span v-if="!building.road_map.required">
                        {{$t('contacts.formEditBuildings.formFields.roadmap.errors.required')}}
                      </span>
                      <span v-if="!building.road_map.maxLength">
                        {{$t('contacts.formEditBuildings.formFields.roadmap.errors.maxLength')}}
                      </span>
                      <span v-if="!building.road_map.alpha">
                        {{$t('contacts.formEditBuildings.formFields.roadmap.errors.alpha')}}
                      </span>
                    </b-form-invalid-feedback>
                  </b-form-group>
                </b-col>
              </b-row>
              <b-row>
                <b-col>
                  <b-card
                    no-body
                    class="mb-3"
                    v-for="(worktime, wIndex) in building.work_time.$each.$iter"
                    v-bind:key="wIndex"
                  >
                    <b-card-header header-tag="header" class="p-0" role="tab">
                      <b-button-group class="w-100">
                        <b-button
                          block
                          class="text-left"
                          v-b-toggle="'workTimeAccordion-' + wIndex"
                          variant="info"
                          v-bind:title="$t(
                            'contacts.formEditBuildings.formFields.worktime.title.placeholder')"
                          v-b-tooltip.hover
                        >
                          <font-awesome-icon icon="business-time" fixed-width />
                          {{worktime.title.$model}}
                        </b-button>
                        <b-button
                        v-if="can(user_perms, 'put', 'contacts')"
                          variant="danger"
                          v-bind:title="$t(
                            'contacts.formEditBuildings.formFields.worktime.deleteWorktimeButton')"
                          v-b-tooltip.hover
                          @click="buildings[bIndex].work_time.splice(wIndex, 1);
                            building.$touch()"
                        >
                          <font-awesome-icon icon="trash" fixed-width />
                        </b-button>
                        <b-button
                          v-else
                          v-bind:title="$t(
                            'contacts.formEditBuildings.formFields.worktime.deleteWorktimeButton')"
                          v-b-tooltip.hover
                        >
                          <font-awesome-icon :icon="['fa', 'lock']" fixed-width />
                        </b-button>
                      </b-button-group>
                    </b-card-header>
                    <b-collapse
                      :id="`workTimeAccordion-${wIndex}`"
                      accordion="worktime"
                      role="tabpanel"
                    >
                      <b-list-group flush>
                        <b-list-group-item>

                          <b-form-group class="m-0">
                            <b-form-input
                              :type="'text'"
                              v-model="worktime.title.$model"
                              v-bind:placeholder="$t(
                                'contacts.formEditBuildings.'
                                +'formFields.worktime.title.placeholder')"
                              :state="worktime.title.$dirty ?
                                !worktime.title.$error : null"
                            >
                            </b-form-input>

                            <b-form-invalid-feedback>
                              <span v-if="!worktime.title.required">
                                {{$t('contacts.formEditBuildings'+
                                    '.formFields.worktime.title.errors.required')}}
                              </span>
                              <span v-if="!worktime.title.maxLength">
                                {{$t('contacts.formEditBuildings'+
                                    '.formFields.worktime.title.errors.maxLength')}}
                              </span>
                              <span v-if="!worktime.title.alpha">
                                {{$t('contacts.formEditBuildings'+
                                    '.formFields.worktime.title.errors.alpha')}}
                              </span>
                              <span v-if="!worktime.regime.required">
                                {{$t('contacts.formEditBuildings'+
                                    '.formFields.worktime.errorPeriod')}}
                              </span>
                            </b-form-invalid-feedback>
                          </b-form-group>
                        </b-list-group-item>
                        <b-list-group-item
                          v-for="(iRegime, rIndex) in worktime.regime.$each.$iter"
                          v-bind:key="rIndex"
                        >
                          <b-form-group class="m-0">
                            <b-input-group>
                              <b-form-input
                                :type="'text'"
                                v-model="iRegime.title.$model"
                                v-bind:placeholder="$t(
                                  'contacts.formEditBuildings.'
                                  +'formFields.worktime.regime.placeholders.title')"
                                :state="iRegime.title.$dirty ?
                                  !iRegime.title.$error : null"
                              >
                              </b-form-input>
                              <vue-timepicker
                                format="HH:mm"
                                v-model="iRegime.from.$model"
                                input-class="h-100 w-100 borderless"
                                class="form-control p-0"
                                hide-clear-button
                                v-bind:placeholder="$t(
                                  'contacts.formEditBuildings.'
                                  +'formFields.worktime.regime.placeholders.from')"
                              >
                              </vue-timepicker>
                              <div class="input-group-text">&mdash;</div>
                              <vue-timepicker
                                format="HH:mm"
                                v-model="iRegime.to.$model"
                                input-class="h-100 w-100 borderless"
                                class="form-control p-0"
                                hide-clear-button
                                v-bind:placeholder="$t(
                                  'contacts.formEditBuildings.'
                                  +'formFields.worktime.regime.placeholders.to')"
                              >
                              </vue-timepicker>

                              <b-input-group-append>
                                <b-button
                                  variant="danger"
                                  v-if="can(user_perms, 'put', 'contacts')"
                                  v-bind:title="$t(
                                    'contacts.formEditBuildings.'
                                    +'formFields.worktime.regime.deleteRegimeButton')"
                                  v-b-tooltip.hover
                                 @click="buildings[bIndex].work_time[
                                  wIndex].regime.splice(rIndex, 1);
                                    worktime.$touch()"
                                >
                                  <font-awesome-icon icon="trash" fixed-width />
                                </b-button>
                                <b-button
                                  v-else
                                  block
                                  v-bind:title="$t(
                                    'contacts.formEditBuildings.'
                                    +'formFields.worktime.regime.deleteRegimeButton')"
                                  v-b-tooltip.hover
                                >
                                  <font-awesome-icon :icon="['fa', 'lock']" fixed-width />
                                </b-button>
                              </b-input-group-append>
                              <b-form-invalid-feedback>
                                 <span v-if="!iRegime.from.required">
                                  {{$t('contacts.formEditBuildings'+
                                      '.formFields.worktime.regime.errors.required')}}
                                </span>
                                <span v-if="!iRegime.from.maxLength">
                                  {{$t('contacts.formEditBuildings'+
                                      '.formFields.worktime.regime.errors.maxLength')}}
                                </span>
                                <span v-if="!iRegime.from.alpha">
                                  {{$t('contacts.formEditBuildings'+
                                      '.formFields.worktime.regime.errors.alphaTime')}}
                                </span>
                                <span v-if="!iRegime.to.required">
                                  {{$t('contacts.formEditBuildings'+
                                      '.formFields.worktime.regime.errors.required')}}
                                </span>
                                <span v-if="!iRegime.to.maxLength">
                                  {{$t('contacts.formEditBuildings'+
                                      '.formFields.worktime.regime.errors.maxLength')}}
                                </span>
                                <span v-if="!iRegime.to.alpha">
                                  {{$t('contacts.formEditBuildings'+
                                      '.formFields.worktime.regime.errors.alphaTime')}}
                                </span>
                                <span v-if="!iRegime.title.required">
                                  {{$t('contacts.formEditBuildings'+
                                      '.formFields.worktime.regime.errors.required')}}
                                </span>
                                <span v-if="!iRegime.title.maxLength">
                                  {{$t('contacts.formEditBuildings'+
                                      '.formFields.worktime.regime.errors.maxLength')}}
                                </span>
                                <span v-if="!iRegime.title.alpha">
                                  {{$t('contacts.formEditBuildings'+
                                      '.formFields.worktime.regime.errors.alpha')}}
                                </span>
                              </b-form-invalid-feedback>
                            </b-input-group>
                          </b-form-group>
                        </b-list-group-item>
                        <b-list-group-item class="p-0">
                          <b-button
                            v-if="can(user_perms, 'put', 'contacts')"
                            block
                            variant="success"
                            v-bind:title="$t('contacts.formEditBuildings.'
                              +'formFields.worktime.regime.addRegimeButton')"
                            v-b-tooltip.hover
                            @click="buildings[bIndex]
                              .work_time[wIndex]
                              .regime.push({title: '', from: '08:00', to: '17:00'})"
                          >
                            <font-awesome-icon icon="plus" fixed-width />
                            <font-awesome-icon icon="clock" fixed-width />
                          </b-button>
                          <b-button
                            v-else
                            block
                            class="mb-3"
                            v-bind:title="$t('contacts.formEditBuildings.'
                              +'formFields.worktime.regime.addRegimeButton')"
                            v-b-tooltip.hover
                          >
                            <font-awesome-icon :icon="['fa', 'lock']" fixed-width />
                          </b-button>
                        </b-list-group-item>
                      </b-list-group>
                    </b-collapse>
                  </b-card>

                  <b-button
                    block
                    variant="success"
                    class="mb-3"
                    v-if="can(user_perms, 'put', 'contacts')"
                    v-bind:title="$t(
                      'contacts.formEditBuildings.formFields.worktime.addWorktimeButton')"
                    v-b-tooltip.hover
                    @click="buildings[bIndex]
                      .work_time.push({title: '', regime: []})"
                  >
                    <font-awesome-icon icon="plus" fixed-width />
                    <font-awesome-icon icon="business-time" fixed-width />
                  </b-button>
                  <b-button
                    v-else
                    block
                    class="mb-3"
                    v-bind:title="$t(
                      'contacts.formEditBuildings.formFields.worktime.addWorktimeButton')"
                    v-b-tooltip.hover
                  >
                    <font-awesome-icon :icon="['fa', 'lock']" fixed-width />
                  </b-button>

                </b-col>
                <b-col>

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
                            <b-col :cols="contact.$model.cid ? 7 : 12">
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

                            <b-col cols="5" v-if="contact.$model.cid">
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
                  <b-button
                    block
                    variant="success"
                    class="mb-3"
                    v-bind:title="$t(
                      'contacts.formEditBuildings.formFields.employee.addEmployeeButton')"
                    v-b-tooltip.hover
                    v-if="can(user_perms, 'put', 'contacts')"
                    @click="buildings[bIndex]
                      .employee_contacts.push(
                        {
                          post: '',
                          name: '',
                          surname: '',
                          patronymic: '',
                          email: '',
                          phone: '',
                          photo: ''
                        })"
                  >
                    <font-awesome-icon icon="plus" fixed-width />
                    <font-awesome-icon icon="address-book" fixed-width />
                  </b-button>
                  <b-button
                    v-else
                    block
                    class="mb-3"
                    v-bind:title="$t(
                      'contacts.formEditBuildings.formFields.employee.addEmployeeButton')"
                    v-b-tooltip.hover
                  >
                    <font-awesome-icon :icon="['fa', 'lock']" fixed-width />
                  </b-button>
                </b-col>






                <b-col>

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
                  <b-button
                    block
                    variant="success"
                    class="mb-3"
                    v-bind:title="$t(
                      'contacts.formEditBuildings.formFields.employee.addEmployeeButton')"
                    v-b-tooltip.hover
                    v-if="can(user_perms, 'put', 'contacts')"
                    @click="buildings[bIndex]
                      .employee_contacts.push(
                        {
                          post: '',
                          name: '',
                          surname: '',
                          patronymic: '',
                          email: '',
                          phone: '',
                          photo: ''
                        })"
                  >
                    <font-awesome-icon icon="plus" fixed-width />
                    <font-awesome-icon icon="address-book" fixed-width />
                  </b-button>
                  <b-button
                    v-else
                    block
                    class="mb-3"
                    v-bind:title="$t(
                      'contacts.formEditBuildings.formFields.employee.addEmployeeButton')"
                    v-b-tooltip.hover
                  >
                    <font-awesome-icon :icon="['fa', 'lock']" fixed-width />
                  </b-button>
                </b-col>




              </b-row>

              <b-row>
                <b-col>
                  <b-button variant="primary"
                    v-bind:title="$t('contacts.formEditBuildings.tooltips.submitBuildingsButton')"
                    v-b-tooltip.hover
                    :disabled="!building.$anyDirty
                      || building.$invalid
                      || formPending
                      || building.work_time.$invalid
                      || building.employee_contacts.$invalid"
                    v-if="can(user_perms, 'put', 'contacts')"
                    @click="updateBuilding(building.$model)"
                  >
                    <font-awesome-icon v-if="!formPending"
                      :icon="['fa', 'save']" fixed-width />
                    <b-spinner small v-if="formPending"></b-spinner>
                  </b-button>
                  <b-button
                    v-else
                    v-bind:title="$t('contacts.formEditBuildings.tooltips.submitBuildingsButton')"
                    v-b-tooltip.hover
                  >
                    <font-awesome-icon :icon="['fa', 'lock']" fixed-width />
                  </b-button>

                  <b-button
                    variant="danger"
                    class="float-right"
                    v-if="can(user_perms, 'delete', 'contacts')"
                    v-bind:title="$t('contacts.formEditBuildings.tooltips.deleteBuildingsButton')"
                    v-b-tooltip.hover
                    v-b-modal.delete-modal
                    :disabled="formPending"
                    @click="selectBuilding(building.$model.id)"
                  >
                      <font-awesome-icon v-if="!formPending"
                        :icon="['fa', 'trash']" fixed-width />
                      <b-spinner small v-if="formPending"></b-spinner>
                  </b-button>
                  <b-button
                    v-else
                    class="float-right"
                    v-bind:title="$t('contacts.formEditBuildings.tooltips.deleteBuildingsButton')"
                    v-b-tooltip.hover
                  >
                    <font-awesome-icon :icon="['fa', 'lock']" fixed-width />
                  </b-button>
                </b-col>
              </b-row>
            </b-form>

            <template v-slot:title>
              <font-awesome-icon :icon="['fa', 'building']" fixed-width />
              {{building.name.$model}}
            </template>
          </b-tab>

          <!-- New Tab Button (Using tabs-end slot) -->
          <template v-slot:tabs-end>
            <b-nav-item
              href="#"
              class="bg-success border-success ml-3"
              v-bind:title="$t('contacts.formEditBuildings.tooltips.addBuildingsButton')"
              v-b-tooltip.hover
              v-b-modal.new-modal
              v-if="can(user_perms, 'post', 'contacts')"
            >
              <font-awesome-icon :icon="['fa', 'plus']" fixed-width class="text-white"/>
            </b-nav-item>
            <b-nav-item
              v-else
              href="#"
              class="bg-secondary border-secondary ml-3"
              v-bind:title="$t('contacts.formEditBuildings.tooltips.addBuildingsButton')"
              v-b-tooltip.hover
            >
              <font-awesome-icon :icon="['fa', 'lock']" fixed-width class="text-white"/>
            </b-nav-item>
          </template>

          <!-- Render this if no tabs -->
          <template v-slot:empty>
            <div class="text-center text-muted">
              <i18n path="contacts.formEditBuildings.noBuildings">
                <br slot="break">
                <font-awesome-icon
                  :icon="['fa', 'plus']"
                  fixed-width
                  slot="plus"
                />
              </i18n>
            </div>
          </template>
        </b-tabs>
      </b-card>
    </template>

    <b-modal id="delete-modal"
            @show="deletePassphrase=''"
            @hidden="deletePassphrase=''"
            @close="deletePassphrase=''"
             v-bind:title="$t('contacts.deleteModal.title')"
             v-b-tooltip.hover
             hide-footer size="sm" centered
            :header-bg-variant="'danger'"
            :header-text-variant="'light'"
            v-if="can(user_perms, 'delete', 'contacts')">

      <b-form class="w-100" @submit.prevent="deleteBuilding(selectedBuild.id)">

        <b-form-group
        :description="$t('contacts.deleteModal.confirmationField.description')">
          <b-input-group>

            <b-form-input
              name="confirmation-passphrase"
              autofocus
              v-model="$v.deletePassphrase.$model"
              v-bind:placeholder="$t('contacts.deleteModal.confirmationField.placeholder')"
              :state="$v.deletePassphrase.$dirty ? !$v.deletePassphrase.$error : null"
              @input="$v.deletePassphrase.$touch()">
            </b-form-input>
          </b-input-group>

        </b-form-group>
        <b-button type="submit" block
        variant="danger" v-bind:title="$t('contacts.deleteModal.tooltips.deleteButton')"
        v-b-tooltip.hover
        :disabled="!$v.deletePassphrase.$anyDirty || $v.deletePassphrase.$invalid">
          <font-awesome-icon :icon="['fa', 'trash']" fixed-width />
        </b-button>

      </b-form>
    </b-modal>

    <b-modal id="new-modal"
            v-bind:title="$t('contacts.formNewBuildings.formTitle')"
            hide-footer size="xl" centered
            :header-bg-variant="'success'"
            :header-text-variant="'light'"
            v-if="can(user_perms, 'post', 'contacts')">

      <b-form class="w-100" @submit.prevent="addNewBuilding">

        <b-form-group>
          <b-form-input name="name"
            type="text"
            autofocus
            v-bind:placeholder="$t('contacts.formNewBuildings.formFields.name.placeholder')"
            trim
            v-model="$v.newBuilding.name.$model"
            :state="$v.newBuilding.name.$dirty ? !$v.newBuilding.name.$error : null"
          ></b-form-input>

          <b-form-invalid-feedback
          :state="$v.newBuilding.name.$dirty ? !$v.newBuilding.name.$error : null">
            <span v-if="!$v.newBuilding.name.required">
              {{$t('contacts.formNewBuildings.formFields.name.errors.required')}}
            </span>
            <span v-if="!$v.newBuilding.name.maxLength">
              {{$t('contacts.formNewBuildings.formFields.name.errors.maxLength')}}
            </span>
            <span v-if="!$v.newBuilding.name.alpha">
              {{$t('contacts.formNewBuildings.formFields.name.errors.alpha')}}
            </span>
          </b-form-invalid-feedback>
        </b-form-group>

        <b-form-group>

          <b-form-textarea
            rows="3"
            max-rows="8"
            trim
            v-model="$v.newBuilding.road_map.$model"
            :state="$v.newBuilding.road_map.$dirty ? !$v.newBuilding.road_map.$error : null"
            v-bind:placeholder="$t('contacts.formNewBuildings.formFields.roadmap.placeholder')"
          ></b-form-textarea>

          <b-form-invalid-feedback
          :state="$v.newBuilding.road_map.$dirty ? !$v.newBuilding.road_map.$error : null">
            <span v-if="!$v.newBuilding.road_map.required">
              {{$t('contacts.formNewBuildings.formFields.roadmap.errors.required')}}
            </span>
            <span v-if="!$v.newBuilding.road_map.maxLength">
              {{$t('contacts.formNewBuildings.formFields.roadmap.errors.maxLength')}}
            </span>
            <span v-if="!$v.newBuilding.road_map.alpha">
              {{$t('contacts.formNewBuildings.formFields.roadmap.errors.alpha')}}
            </span>
          </b-form-invalid-feedback>
        </b-form-group>

        <b-row>
          <b-col>
            <b-button type="submit" variant="success" block
            v-bind:title="$t('contacts.formNewBuildings.tooltips.submitBuildingsButton')"
            v-b-tooltip.hover
            :disabled="!$v.newBuilding.$anyDirty || $v.newBuilding.$invalid || formPending">
              <font-awesome-icon v-if="!formPending"
              :icon="['fa', 'save']" fixed-width />
              <b-spinner small v-if="formPending"></b-spinner>
            </b-button>
          </b-col>
        </b-row>

      </b-form>

    </b-modal>

    <b-modal id="employee-photo-modal"
      v-bind:title="$t(
        'contacts.formEditBuildings.formFields.employee.photo.formTitle')"
      hide-footer size="md" centered
      :header-bg-variant="'primary'"
      :header-text-variant="'light'"
      v-if="can(user_perms, 'put', 'contacts')"
      @hidden="onResetImage"
      @close="onResetImage"
    >

      <div class=" row w-100 mx-auto pb-3 justify-content-center align-items-center">
        <img v-bind:src="imageUpdate.imageData ?
        imageUpdate.imageData : '/static/contact_photos/default.png'"
        class="profile-image-preview preview-md preview-square mr-4">

        <img v-bind:src="imageUpdate.imageData ?
        imageUpdate.imageData : '/static/contact_photos/default.png'"
        class="profile-image-preview preview-md mr-4">

        <img v-bind:src="imageUpdate.imageData ?
        imageUpdate.imageData : '/static/contact_photos/default.png'"
        class="profile-image-preview preview-sm mr-4">

      </div>

      <b-form class="w-100" @submit.prevent="onSubmitContactImage(selectedContact)">
        <b-form-group
        :description="$t(
          'contacts.formEditBuildings.formFields.employee.photo.formDescription')"
        >
          <b-form-file
            ref="imageInput"
            @input="onSelectImage"
            lang="ru"
            v-bind:placeholder="$t(
              'contacts.formEditBuildings.formFields.employee.photo.placeholder')"
            v-bind:browse-text="$t(
              'contacts.formEditBuildings.formFields.employee.photo.browseButton')"
            accept="image/jpeg, image/png, image/gif"
            :state="$v.imageUpdate.$dirty ? !$v.imageUpdate.$anyError : null"
          ></b-form-file>
          <b-form-invalid-feedback
          :state="$v.imageUpdate.$dirty ? !$v.imageUpdate.$anyError : null">
            <span v-if="!$v.imageUpdate.size.maxValue">
              {{$t('contacts.formEditBuildings.formFields.employee.photo.errors.maxValue')}}
            </span>
            <span v-if="!$v.imageUpdate.type.isImage">
              {{$t('contacts.formEditBuildings.formFields.employee.photo.errors.isImage')}}
            </span>
          </b-form-invalid-feedback>

        </b-form-group>

        <b-button
          class="mb-3"
          type="submit"
          block
          variant="primary"
          v-bind:title="$t(
            'contacts.formEditBuildings.formFields.employee.photo.saveButton')"
          v-b-tooltip.hover
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
import moment from 'moment';
import { mapState } from 'vuex';
import VueTelInput from 'vue-tel-input';
import VueTimepicker from 'vue2-timepicker';
import _ from 'lodash';
import {
  required, maxLength, minLength, sameAs, email, maxValue,
} from 'vuelidate/lib/validators';
import Breadcumbs from './Breadcumbs';
import { can, formatBytes } from '@/utils';
import { imageType } from '@/validators';


export default {
  name: 'Contacts',
  data() {
    return {
      selected: [],
      selectAll: false,
      preloadValue: 0,
      isActiveProgress: false,
      can,
      tabs: [],
      tabCounter: 0,
      deletePassphrase: '',
      selectedBuild: {},
      selectedContact: {},
      file: null,
      newBuilding: {
        name: '',
        road_map: '',
      },
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
      sameAsPassphrase: sameAs(function samePassphrase() {
        return this.$t('contacts.deleteModal.confirmationField.passphrase');
      }),
    },
    imageUpdate: {
      size: {
        maxValue: maxValue(1),
      },
      type: {
        isImage: imageType,
      },
    },
    organization: {
      company_name: {
        required,
        maxLength: maxLength(50),
        alpha: val => /^[а-яёa-zА-ЯЁA-Z0-9\s\W]*$/i.test(val),
      },
      full_company_name: {
        required,
        maxLength: maxLength(200),
        alpha: val => /^[а-яёa-zА-ЯЁA-Z0-9\s\W]*$/i.test(val),
      },
      requisites: {
        required,
        $each: {
          title: {
            required,
            maxLength: maxLength(50),
            minLength: minLength(1),
            alpha: val => /^[а-яёa-zА-ЯЁA-Z0-9\s\W]*$/i.test(val),
          },
          value: {
            required,
            maxLength: maxLength(200),
            minLength: minLength(1),
            alpha: val => /^[а-яёa-zА-ЯЁA-Z0-9\s\W]*$/i.test(val),
          },
        },
      },
    },
    buildings: {
      $each: {
        name: {
          required,
          maxLength: maxLength(50),
          alpha: val => /^[а-яёa-zА-ЯЁA-Z0-9\s\W]*$/i.test(val),
        },
        road_map: {
          required,
          maxLength: maxLength(500),
          alpha: val => /^[а-яёa-zА-ЯЁA-Z0-9\s\W]*$/i.test(val),
        },
        work_time: {
          required,
          $each: {
            title: {
              required,
              maxLength: maxLength(50),
              alpha: val => /^[а-яёa-zА-ЯЁA-Z0-9\s\W]*$/i.test(val),
            },
            regime: {
              required,
              $each: {
                title: {
                  required,
                  maxLength: maxLength(50),
                  alpha: val => /^[а-яёa-zА-ЯЁA-Z0-9\s\W]*$/i.test(val),
                },
                from: {
                  required,
                  maxLength: maxLength(5),
                  alpha: val => /^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$/i.test(val),
                },
                to: {
                  required,
                  maxLength: maxLength(5),
                  alpha: val => /^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$/i.test(val),
                },
              },
            },
          },
        },
        employee_contacts: {
          required,
          $each: {
            post: {
              required,
              maxLength: maxLength(100),
              alpha: val => /^[а-яёa-zА-ЯЁA-Z0-9\s\W]*$/i.test(val),
            },
            patronymic: {
              required,
              maxLength: maxLength(50),
              alpha: val => /^[а-яёa-zА-ЯЁA-Z0-9\s\W]*$/i.test(val),
            },
            surname: {
              required,
              maxLength: maxLength(50),
              alpha: val => /^[а-яёa-zА-ЯЁA-Z0-9\s\W]*$/i.test(val),
            },
            name: {
              required,
              maxLength: maxLength(50),
              alpha: val => /^[а-яёa-zА-ЯЁA-Z0-9\s\W]*$/i.test(val),
            },
            email: {
              required,
              email,
            },
            phone: {
              required,
              minLength: minLength(16),
            },
            photo: {
              maxLength: maxLength(100),
              alpha: val => /^[а-яёa-zА-ЯЁA-Z0-9\s\W]*$/i.test(val),
            },
          },
        },
      },
    },
    newBuilding: {
      name: {
        required,
        maxLength: maxLength(50),
        alpha: val => /^[а-яёa-zА-ЯЁA-Z0-9\s\W]*$/i.test(val),
      },
      road_map: {
        required,
        maxLength: maxLength(500),
        alpha: val => /^[а-яёa-zА-ЯЁA-Z0-9\s\W]*$/i.test(val),
      },
    },
  },
  components: {
    Breadcumbs, VueTelInput, VueTimepicker,
  },
  computed: mapState({
    organization: state => state.organization,
    buildings: state => state.buildings,
    user_perms: state => state.user_perms,
    uid: state => state.uid,
    progressValue: state => state.uploadProgress,
    progressMax: state => state.uploadProgressMax,
    formPending: state => state.formPending,
  }),
  watch: {
    user_perms() {
      if (can(this.user_perms, 'get', 'contacts')) {
        this.$store.dispatch('loadOrganization');
        this.$store.dispatch('loadCompanyBuildings');
      }
    },
  },
  methods: {
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
    onSubmitContactImage(ids) {
      this.$v.imageUpdate.$touch();

      if (!this.$v.imageUpdate.$invalid) {
        const formData = new FormData();
        if (this.file) {
          formData.append('employee_photo', this.file[0]);
        }
        this.isActiveProgress = true;
        this.$store.dispatch('updateEmployeePhoto', { formData, ids });
      }
    },
    onResetImage() {
      this.selectedContact = {};
      this.file = null;
      this.imageUpdate.type = '';
      this.imageUpdate.size = 0;
      this.imageUpdate.imageData = '';
      this.isActiveProgress = false;
      this.$v.imageUpdate.$reset();
      // Trick to reset/clear native browser form validation state
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    },
    deleteEmployeePhoto(ids) {
      this.$store.dispatch('deleteEmployeePhoto', ids);
    },
    dateFormatter(date) {
      return moment(date).format('YYYY-MM-DD');
    },
    deleteBuilding(id) {
      if (can(this.user_perms, 'delete', 'contacts')) {
        this.$store.dispatch('deleteBuilding', { id });
      }
    },
    updateBuilding(updateInfo) {
      if (can(this.user_perms, 'put', 'contacts')) {
        this.$store.dispatch('updateBuilding', updateInfo);
      }
    },
    addNewBuilding() {
      if (can(this.user_perms, 'post', 'contacts')) {
        this.$v.newBuilding.$touch();

        if (!this.$v.newBuilding.$invalid) {
          this.$store.dispatch('newBuilding', this.newBuilding);
        }
      }
    },
    updateCompany() {
      this.$v.$touch();

      if (!this.$v.organization.$invalid) {
        this.$store.dispatch('updateCompanyNames', this.organization);
      }
    },
    selectBuilding(id) {
      this.selectedBuild = _.find(this.buildings, { id });
    },
  },
};
</script>
