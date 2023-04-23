<template>
  <div class="all-line-row">
    <div>
      <model-page></model-page>
    </div>
    <div>
      <frame-page></frame-page>
    </div>
    <div>
      <compare-page></compare-page>
    </div>
  </div>
</template>
<script>
import modelPage from './homeBase/modelPage.vue';
import framePage from './homeBase/framePage.vue';
import comparePage from './homeBase/comparePage.vue';

export default {
  name: 'homePage',
  data: function () {
    return {
    };
  },
  watch: {
  },
  mounted: function () {
  },
  components: {
    modelPage,
    framePage,
    comparePage
  },
  computed: {
  },
  methods: {
    clickTab() {
    },
    updateData() {
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