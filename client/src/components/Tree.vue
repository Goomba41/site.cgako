<template>
  <div class="tree-menu">
    <div class="tree-item" :style="indent">{{ label }}</div>
    <Tree
      v-for="node in nodes"
      :nodes="node.children"
      :label="node.name"
      :depth="depth + 1"
      v-bind:key="node.id"
    >
    </Tree>
  </div>
</template>
<script>
export default {
  props: ['label', 'nodes', 'depth'],
  name: 'Tree',
  computed: {
    indent() {
      return { transform: `translate(${this.depth * 50}px)` };
    },
  },
};
</script>
