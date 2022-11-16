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
      <person-window></person-window>
      </TabPane>
      <TabPane
        label="项目空间"
        name="project"
      >
      </TabPane>
    </Tabs>
  </div>
</template>
<script>

import PersonWindow from './PersonWindow.vue';

export default {
name: 'PaddleDemand',
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
