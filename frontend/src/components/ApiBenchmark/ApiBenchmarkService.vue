<template>
  <div class="all-line-row">
    <el-tabs
      v-model="tabName"
      type="card"
      @tab-click="clickTab"
    >
      <el-tab-pane label="主页面" name="personal">
        <home-page></home-page>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import HomePage from './HomePage.vue';

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
    HomePage
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
