<template>
  <li
    v-bind:class="[
      node.level > 1 && node.children && node.children.length ? 'has-sub-sub'
      : node.children && node.children.length ? 'has-sub' : '']"
    v-if="node.level!=0"
  >
    <a href="#">{{node.name}}</a>
    <ul
      v-if="node.children && node.children.length"
      v-bind:class="[((node.level > 1) && (node.children && node.children.length)) ? 'child' : '']"
    >
      <node v-for="child in node.children" v-bind:key="child.id" :node="child"></node>
    </ul>
  </li>
  <ul class="links" v-else>
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
  },
};
</script>
