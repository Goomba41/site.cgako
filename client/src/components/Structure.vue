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

        <b-card no-body class="text-center" v-if="structure && structure.length">

          <vue-tree-list class="p-3"
            :model="data"
            @click="onClick"
            @delete-node="onDel"
            :default-tree-node-name="$t('structure.tooltips.defaultTreeNodeName')"
            :default-leaf-node-name="$t('structure.tooltips.defaultLeafNodeName')"
            v-bind:default-expanded="true">
            <span class="icon" slot="addTreeNode"
              v-bind:title="$t('structure.tooltips.addSection')"
              v-b-tooltip.hover
            >
              <b-button class="mr-1" size="sm" variant="success">
                <font-awesome-icon :icon="['fa', 'plus']" fixed-width />
              </b-button>
            </span>
            <span class="icon" slot="editNode"
              v-bind:title="$t('structure.tooltips.editSection')"
              v-b-tooltip.hover
            >
              <b-button class="mr-1" size="sm" variant="primary">
                <font-awesome-icon :icon="['fa', 'pencil-alt']" fixed-width />
              </b-button>
            </span>
            <span class="icon" slot="addLeafNode"></span>
            <span class="icon" slot="delNode"
              v-bind:title="$t('structure.tooltips.deleteSection')"
              v-b-tooltip.hover
            >
              <b-button class="mr-1" size="sm" variant="danger">
                <font-awesome-icon :icon="['fa', 'trash']" fixed-width />
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
            v-if="can(user_perms, 'delete', 'structure')">

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

  </main>
</template>

<script>
import { mapState } from 'vuex';
import { VueTreeList, Tree, TreeNode } from 'vue-tree-list';
import {
  required, sameAs,
} from 'vuelidate/lib/validators';
import Breadcumbs from './Breadcumbs';
import { can } from '@/utils';
// TreeNode

export default {
  name: 'Structure',
  data() {
    return {
      can,
      section: {},
      data: {},
      deletePassphrase: '',
    };
  },
  validations: {
    deletePassphrase: {
      required,
      sameAsName: sameAs(function sameName() {
        return this.section.name;
      }),
    },
  },
  components: { Breadcumbs, VueTreeList },
  computed: mapState({
    user_perms: state => state.user_perms,
    structure: state => state.structure,
    uid: state => state.uid,
  }),
  watch: {
    user_perms() {
      if (can(this.user_perms, 'get', 'structure')) {
        this.$store.dispatch('loadStructure');
      }
    },
    structure(structure) {
      this.data = new Tree(structure);
    },
  },
  methods: {
    onClick(params) {
      this.section = params;
    },
    onDel(node) {
      this.section = node;
      this.$bvModal.show('delete-modal');
    },
    deleteSection(id) {
      this.$store.dispatch('deleteSection', { id });
      // this.section.remove();
    },
  },
};
</script>
