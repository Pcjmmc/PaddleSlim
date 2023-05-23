<template>
  <div>
    <Card style="width: 100%;height: 450px;">
      <span style="float:left;width:50%;">
        <frame-pie
          title="模型库覆盖情况"
          :option="datas.pie.option"
          :optionData="datas.pie.datas"
        ></frame-pie>
      </span>
      <span style="float:right;width:50%;">
        <frame-colum
          title="FP配置覆盖情况"
          :option="datas.colum.option"
          :optionData="datas.colum.datas"
        ></frame-colum>
      </span>
    </Card>
  </div>
</template>
<script>

import framePie from './framePie.vue';
import frameColum from './frameColum.vue';

export default {
  props: {
    datas: {
      type: Object,
      default: function () {
        return {};
      }
    }
  },
  data: function () {
    return {
    };
  },
  watch: {
  },
  mounted: function () {
  },
  components: {
    framePie,
    frameColum
  },
  computed: {
  },
  methods: {
  }
};
</script>

<style scoped>
</style>