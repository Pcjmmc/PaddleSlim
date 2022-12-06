<template>
  <div class="all-line-row">
    <el-tabs
      v-model="tabName"
      type="card"
      @tab-click="clickTab"
    >
      <el-tab-pane
        label="个人空间"
        name="personal"
      >
      <compile-service></compile-service>
      </el-tab-pane>
      <el-tab-pane
        label="全局视图"
        name="globle"
      >
      <compile-globle></compile-globle>
      </el-tab-pane>
    </el-tabs>
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
    clickTab(tag, event) {
    }
  }
};
</script>

<style scoped>
.all-line-row {
  margin-top: 1%;
  margin-bottom: 1%;
  margin-left: 1%;
  margin-right: 1%;
  font-size:14px;
}
</style>