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
      <compile-globle></compile-globle>
      </TabPane>
    </Tabs>
  </div>
</template>
<script>

import CompileService from './CompileService.vue';
import CompileGloble from './CompileGloble.vue';

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
    CompileService,
    CompileGloble
  },
  computed: {},
  methods: {
    clickTab(name) {
      console.log('click name is', name);
    }
  }
};
</script>