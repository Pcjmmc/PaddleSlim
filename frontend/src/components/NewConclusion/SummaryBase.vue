<template>
  <div style="margin-left: 1%;">
    <desc-detail :item="datas" :index="idx"></desc-detail>
  </div>
</template>

<script>

import DescDetail from './DescDetail.vue';

export default {
  name: 'SummaryBase',
  props: {
    idx: {
      type: [Number],
      default: function () {
        return '';
      }
    },
    datas: {
      type: [Object],
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
    DescDetail
  },
  methods: {
  }
};
</script>

<style scoped>
.center-card-s {
  width: 100%;
  max-height: 600px;
  overflow: auto;
  margin-bottom: 1%
}
.all-line-row {
  margin-top: 1%;
  margin-bottom: 1%;
  margin-left: 1%;
  margin-right: 1%;
  font-size:14px;
}
.btn-success {
  color: #fff;
  background-color: #67c23a;
  border-color: #67c23a;
}
.ivu-form-item{
  margin-bottom: 6px;
  font-size: 14px;
}
</style>
