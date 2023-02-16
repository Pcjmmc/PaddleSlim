<template>
  <div style="margin-left: 1%;">
    <div>
      <Table :columns="columns7" :data="datas"></Table>
    </div>
  </div>
</template>

<script>

export default {
  name: 'SummaryBase',
  props: {
    datas: {
      type: [Array],
      default: function () {
        return {};
      }
    }
  },
  data: function () {
    return {
      columns7: [
        {
          title: '阶段',
          align: 'center',
          key: 'step'
        },
        {
          title: '总量',
          align: 'center',
          key: 'total'
        },
        {
          title: '成功',
          align: 'center',
          key: 'pass'
        },
        {
          title: '失败',
          align: 'center',
          key: 'fail'
        },
        {
          title: '运行中',
          align: 'center',
          key: 'running'
        },
        {
          title: '轮数',
          align: 'center',
          key: 'round'
        },
        {
          title: '进度',
          align: 'center',
          key: 'progress'
        }
      ]
    };
  },
  watch: {
  },
  mounted: function () {
  },
  components: {
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
  margin-bottom: 12px;
  font-size: 14px;
}
</style>
