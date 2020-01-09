<template>
  <!-- Main -->
  <div id="main">
    <!-- Post -->
    <section class="post" v-if="this.$route.path==='/contacts'">
      <header>
        <h2>{{contactsData.full_company_name}} ({{contactsData.company_name}})</h2>
      </header>

      <section class="contacts">
        <h2>Адреса и телефоны архива</h2>

        <b-tabs content-class="mt-0 box">
          <b-tab
            v-for="(building, bIndex) in contactsData.buildings"
            v-bind:key="building.id"
            :title="building.name"
            :active="bIndex === 0"
          >
            <b-row>
              <b-col>
                <iframe :src="building.road_map" width="100%" height="500" frameborder="0">
                </iframe>
              </b-col>
              <b-col v-if="building.additional_info && building.additional_info.length > 0">
                <ul>
                  <li v-for="(info, iIndex) in building.additional_info" v-bind:key="iIndex">
                    <b>{{info.title}}: </b>{{info.value}}
                  </li>
                </ul>
              </b-col>
            </b-row>

            <div class="table-wrapper pt-3">
              <h3>Режимы работы:</h3>
              <table class="contacts">
                <tbody>
                  <tr>
                    <td
                      v-for="(work, wIndex) in building.work_time"
                      v-bind:key="wIndex"
                    >
                      <h4>{{work.title}}</h4>
                      <ul>
                        <li
                          v-for="(interval, iIndex) in work.regime"
                          v-bind:key="iIndex"
                        >
                          <b>{{interval.title}}:</b> {{interval.from}} — {{interval.to}}
                        </li>
                      </ul>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div class="table-wrapper">
              <table class="contacts">
                <tbody>
                  <tr
                    v-for="contact in building.employee_contacts"
                    v-bind:key="contact.cid"
                  >
                    <td class="photo">
                      <div class="photo-wrapper">
                        <img v-if="contact.photo" :src="'/static/contact_photos/'+contact.photo"
                        alt="Фотокарточка">
                        <img v-else :src="'/static/contact_photos/default.png'"
                        alt="Фотокарточка">
                        <div></div>
                      </div>
                    </td>
                    <td>
                      <p>
                        <b>{{contact.post}}</b> —
                        {{contact.surname}} {{contact.name}} {{contact.patronymic}}
                      </p>
                      <p><a :href="`mailto:${contact.email}`">{{contact.email}}</a></p>
                      <p><b>{{contact.phone}}</b></p>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </b-tab>
        </b-tabs>

      </section>

      <section class="box">
        <h2>Реквизиты учреждения</h2>
        <ul class="requisites">
          <li
            v-for="(requisite, rIndex) in contactsData.requisites"
            v-bind:key="rIndex"
          >
            <b>{{requisite.title}}:</b> {{requisite.value}}
          </li>
        </ul>
      </section>

    </section>

    <template v-else-if="this.$route.path==='/news'">

      <b-pagination-nav
        class="text-center"
        :number-of-pages="pagesNews.pages"
        :pages="pagination"
        use-router
        align="center"
        :first-text="'« Первая'"
        :prev-text="'‹ Предыдущая'"
        :next-text="'Следующая ›'"
        :last-text="'Последняя »'"
      ></b-pagination-nav>

      <div class="one-panel">

        <section class="posts">
          <article class="half-image" v-for="page in pagesNews.results" v-bind:key="page.uri">
            <header>
              <span class="date">
                {{$options.filters.moment(page.creation_date, 'MMMM DD, YYYY')}}
              </span>
              <h2>
                  <router-link
                    :to="{ name: 'SinglePage', params: { uri: page.uri }}"
                  >{{page.title}}</router-link>
              </h2>
            </header>
            <router-link
              :to="{ name: 'SinglePage', params: { uri: page.uri }}"
              class="image fit"
            >
              <img :src="'/static/page_covers/'+page.cover" alt="" />
            </router-link>
            <p class="line-clamp">{{page.seo_description}}</p>
            <ul class="actions special">
              <li>
                  <router-link
                    :to="{ name: 'SinglePage', params: { uri: page.uri }}"
                    class="button"
                  >Смотреть полностью</router-link>
              </li>
            </ul>
          </article>
        </section>
      </div>

      <b-pagination-nav
        class="text-center"
        :number-of-pages="pagesNews.pages"
        :pages="pagination"
        use-router
        align="center"
        :first-text="'« Первая'"
        :prev-text="'‹ Предыдущая'"
        :next-text="'Следующая ›'"
        :last-text="'Последняя »'"
      ></b-pagination-nav>

    </template>

    <section class="post" v-else>
      <header class="major">
        <span class="date">
          {{$options.filters.moment(this.pageData.creation_date, 'MMMM DD, YYYY')}}
        </span>
        <h1>
          {{this.pageData.title}}
        </h1>
        <p>
          {{this.pageData.seo_description}}
        </p>
      </header>

      <carousel
        :autoplay="false"
        :slideOnSwipe="false"
        v-if="pageData.gallery && pageData.gallery.length > 0"
        :data="pageData.gallery"
        class="w-100 mb-5"
      >
      </carousel>

      <div v-html="this.pageData.text">
      </div>

      <template
        v-if="this.pageData.files && this.pageData.files.length > 0"
      >
        <h2>Вложения:</h2>
        <ol>
          <li
            v-for="file in this.pageData.files"
            :key="file.fid"
          >
            <a :href="'/static/page_files/'+file.fname">
              {{file.name}} <i>({{file.extension}}, {{file.size}})</i>
            </a>
          </li>
        </ol>
      </template>
    </section>

  </div>
</template>

<style lang="css">
@import '../assets/css/main.css';
@import '../assets/css/slider.css';
@import '../assets/css/noscript.css';
</style>

<script>
import { mapState } from 'vuex';

export default {
  name: 'SinglePage',
  data() {
    return {
      pagination: [],
    };
  },
  computed: mapState({
    pageData: state => state.pageData,
    contactsData: state => state.contactsData,
    pagesNews: state => state.pagesNews,
  }),
  components: {
  },
  created() {
    this.fetchData();
  },
  watch: {
    $route: 'fetchData',
    pageData: function galleryHandler(pageData) {
      if (pageData.gallery && pageData.gallery.length > 0) {
        pageData.gallery.forEach((image) => {
          this.$set(
            image,
            'content',
            createElement => (
              createElement('div', {
                class: 'slide',
              },
              [
                createElement('div', {
                  attrs: {
                    style: `background-image:url(/static/page_gallery/${image.fname})`,
                  },
                  class: '',
                }),
                createElement('span', [`${image.name}`]),
              ])
            ),
          );
        });
      }
    },
    pagesNews: function paginationHandler(pagesNews) {
      this.pagination = [];
      for (let i = 0; i < pagesNews.pages; i += 1) {
        this.pagination.push({ link: { query: { start: (i * 6) + 1, limit: 6 } }, text: i + 1 });
      }
    },
  },
  methods: {
    fetchData() {
      this.$store.dispatch('loadPageData', { uri: this.$route.params.uri });
      if (this.$route.path === '/contacts') {
        this.$store.dispatch('loadContactsData');
      }
      if (this.$route.path === '/news') {
        this.$store.dispatch('loadPagesNews', { start: this.$route.query.start, limit: this.$route.query.limit });
      }
    },
  },
};
</script>
