<template>
  <div style="">
    <Tabs
      :value="tabName"
      v-on:on-click="clickTab"
    >
      <TabPane
        label="编译服务"
        name="compile"
        icon="md-build"
      >
      <compile-service></compile-service>
      </TabPane>
      <TabPane
        label="测试服务"
        name="test"
        icon="md-hammer"
      >
      <test-service></test-service>
      </TabPane>
    </Tabs>
  </div>
</template>
<script>

import CompileService from './CompileService.vue';
import TestService from './TestService.vue';

export default {
  data: function () {
    return {
      tabName: 'compile'
    };
  },
  watch: {
  },
  mounted: function () {
  },
  components: {
    CompileService,
    TestService
  },
  computed: {},
  methods: {
    clickTab(name) {
      console.log('click name is', name);
    }
  }
};
</script>
<style scoped>
.bound{
}
</style>
<style>
.ivu-tabs-nav-container{
  font-size:18px;
}
</style>