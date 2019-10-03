<template>
  <main class="container-fluid d-flex flex-column">
    <breadcumbs></breadcumbs>

    <b-row class="pb-4 m-0 w-100 flex-grow-1 blocker"
    v-if="!can(user_perms, 'get', 'structure')">
      <b-col class="align-self-center text-center">
        <font-awesome-icon :icon="['fa', 'lock']" fixed-width size="10x"/>
      </b-col>
    </b-row>

    <b-row class="p-3 justify-content-center" v-if="can(user_perms, 'get', 'structure')">
      <b-col sm="12">

        <b-card no-body class="text-center">

          <vue-tree-list class="p-3"
            :model="data"
            @delete-node="onDel"
            @add-node="onAddNode"
            @drop="onDrop"
            @edit="onEdit"
            :default-tree-node-name="$t('structure.tooltips.defaultTreeNodeName')"
            :default-leaf-node-name="$t('structure.tooltips.defaultLeafNodeName')"
            v-bind:default-expanded="true">
            <span class="icon" slot="addTreeNode"
              v-bind:title="$t('structure.tooltips.addSection')"
              v-b-tooltip.hover
            >
              <b-button class="mr-1" size="sm" variant="success"
                v-if="can(user_perms, 'post', 'structure')"
              >
                <font-awesome-icon :icon="['fa', 'plus']" fixed-width />
              </b-button>
              <b-button class="mr-1" size="sm" v-else>
                <font-awesome-icon :icon="['fa', 'lock']" fixed-width />
              </b-button>

            </span>
            <span class="icon" slot="editNode"
              v-bind:title="$t('structure.tooltips.editSection')"
              v-b-tooltip.hover
            >
              <b-button class="mr-1" size="sm" variant="primary"
                v-if="can(user_perms, 'put', 'structure')"
              >
                <font-awesome-icon :icon="['fa', 'pencil-alt']" fixed-width />
              </b-button>
              <b-button class="mr-1" size="sm" v-else>
                <font-awesome-icon :icon="['fa', 'lock']" fixed-width />
              </b-button>
            </span>
            <span class="icon" slot="addLeafNode"></span>
            <span class="icon" slot="delNode"
              v-bind:title="$t('structure.tooltips.deleteSection')"
              v-b-tooltip.hover
            >
              <b-button class="mr-1" size="sm" variant="danger"
                v-if="can(user_perms, 'delete', 'structure')"
              >
                <font-awesome-icon :icon="['fa', 'trash']" fixed-width />
              </b-button>
              <b-button class="mr-1" size="sm" v-else>
                <font-awesome-icon :icon="['fa', 'lock']" fixed-width />
              </b-button>
            </span>
          </vue-tree-list>

        </b-card>

      </b-col>
    </b-row>

    <b-modal id="delete-modal"
      @show="deletePassphrase=''"
      @hidden="deletePassphrase=''"
      @close="deletePassphrase=''"
       v-bind:title="$t('structure.deleteModal.title')"
       v-b-tooltip.hover
       hide-footer size="sm" centered
      :header-bg-variant="'danger'"
      :header-text-variant="'light'"
      v-if="can(user_perms, 'delete', 'structure')"
    >

      <b-form class="w-100" @submit.prevent="deleteSection(section.id)">

        <b-form-group
        :description="$t('structure.deleteModal.confirmationField.description')"
        >
          <b-input-group>

            <b-form-input
              name="confirmation-passphrase"
              autofocus
              v-model="$v.deletePassphrase.$model"
              v-bind:placeholder="$t('structure.deleteModal.confirmationField.placeholder')"
              :state="$v.deletePassphrase.$dirty ? !$v.deletePassphrase.$error : null"
              @input="$v.deletePassphrase.$touch()"
              >
            </b-form-input>
          </b-input-group>

        </b-form-group>
        <b-button type="submit" block
        variant="danger" v-bind:title="$t('structure.deleteModal.tooltips.deleteButton')"
        v-b-tooltip.hover
        :disabled="!$v.deletePassphrase.$anyDirty || $v.deletePassphrase.$invalid"
        >
          <font-awesome-icon :icon="['fa', 'trash']" fixed-width />
        </b-button>

        <div class="row mx-auto pl-3 pr-3 pt-3 border-top">
          <span class="text-danger notation text-center">
              <font-awesome-icon :icon="['fa', 'exclamation-triangle']"
              size="1x" fixed-width />
              {{$t('structure.deleteModal.description')}}
          </span>
        </div>

      </b-form>
    </b-modal>

    <b-modal id="new-modal"
      v-bind:title="$t('structure.formNew.formTitle')"
      hide-footer size="xl" centered
      :header-bg-variant="'success'"
      :header-text-variant="'light'"
      @hidden="onReset"
      v-if="can(user_perms, 'post', 'structure')"
    >

      <b-form class="w-100" @submit.prevent="newSectionSubmit" @reset="onReset">

        <b-form-group>
          <b-form-input name="name"
            type="text"
            autofocus
            v-bind:placeholder="$t('structure.formNew.formFields.name.placeholder')"
            trim
            v-model="$v.newSection.name.$model"
            :state="$v.newSection.name.$dirty ? !$v.newSection.name.$error : null"
          ></b-form-input>

          <b-form-invalid-feedback
          >
            <span v-if="!$v.newSection.name.required">
              {{$t('structure.formNew.formFields.name.errors.required')}}
            </span>
            <span v-if="!$v.newSection.name.minLength">
              {{$t('structure.formNew.formFields.name.errors.minLength')}}
            </span>
            <span v-if="!$v.newSection.name.maxLength">
              {{$t('structure.formNew.formFields.name.errors.maxLength')}}
            </span>
            <span v-if="!$v.newSection.name.alpha">
              {{$t('structure.formNew.formFields.name.errors.alpha')}}
            </span>
          </b-form-invalid-feedback>

        </b-form-group>

        <b-form-group>
          <b-form-checkbox
          v-model="$v.newSection.enabled.$model"
          name="available"
          switch size="md"
        >
            {{$t('structure.formNew.formFields.enabled.placeholder')}}
          </b-form-checkbox>
        </b-form-group>

        <b-row>
          <b-col>
            <b-button type="submit" variant="success" block
            v-bind:title="$t('structure.formNew.tooltips.submitButton')" v-b-tooltip.hover
            :disabled="!$v.newSection.$anyDirty || $v.newSection.$invalid"
            >
              <font-awesome-icon v-if="!formPending"
              :icon="['fa', 'save']" fixed-width />
              <b-spinner small v-if="formPending"></b-spinner>
            </b-button>
          </b-col>
        </b-row>

      </b-form>

    </b-modal>

    <b-modal id="edit-modal"
      v-bind:title="$t('structure.formEdit.formTitle')"
      hide-footer size="xl" centered
      :header-bg-variant="'primary'"
      :header-text-variant="'light'"
      @hidden="onResetEdit"
      v-if="can(user_perms, 'put', 'structure')"
    >

      <b-form class="w-100" @submit.prevent="updateSectionSubmit">

        <b-form-group>
          <b-form-input name="name"
            type="text"
            autofocus
            v-bind:placeholder="$t('structure.formEdit.formFields.name.placeholder')"
            trim
            v-model="$v.section.name.$model"
            :state="$v.section.name.$dirty ? !$v.section.name.$error : null"
          ></b-form-input>

          <b-form-invalid-feedback>
            <span v-if="!$v.section.name.required">
              {{$t('structure.formEdit.formFields.name.errors.required')}}
            </span>
            <span v-if="!$v.section.name.minLength">
              {{$t('structure.formEdit.formFields.name.errors.minLength')}}
            </span>
            <span v-if="!$v.section.name.maxLength">
              {{$t('structure.formEdit.formFields.name.errors.maxLength')}}
            </span>
            <span v-if="!$v.section.name.alpha">
              {{$t('structure.formEdit.formFields.name.errors.alpha')}}
            </span>
          </b-form-invalid-feedback>

        </b-form-group>

        <b-form-group>
          <b-form-checkbox
          v-model="$v.section.enabled.$model"
          name="available"
          switch size="md"
        >
            {{$t('structure.formEdit.formFields.enabled.placeholder')}}
          </b-form-checkbox>
        </b-form-group>

        <b-row>
          <b-col>
            <b-button type="submit" variant="primary" block
            v-bind:title="$t('structure.formEdit.tooltips.submitButton')" v-b-tooltip.hover
            :disabled="!$v.section.$anyDirty || $v.section.$invalid"
            >
              <font-awesome-icon v-if="!formPending"
              :icon="['fa', 'save']" fixed-width />
              <b-spinner small v-if="formPending"></b-spinner>
            </b-button>
          </b-col>
        </b-row>

      </b-form>

    </b-modal>

  </main>
