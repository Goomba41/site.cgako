<template>
    <footer class="row mx-auto w-100">
      <span class="caption p-3">
        <a href="https://ru.wikipedia.org/wiki/Авторское_право"
        v-b-tooltip.hover v-bind:title="$t('footer.tooltips.aboutCopyright')">
          <font-awesome-icon :icon="['far', 'copyright']" fixed-width size="1x"/>
        </a>
        {{$t('footer.copyrightText')}}, 2019
      </span>

      <span class="caption p-3 ml-auto">

        <span @click="setLocale('ru')">
          <flag iso="ru" :squared="false" v-bind:title="$t('footer.tooltips.languages.rus')"
          v-b-tooltip.hover></flag>
        </span>
        <span @click="setLocale('su')">
          <flag iso="su" :squared="false" v-bind:title="$t('footer.tooltips.languages.sul')"
          v-b-tooltip.hover></flag>
        </span>
        <span @click="setLocale('en')">
          <flag iso="us" :squared="false" v-bind:title="$t('footer.tooltips.languages.eng')"
          v-b-tooltip.hover></flag>
        </span>

        <a href="mailto:anton.borodawkin@yandex.ru" v-b-tooltip.hover
        v-bind:title="$t('footer.tooltips.developerLinks.email')">
          <font-awesome-icon :icon="['fa', 'at']" fixed-width size="1x"/>
        </a>
        <a href="https://github.com/Goomba41" v-b-tooltip.hover
        v-bind:title="$t('footer.tooltips.developerLinks.github')">
          <font-awesome-icon :icon="['fab', 'github']" fixed-width size="1x"/>
        </a>
        <a href="https://vk.com/goomba41" v-b-tooltip.hover
        v-bind:title="$t('footer.tooltips.developerLinks.vk')">
          Бородавкин А.В. c
          <font-awesome-icon :icon="['fa', 'heart']"
          style="color: red;" fixed-width size="1x"/>
        </a>
      </span>
    </footer>
</template>

<script>
export default {
  name: 'Footerline',
  data() {
    return {
    };
  },
  methods: {
    setLocale(locale) {
      this.$store.dispatch('changeLocale', locale);
    },
  },
};
</script>
