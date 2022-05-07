<template>
  <div
    style="margin-bottom: 10px;"
  >
    <Table
      :columns="columns"
      :data="data"
      style="margin-right: 2%"
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

