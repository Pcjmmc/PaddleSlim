<template>
  <div
    style="margin-bottom: 10px;"
  >
    <Table
      border
      :columns="columns"
      :data="data"
    >
    </Table>
  </div>
</template>

<script>

export default {
  name: 'frameDetailBase',
  props: {
    'data': {
      type: [Array],
      default: function () {
        return [];
      }
    },
    'columns': {
      type: [Array],
      default: function () {
        return [];
      }
    }
  },
  data: function () {
    return {
    };
  },
  mounted: function () {
  },
  components: {
  },
  methods: {
  }
};
</script>

