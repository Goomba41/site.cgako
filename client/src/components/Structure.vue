<template>
  <main class="container-fluid d-flex flex-column">
    <breadcumbs></breadcumbs>

    <b-row class="pb-4 m-0 w-100 flex-grow-1 blocker"
    v-if="!can(user_perms, 'get', 'structure')">
      <b-col class="align-self-center text-center">
        <font-awesome-icon :icon="['fa', 'lock']" fixed-width size="10x"/>
      </b-col>
    </b-row>

    <b-row class="pb-4 m-0 w-100" v-if="can(user_perms, 'get', 'structure')">
      <b-col align-self="start" class="text-center" sm="8">
        <b-row class="justify-content-start align-middle align-items-center">
          <span class="text-info pr-3">
<!--
            {{ $tc('rolesPermissions.counter', roles.count) }}
-->
          </span>

          <b-button v-bind:title="$t('rolesPermissions.tooltips.newRoleButton')"
          v-if="can(user_perms, 'post', 'structure')"
          v-b-tooltip.hover class="mr-1" size="sm" variant="success"
          v-b-modal.new-modal>
            <font-awesome-icon icon="plus" fixed-width />
          </b-button>
          <b-button v-else class="mr-1"
          size="sm" v-bind:title="$t('rolesPermissions.tooltips.newRoleButton')"
          v-b-tooltip.hover>
            <font-awesome-icon :icon="['fa', 'lock']" fixed-width />
          </b-button>

          <b-dropdown size="sm" class="mr-1">
<!--
          v-bind:disabled="!selected.length"
          v-bind:class="!selected.length"
-->
            <template slot="button-content">
              <font-awesome-icon icon="list" fixed-width />
            </template>
            <b-dropdown-item variant="danger" v-b-modal.delete-group-modal
            v-if="can(user_perms, 'delete', 'structure')">
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

    </b-row>

    <b-row class="p-3 justify-content-center" v-if="can(user_perms, 'get', 'structure')">
      <b-col sm="6">

<!--
        {{structure}}
-->

        <Tree :label="structure.name" :nodes="structure" :depth="0"></Tree>

      </b-col>
    </b-row>

  </main>
</template>

<script>
import { mapState } from 'vuex';
import Breadcumbs from './Breadcumbs';
import Tree from './Tree';
import { can } from '@/utils';


export default {
  name: 'Structure',
  data() {
    return {
      can,
    };
  },
  components: { Breadcumbs, Tree },
  computed: mapState({
    user_perms: state => state.user_perms,
    structure: state => state.structure,
    uid: state => state.uid,
  }),
  beforeMount() {
    if (can(this.user_perms, 'get', 'structure')) {
      this.$store.dispatch('loadStructure');
    }
  },
  methods: {
  },
};
</script>
