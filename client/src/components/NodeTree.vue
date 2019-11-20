<template>
  <li
    v-bind:class="[
      node.level > 1 && node.children && node.children.length ? 'has-sub'
      : node.children && node.children.length ? 'has-sub' : '']"
    v-if="node.level!=0"
    :title="node.title"
  >
    <template v-if="node.pages && node.pages.length === 1">
      <b-link :to="{name: 'SinglePage', params: { uri: node.pages[0].uri }}">
        {{node.title}}
      </b-link>
    </template>
    <template v-else-if="node.id === 54">
      <b-link :to="{name: 'SinglePage', params: { uri: 'news' }, query: { start: 1, limit: 6 }}">
        {{node.title}}
      </b-link>
    </template>

    <b-link v-else>
      {{node.title}}
    </b-link>

    <ul
      v-if="node.children && node.children.length"
      v-bind:class="[((node.level > 1) && (node.children && node.children.length)) ? 'child' : '']"
    >
      <node v-for="child in node.children" v-bind:key="child.id" :node="child"></node>
    </ul>
  </li>
  <ul
    v-bind:class="['links', search ? 'hidden' : '']"
    v-else
  >
    <template v-if="node.children && node.children.length">
      <node v-for="child in node.children" v-bind:key="child.id" :node="child"></node>
    </template>
  </ul>
</template>

<script>
export default {
  name: 'node',
  props: {
    node: Object,
    search: Boolean,
  },
};
</script>
