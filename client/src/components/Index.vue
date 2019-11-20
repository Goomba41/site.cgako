<template>
<div id="body" class="">

    <div id="wrapper" class="">

        <a
          id="back-to-top"
          href="#"
          class="button icon solo fa-arrow-up hidden"
          v-scroll="backToTop"
          @click.prevent="scrollToTop"
        >
        </a>

        <header id="header">
            <b-link :to="{name: 'Index'}" class="logo">
<!--
              <img alt="Логотип" class="logo-img" src="../assets/images/kirov.png"/>
-->
              <img alt="Логотип" class="logo-img" src="../assets/images/archive.png"/>
              <div>
                <span class="naming">
                  Центральный<br/>
                </span>
                <span class="naming">
                  государственный<br/>
                </span>
                <span class="naming">
                  архив<br/>
                </span>
                <span class="naming">
                  Кировской<br/>
                </span>
                <span class="naming">
                  области<br/>
                </span>
                <span class="sml">на главную</span>
              </div>
            </b-link>
        </header>

        <nav id="nav" v-scroll="navStick">
          <NodeTree :node="menu" :search="searchActive"></NodeTree>
          <ul
            v-bind:class="['search', searchActive ? 'active' : '']"
          >
            <li>
              <input
                ref="searchInput"
                placeholder="Поиск по сайту"
                type="text"
                v-bind:class="['search_fld', searchActive ? 'active' : '']"
              >
            </li>
          </ul>

          <ul class="icons">
            <li
              v-bind:class="['go-search', searchActive ? '' : 'hidden']"
            >
              <a href="#" class="search_btn icon fa-arrow-right">
                <span class="label">Поиск</span>
              </a>
            </li>
            <li>
              <a
                href="#"
                v-bind:class="['icon', searchActive ? 'fa-close' : 'fa-search']"
                @click.prevent="searchActive = !searchActive"
              >
                <span class="label">Открыть/закрыть поисковую строку</span>
              </a>
            </li>
          </ul>
        </nav>

        <div id="main" v-if="this.$route.name==='Index'">

          <div class="banners">
            <carousel
              v-if="banners && banners.length > 0"
              :data="banners"
              :controls="false"
              :interval="15000"
              indicator-type="disc"
              class="w-100"
            >
            </carousel>

          </div>
          <div class="two-panels">
            <main class="firstpanel">
              <div class="header">
                  <h2>Анонсы мероприятий</h2>
              </div>
              <carousel
                v-if="announces && announces.length > 0"
                :data="announces"
                :controls="false"
                :interval="10000"
                indicator-type="disc"
                class="w-100 announces mb-3"
                :autoplay="false"
                :slideOnSwipe="false"
                :pauseOnEnter="false"
              >
              </carousel>

              <div class="header">
                  <h2>Новое в архиве</h2>
              </div>
              <section class="posts">

                  <article
                    v-for="page in lastPages"
                    v-bind:key="page.uri"
                    class="post"
                  >
                    <router-link
                      :to="{ name: 'SinglePage', params: { uri: page.uri }}"
                      class="image fit h-100"
                    >
                      <img
                        :src="'/static/page_covers/'+page.cover"
                      >
                      <header>
                        <span class="date">
                          {{$options.filters.moment(page.creation_date, 'MMMM DD, YYYY')}}
                        </span>
                        <h2 class="line-clamp pr-3 pl-3">
                          {{page.title}}
                        </h2>
                      </header>
                    </router-link>
                  </article>
              </section>
            </main>

              <div class="secondPanel">
                  <aside id="history-dates">
                      <h3>Памятные даты истории России:</h3>
                      <div class="box">
                          <span class="history-date-time">
                              Сегодня (74 года)
                          </span>
                          <h4>Памятная дата военной истории России</h4>
                          <p>
                            В этот день в 1945 году на Эльбе произошла встреча
                            советских и американских войск.
                            Рукопожатие на Эльбе стало символом
                            братства по оружию стран, вместе сражавшихся
                            с нацистской Германией. Остатки вермахта теперь были
                            расколоты на две части — северную и южную.
                          </p>
                      </div>
                  </aside>
              </div>

          </div>

<!--
          <section>
              <h4>Дополнительный блок</h4>
          </section>
-->
        </div>

        <router-view v-else></router-view>

        <footer id="footer">
            <section>
                <h4>Обратная связь</h4>
                <form method="post" action="#">
                    <div class="fields">
                        <div class="field">
                            <label for="name">Ваше имя</label>
                            <input type="text" name="name" id="name" />
                        </div>
                        <div class="field">
                            <label for="email">Email</label>
                            <input type="text" name="email" id="email" />
                        </div>
                        <div class="field">
                            <label for="message">Ваше сообщение</label>
                            <textarea name="message" id="message" rows="3"></textarea>
                        </div>
                    </div>
                    <ul class="actions">
                        <li><input type="submit" value="Отправить сообщение" /></li>
                    </ul>
                </form>
            </section>
            <section class="contact">
                <h4>Контактная информация</h4>

                <h3>Адрес</h3>
                <p>
                  Юридический адрес (главный корпус): 610027,
                  г. Киров, ул. Карла Маркса, д. 142
                </p>

                <h3>Телефон</h3>
                <p><a href="#">+7 (8332) 357-556</a></p>

                <h3>Email</h3>
                <p><a href="#">info@cgako.ru</a></p>

                <h3>Соц. сети</h3>
                <ul class="icons alt">
                    <li>
                      <a href="#" class="icon alt fa-vk">
                        <span class="label">VK</span>
                      </a>
                    </li>
                    <li>
                      <a href="#" class="icon alt fa-instagram">
                        <span class="label">Instagram</span>
                      </a>
                    </li>
                </ul>

            </section>
            <section class="colleagues">
                    <h4>Коллеги</h4>
                    <ul class="colleagues-list">
                        <li><a class="fed_archives" href="http://archives.ru" title="Федеральное архивное агентство"></a></li>
                        <li><a class="fed_archives_portal" href="http://www.rusarchives.ru" title="Портал архивы России"></a></li>
                        <li><a class="kirov_minkult" href="http://cultura.kirovreg.ru/" title="Министерство культуры Кировской области"></a></li>
                    </ul>
            </section>
        </footer>

        <div id="copyright">
            <ul><li>&copy; {{copyDate}} ЦГАКО</li><li>Дизайн: <a href="https://vk.com/goomba41">Бородавкин А.В.</a></li><li>Использование материалов сайта без согласования с КОГБУ ЦГАКО запрещено</li></ul>
        </div>

    </div>

