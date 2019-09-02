<template>
    <main class="container-fluid">
        <breadcumbs></breadcumbs>

        <b-row class="pb-3">

          <b-col cols="3">
            <b-card no-body class="overflow-hidden shaded"
            style="max-width: 540px;">
              <b-row no-gutters>
                <b-col sm="6" class="text-primary my-auto
                justify-content-center align-middle align-items-center text-center">
                  <font-awesome-icon :icon="['fa', 'user']" fixed-width size="3x"/>
                </b-col>
                <b-col sm="6" class="bg-primary text-white
                justify-content-center align-middle align-items-center text-center">
                  <b-card-body>
                    <b-card-text>
                      <h2 class="">15</h2>
                      <span class="notation">
                        {{$t('dashboard.counters.cmsUsers')}}
                      </span>
                    </b-card-text>
                  </b-card-body>
                </b-col>
              </b-row>
            </b-card>
          </b-col>
          <b-col cols="3">
            <b-card no-body class="overflow-hidden shaded"
            style="max-width: 540px;">
              <b-row no-gutters>
                <b-col sm="6" class="text-info my-auto
                justify-content-center align-middle align-items-center text-center">
                  <font-awesome-icon :icon="['fa', 'users']" fixed-width size="2x"/>
                </b-col>
                <b-col sm="6" class="bg-info text-white
                justify-content-center align-middle align-items-center text-center">
                  <b-card-body>
                    <b-card-text>
                      <h2 class="">150</h2>
                      <span class="notation">
                        {{$t('dashboard.counters.siteUsers')}}
                      </span>
                    </b-card-text>
                  </b-card-body>
                </b-col>
              </b-row>
            </b-card>
          </b-col>
          <b-col cols="3">
            <b-card no-body class="overflow-hidden shaded"
            style="max-width: 540px;">
              <b-row no-gutters>
                <b-col sm="6" class="text-success my-auto
                justify-content-center align-middle align-items-center text-center">
                  <font-awesome-icon :icon="['fa', 'newspaper']" fixed-width size="2x"/>
                </b-col>
                <b-col sm="6" class="bg-success text-white
                justify-content-center align-middle align-items-center text-center">
                  <b-card-body>
                    <b-card-text>
                      <h2 class="">350</h2>
                      <span class="notation">
                        {{$t('dashboard.counters.news')}}
                      </span>
                    </b-card-text>
                  </b-card-body>
                </b-col>
              </b-row>
            </b-card>
          </b-col>
          <b-col cols="3">
            <b-card no-body class="overflow-hidden shaded"
            style="max-width: 540px;">
              <b-row no-gutters>
                <b-col sm="6" class="text-warning my-auto
                justify-content-center align-middle align-items-center text-center">
                  <font-awesome-icon :icon="['fa', 'list']" fixed-width size="2x"/>
                </b-col>
                <b-col sm="6" class="bg-warning text-white
                justify-content-center align-middle align-items-center text-center">
                  <b-card-body>
                    <b-card-text>
                      <h2 class="">5</h2>
                      <span class="notation">
                        {{$t('dashboard.counters.sections')}}
                      </span>
                    </b-card-text>
                  </b-card-body>
                </b-col>
              </b-row>
            </b-card>
          </b-col>

        </b-row>

        <b-row class="pb-3">
          <b-col cols="12">
            <b-list-group horizontal class="shaded" v-if="Object.keys(projectLangs).length > 0">
              <b-list-group-item class="text-center flex-fill"
              :key="name" v-for="(value, name) in projectLangs">
                <b-row class="mx-auto justify-content-center align-items-center
                text-center vertical-align">
                  <h3 class="m-0 pr-2 weight-100 small">
                    <font-awesome-icon :icon="['fa', 'circle']"
                    :class="'color-' + name" fixed-width/> {{name}}
                  </h3>
                  <span style="line-height: 1.2;">{{value}}%</span>
                </b-row>
              </b-list-group-item>
            </b-list-group>
            <b-list-group horizontal class="shaded" v-else>
              <b-list-group-item class="text-center flex-fill">
                <b-row class="mx-auto justify-content-center align-items-center
                text-center vertical-align">
                  <h3 class="m-0 pr-2 small text-danger">
                    Данные о проекте не могут быть получены!
                  </h3>
                </b-row>
              </b-list-group-item>
            </b-list-group>
          </b-col>
        </b-row>

<!--
        <b-row>
          <b-col cols="8">
            <b-card
              border-variant="secondary"
              header="Траффик сайта"
              header-border-variant="secondary"
              align="center"
            >
              <b-card-text>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</b-card-text>
            </b-card>
          </b-col>
          <b-col cols="4">
            <b-card
              border-variant="secondary"
              header="Места просмотра"
              header-border-variant="secondary"
              align="center"
            >
              <b-card-text>Lorem ipsum dolor sit amet</b-card-text>
            </b-card>
          </b-col>
        </b-row>
-->

    </main>
</template>

<script>
import axios from 'axios';
import Breadcumbs from './Breadcumbs';

export default {
  name: 'Dashboard',
  data() {
    return {
      projectLangs: {},
    };
  },
  components: { Breadcumbs },
  mounted() {
    return axios.get('https://api.github.com/repos/Goomba41/site.cgako/languages')
      .then((response) => {
        let sum = 0;
        const langs = response.data;
        Object.entries(response.data).forEach((value) => {
          sum += value[1];
        });
        Object.entries(langs).forEach(([key, value]) => {
          langs[key] = parseFloat(((value / sum) * 100)).toFixed(2);
        });
        this.projectLangs = langs;
      })
      .catch((error) => {
        // eslint-disable-next-line
        console.error(error);
      });
  },
};
</script>
