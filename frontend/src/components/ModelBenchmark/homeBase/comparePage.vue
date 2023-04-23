<template>
  <div>
    <div style="margin-top:1%;">
      <Card>
        <Form
          :model="search"
          :label-width="65"
          style="width: 100%"
        >
          <Row>
            <Col span="5">
              <FormItem label="任务名:" prop="name">
                <Select
                  clearable
                  v-model="search.name"
                  :transfer="true"
                  :popper-append-to-body="false"
                  v-on:on-change="upDateChildDatas"
                >
                  <Option
                    :key="index"
                    :value="item"
                    v-for="(item, index) in allTasks"
                  >{{ item }}</Option>
                </Select>
              </FormItem>
            </Col>
            <Col span="4">
              <FormItem label="配置:" prop="dt">
                <Select
                  clearable
                  v-model="search.conf"
                  :transfer="true"
                  :popper-append-to-body="false"
                  v-on:on-change="upDateChildDatas"
                >
                  <Option
                    :key="index"
                    :value="item"
                    v-for="(item, index) in allConfs"
                  >{{ item }}</Option>
                </Select>
              </FormItem>
            </Col>
            <Col span="4">
              <FormItem label="指标:" prop="dt">
                <Select
                  clearable
                  v-model="search.indicator"
                  :transfer="true"
                  :popper-append-to-body="false"
                  v-on:on-change="upDateChildDatas"
                >
                  <Option
                    :key="index"
                    :value="item"
                    v-for="(item, index) in allIndicators"
                  >{{ item }}</Option>
                </Select>
              </FormItem>
            </Col>
            <Col span="4">
              <FormItem label="类型:" prop="dt">
                <Select
                  clearable
                  v-model="search.type"
                  :transfer="true"
                  :popper-append-to-body="false"
                  v-on:on-change="upDateChildDatas"
                >
                  <Option
                    :key="index"
                    :value="item"
                    v-for="(item, index) in allTypes"
                  >{{ item }}</Option>
                </Select>
              </FormItem>
            </Col>
            <Col span="7">
              <FormItem label="时间:" prop="dt">
                <DatePicker
                  clearable
                  type="daterange"
                  placement="bottom-end"
                  placeholder=" 开始时间 ～ 结束时间 "
                  v-model="search.dt"
                  style="width:80%"
                  v-on:on-change="upDateChildDatas"
                ></DatePicker>
              </FormItem>
            </Col>
          </Row>
        </Form>
        <compare-prod ref="child1" :search="search"></compare-prod>
        <compare-sence ref="child2" :search="search"></compare-sence>
      </Card>
    </div>
  </div>
</template>
<script>

import compareProd from './compareProd.vue';
import compareSence from './compareSence.vue';

export default {
  name: 'comparePage',
  data: function () {
    return {
      allTasks: [
        '单机11.2_8.1_V100全量例行',
        '多机11.8_8.6.1_V100全量例行',
        '单机11.8_8.6.1_V100全量例行',
        '单机11.2_8.1_RTX3090_S_P0例行'
      ],
      allTypes: [
        '模型级别',
        '配置级别'
      ],
      allIndicators: [
        'ips',
        'gpu_mem',
        'gpu_use',
        'cpu_use',
        'accuracy'
      ],
      allConfs: [
        'N1C1',
        'N1C8'
      ],
      search: {
        dt: '',
        name: '',
        indicator: '',
        conf: ''
      }
    };
  },
  watch: {
  },
  mounted: async function () {
    await this.getSettings();
    await this.upDateChildDatas();
  },
  components: {
    compareProd,
    compareSence
  },
  computed: {},
  methods: {
    clickTab(tag, event) {
    },
    async getSettings() {
      // this.allTasks = [];
      // this.allTypes = [];
      // this.allIndicators = [];
      // this.allConfs = [];
    },
    async upDateChildDatas() {
      // 调用两个子组件
      this.$refs.child1.getDatas();
      this.$refs.child2.getDatas();
    }
  }
};
</script>

<style scoped>
</style>