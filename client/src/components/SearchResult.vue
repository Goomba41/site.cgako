<template>

<!-- Main -->
<div id="main">
  <article>
    <h2 class="search-result-header m-0">
      Результаты поиска «<span>{{this.$route.query.q}}</span>»
      (<span>{{searchResults.count}}</span> записи найдено)
    </h2>
<!--
    <div class="row">

      <div class="col-4 col-12-small">
        <input type="radio" id="demo-priority-low" name="demo-priority" checked="">
        <label for="demo-priority-low">Полнотекстовый поиск</label>
      </div>
      <div class="col-4 col-12-small">
        <input type="radio" id="demo-priority-low" name="demo-priority" checked="">
        <label for="demo-priority-low">Точное совпадение</label>
      </div>
      <div class="col-4 col-12-small">
        <select name="demo-category" id="demo-category">
          <option value="1">Сначала новые</option>
          <option value="1">Сначала старые</option>
          <option value="1">Сначала популярные</option>
          <option value="1">По алфавиту</option>
          <option value="1">По разделу</option>
        </select>
      </div>

    </div>
-->
  </article>

  <article class="results-list">
    <template v-if="searchResults.results && searchResults.results.length !== 0">
      <ol>
        <li v-for="row in searchResults.results" v-bind:key="row.id">
          <router-link
            :to="{ name: 'SinglePage', params: { uri: row.uri }}"
          >
            {{$options.filters.moment(row.creation_date, 'YYYY-MM-DD')}} /
            {{row.structure.title}} /
            <span>{{row.title}}</span>
          </router-link>
          <br>
          <span>{{row.seo_description}}</span>
        </li>
      </ol>
    </template>
    <template v-else>
      К сожалению по Вашему запросу ничего не найдено!
    </template>
  </article>

  <b-pagination-nav
    class="text-center"
    :number-of-pages="searchResults.pages"
    :pages="pagination"
    use-router
    align="center"
    :first-text="'« Первая'"
    :prev-text="'‹ Предыдущая'"
    :next-text="'Следующая ›'"
    :last-text="'Последняя »'"
  ></b-pagination-nav>

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
  name: 'SearchResult',
  data() {
    return {
      pagination: [],
    };
  },
  created() {
    this.fetchData();
  },
  mounted() {
  },
  computed: mapState({
    searchResults: state => state.searchResults,
  }),
  components: {

  },
  methods: {
    fetchData() {
      if (this.$route.name === 'SearchResult') {
        this.$store.dispatch('loadSearchResult',
          {
            start: this.$route.query.start,
            limit: this.$route.query.limit,
            q: this.$route.query.q,
          });
      }
    },
  },
  watch: {
    $route: 'fetchData',
    searchResults: function paginationHandler(searchResults) {
      this.pagination = [];
      for (let i = 0; i < searchResults.pages; i += 1) {
        this.pagination.push({
          link: {
            query: {
              start: (i * 20) + 1,
              limit: 20,
              q: this.$route.query.q,
            },
          },
          text: i + 1,
        });
      }
    },
  },
};
</script>
