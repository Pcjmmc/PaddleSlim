<template>
  <div style="margin-top: 1%;margin-left:1%;margin-right:1%;">
    <el-tabs
      v-model="tabName"
      type="card"
      @tab-click="clickTab"
    >
      <el-tab-pane
        label="个人空间"
        name="personal"
      >
      <person-window></person-window>
      </el-tab-pane>
      <el-tab-pane
        label="团队空间"
        name="project"
      >
      <global-view></global-view>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>
<script>

import PersonWindow from './PersonWindow.vue';
import GlobalView from './GlobalView.vue';

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
    PersonWindow,
    GlobalView
  },
  computed: {},
  methods: {
    clickTab(tab, event) {
    }
  }
};
</script>