</div>

</template>

<style lang="css">
@import '../assets/css/main.css';
@import '../assets/css/slider.css';
@import '../assets/css/noscript.css';
</style>

<script>
import { mapState } from 'vuex';
import NodeTree from './NodeTree';

export default {
  name: 'Index',
  data() {
    return {
      currentYear: new Date().getFullYear(),
      initialYear: 2019,
      searchActive: false,
      initialOffset: 0,
      announces: [
        {
          id: 1,
          title: 'ОТКРЫТИЕ ВЫСТАВКИ ФОТОГРАФИИ "ГЕРОИ СРЕДИ НАС..."',
          address: 'Казанская 16А',
          time: '11:00 27 декабря 2018 года',
          text: '27 декабря 2018 года состоится презентация выставки фотографий Е. А. Глазыриной «Герои среди нас...», посвященной 76-й годовщине со дня начала Великой Отечественной войны.',
          content(createElement, content) {
            return createElement('section', [
              createElement('h3', {
                class: 'noselect',
              }, [`${content.time}, ${content.address}, ${content.title}`]),
              createElement('p', {
                class: 'line-clamp noselect m-0',
              }, [`${content.text}`]),
            ]);
          },
        },
        {
          id: 2,
          title: 'ОТКРЫТИЕ ВЫСТАВКИ ФОТОГРАФИИ "ГЕРОИ СРЕДИ НАС..."',
          address: 'Казанская 16А',
          time: '11:00 27 декабря 2018 года',
          text: '27 декабря 2018 года состоится презентация выставки фотографий Е. А. Глазыриной «Герои среди нас...», посвященной 76-й годовщине со дня начала Великой Отечественной войны.',
          content(createElement, content) {
            return createElement('section', [
              createElement('h3', {
                class: 'noselect',
              }, [`${content.time}, ${content.address}, ${content.title}`]),
              createElement('p', {
                class: 'line-clamp noselect m-0',
              }, [`${content.text}`]),
            ]);
          },
        },
      ],
    };
  },
  created() {
    this.fetchData();
  },
  mounted() {
    this.initialOffset = document.querySelector('nav#nav').offsetTop;
  },
  computed: mapState({
    menu: state => state.menu,
    banners: state => state.banners,
    lastPages: state => state.lastPages,
    copyDate() {
      if (this.currentYear > this.initialYear) {
        return `${this.initialYear}-${this.currentYear}`;
      }
      return `${this.initialYear}`;
    },
  }),
  components: {
    NodeTree,
  },
  methods: {
    fetchData() {
      this.$store.dispatch('loadMenu');
      if (this.$route.name === 'Index') {
        this.$store.dispatch('loadBanners');
        this.$store.dispatch('loadLastPages', { limit: 7 });
      }
    },
    navStick(evt, el) {
      if (el) {
        if (window.pageYOffset > this.initialOffset) {
          el.classList.add('sticky');
        } else {
          el.classList.remove('sticky');
        }
      }
    },
    backToTop(evt, el) {
      if (el) {
        if (window.scrollY > 500) {
          el.classList.remove('hidden');
        } else {
          el.classList.add('hidden');
        }
      }
    },
    scrollToTop() {
      window.scrollTo({
        top: 0,
        behavior: 'smooth',
      });
    },
  },
  watch: {
    $route: 'fetchData',
    banners: function bannersHandler(banners) {
      if (banners && banners.length > 0) {
        banners.forEach((banner) => {
          this.$set(
            banner,
            'content',
            createElement => (
              createElement('div', {
                class: 'banner-slide',
              }, [
                createElement('a', {
                  attrs: {
                    href: `${banner.uri}`,
                  },
                  class: 'w-100',
                },
                [
                  createElement('img', {
                    attrs: {
                      src: `/static/page_covers/${banner.cover}`,
                    },
                    class: 'banner-image noselect',
                  }),
                  createElement('section', {
                    class: 'banner-desc noselect',
                  },
                  [
                    createElement('h4', {
                      class: 'noselect',
                    }, [`${banner.title}`]),
                    createElement('p', {
                      class: 'line-clamp noselect',
                    }, [`${banner.seo_description}`]),
                  ]),
                ]),
              ])
            ),
          );
        });
      }
    },
  },
};
</script>
