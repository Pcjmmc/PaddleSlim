<template>
  <div class="all-line-row">
    <el-tabs
      v-model="tabName"
      type="card"
      @tab-click="clickTab"
    >
      <el-tab-pane label="主页面" name="home">
        <home-page></home-page>
      </el-tab-pane>
      <el-tab-pane label="任务页面" name="task">
        <task></task>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import HomePage from './HomePage.vue';
import Task from './MyTask.vue';
export default {
data: function () {
    return {
    tabName: 'home'
    };
},
watch: {
},
mounted: function () {
},
components: {
    HomePage,
    Task
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
  font-size: 14px;
}
</style>
