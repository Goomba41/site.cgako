<template>
  <aside class="sidebar">

    <b-list-group class="pt-3 pb-3">
      <b-list-group-item class="heading noselect">
        <h3 class="m-0 weight-100 small">{{$t('menu.titles.navigation')}}</h3>
      </b-list-group-item>

      <router-link :to="{ name: 'Dashboard' }">
        <b-list-group-item class="noselect" @click="sidebarOff">
          <font-awesome-icon :icon="['fa', 'th-large']" class="pr-3" fixed-width size="2x"/>
          {{$t('menu.menuItems.dashboard')}}
        </b-list-group-item>
      </router-link>

      <b-list-group-item v-b-toggle.collapse-site class="noselect">
        <font-awesome-icon :icon="['fa', 'globe-europe']" class="pr-3" fixed-width size="2x"/>
        {{$t('menu.menuItems.site')}}
        <font-awesome-icon :icon="['fa', 'chevron-down']" class="ml-auto" fixed-width size="1x"/>
      </b-list-group-item>

      <b-collapse id="collapse-site" class="noselect">
        <b-list-group class="">
            <router-link :to="{ name: 'Users' }">
              <b-list-group-item class="noselect" @click="sidebarOff">
                <span class="ml-4">
                  <font-awesome-icon :icon="['fa', 'user']" class="" fixed-width size="1x"/>
                  {{$t('menu.menuItems.users')}}
                </span>
              </b-list-group-item>
            </router-link>
            <router-link :to="{ name: 'Roles' }">
              <b-list-group-item class="noselect" @click="sidebarOff">
                <span class="ml-4">
                  <font-awesome-icon :icon="['fa', 'id-card']" class="" fixed-width size="1x"/>
                  {{$t('menu.menuItems.permissions')}}
                </span>
              </b-list-group-item>
            </router-link>
            <b-list-group-item class="noselect" disabled @click="sidebarOff">
              <span class="ml-4">
                <font-awesome-icon :icon="['fa', 'newspaper']" class="" fixed-width size="1x"/>
                {{$t('menu.menuItems.news')}}
              </span>
            </b-list-group-item>
        </b-list-group>
      </b-collapse>

      <b-list-group-item class="noselect" disabled @click="sidebarOff">
        <font-awesome-icon :icon="['fa', 'folder']" class="pr-3" fixed-width size="2x"/>
        {{$t('menu.menuItems.materials')}}
      </b-list-group-item>

    </b-list-group>

    <b-list-group class="pt-3 pb-3">
      <b-list-group-item class="heading noselect">
        <h3 class="m-0 weight-100 small">{{$t('menu.titles.settings')}}</h3>
      </b-list-group-item>

      <b-list-group-item class="noselect">
        <font-awesome-icon :icon="['fa', 'language']" class="pr-3" fixed-width size="2x"/>
        <multiselect v-model="value" :options="options"
        :show-labels="false" :searchable="false" :close-on-select="true"
        :hideSelected="true" :allowEmpty="false">
          <template slot="singleLabel" slot-scope="props">
            <flag :iso="props.option.class" :squared="false"></flag>
            <span class="pl-1">
              {{ $t('footer.tooltips.languages.' + props.option.translation) }}
            </span>
          </template>
          <template slot="option" slot-scope="props">
            <flag :iso="props.option.class" :squared="false"></flag>
            <span class="pl-1">
              {{ $t('footer.tooltips.languages.' + props.option.translation) }}
            </span>
          </template>
        </multiselect>
      </b-list-group-item>

    </b-list-group>

  </aside>

</template>

<script>
import { EventBus } from '@/utils';
import Multiselect from 'vue-multiselect';

export default {
  name: 'Sidebar',
  data() {
    return {
      value: { locale: 'ru', class: 'ru', translation: 'rus' },
      options: [
        { locale: 'ru', class: 'ru', translation: 'rus' },
        { locale: 'su', class: 'su', translation: 'sul' },
        { locale: 'en', class: 'us', translation: 'eng' },
      ],
    };
  },
  components: { Multiselect },
  methods: {
    sidebarOff() {
      EventBus.$emit('sidebarOff');
    },
  },
};
</script>