</template>

<script>
import { mapState } from 'vuex';
import { VueTreeList, Tree } from 'vue-tree-list';
import {
  required, sameAs, minLength, maxLength,
} from 'vuelidate/lib/validators';
import Breadcumbs from './Breadcumbs';
import { EventBus, can } from '@/utils';

export default {
  name: 'Structure',
  data() {
    return {
      can,
      section: {},
      newSection: {},
      data: {},
      deletePassphrase: '',
      availableDefault: true,
    };
  },
  validations: {
    deletePassphrase: {
      required,
      sameAsName: sameAs(function sameName() {
        return this.section.name;
      }),
    },
    newSection: {
      name: {
        required,
        minLength: minLength(4),
        maxLength: maxLength(50),
        alpha: val => /^[а-яёa-zА-ЯЁA-Z0-9\s\W]*$/i.test(val),
      },
      enabled: {
        required,
      },
    },
    section: {
      name: {
        required,
        minLength: minLength(4),
        maxLength: maxLength(50),
        alpha: val => /^[а-яёa-zА-ЯЁA-Z0-9\s\W]*$/i.test(val),
      },
      enabled: {
        required,
      },
    },
  },
  components: { Breadcumbs, VueTreeList },
  computed: mapState({
    user_perms: state => state.user_perms,
    structure: state => state.structure,
    uid: state => state.uid,
    formPending: state => state.formPending,
  }),
  watch: {
    user_perms() {
      if (can(this.user_perms, 'get', 'structure')) {
        this.$store.dispatch('loadStructure');
      }
    },
    structure(structure) {
      this.data = new Tree([structure]);
    },
  },
  methods: {
    onClick(params) {
      this.section = params;
    },
    onEdit(params) {
      this.section = params;
      this.$bvModal.show('edit-modal');
    },
    onDel(node) {
      this.section = node;
      this.$bvModal.show('delete-modal');
    },
    deleteSection(id) {
      this.$store.dispatch('deleteSection', { id });
    },
    onAddNode(params) {
      /* eslint no-param-reassign:
      ["error", { "props": true, "ignorePropertyModificationsFor": ["params"] }] */
      params.enabled = this.availableDefault;
      this.newSection = params;
      this.$bvModal.show('new-modal');
    },
    onReset(evt) {
      evt.preventDefault();
      this.newSection.remove();
      this.newSection = {};
      this.$v.newSection.$reset();

      // Trick to reset/clear native browser form validation state
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
      EventBus.$emit('forceRerender');
    },
    onResetEdit(evt) {
      evt.preventDefault();
      this.section = {};
      this.$v.section.$reset();

      // Trick to reset/clear native browser form validation state
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
      EventBus.$emit('forceRerender');
    },
    newSectionSubmit() {
      this.$v.$touch();

      if (!this.$v.newSection.$invalid) {
        delete this.newSection.parent;
        this.$store.dispatch('newSection', this.newSection);
      }
    },
    updateSectionSubmit() {
      this.$v.$touch();

      if (!this.$v.section.$invalid) {
        delete this.section.parent;
        this.$store.dispatch('updateSection', this.section);
      }
    },
    onDrop(params) {
      this.$store.dispatch('updateSectionParent', { sid: params.node.id, pid: params.target.id });
    },
  },
};
</script>
