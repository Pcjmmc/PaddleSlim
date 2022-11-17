<template>
  <div>
    <Tabs
      :value="tabName"
      v-on:on-click="clickTab"
    >
      <TabPane
        label="个人空间"
        name="personal"
      >
      <compile-service></compile-service>
      </TabPane>
      <TabPane
        label="全局视图"
        name="globle"
      >
      </TabPane>
    </Tabs>
  </div>
</template>
<script>

import CompileService from './CompileService.vue';

export default {
  data: function () {
    return {
      tabName: 'personal'
    };
  },
  watch: {
  },
  mounted: function () {
  },
  components: {
    CompileService
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