<template>
  <div style="margin-top: 1%;">
    <person-window></person-window>
  </div>
</template>
<script>

import PersonWindow from './PersonWindow.vue';

export default {
name: 'PaddleDemand',
  data: function () {
    return {
      tabName: 'persion'
    };
  },
  watch: {
  },
  mounted: function () {
  },
  components: {
    PersonWindow
  },
  computed: {},
  methods: {
    clickTab(name) {
      console.log('click name is', name);
    }
  }
};
</script>
<style>
  .ivu-tabs-nav-container{
    font-size:18px;
  }
</style>
