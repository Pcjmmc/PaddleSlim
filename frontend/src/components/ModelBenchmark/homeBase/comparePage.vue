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
              <FormItem label="任务名:" prop="task_name">
                <Select
                  clearable
                  filterable
                  v-model="search.task_name"
                  :transfer="true"
                  :popper-append-to-body="false"
                  v-on:on-change="updateTaskName"
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
              <FormItem label="配置:" prop="config_name">
                <Select
                  clearable
                  v-model="search.config_name"
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
              <FormItem label="指标:" prop="index_name">
                <Select
                  clearable
                  v-model="search.index_name"
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
              <FormItem label="类型:" prop="summary_type">
                <Select
                  clearable
                  v-model="search.summary_type"
                  :transfer="true"
                  :popper-append-to-body="false"
                  v-on:on-change="upDateChildDatas"
                >
                  <Option
                    :key="index"
                    :value="item.type_id"
                    v-for="(item, index) in allTypes"
                  >{{ item.type_name }}</Option>
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
import api from '../../../api/index';
import { ModelsBenchmarkHomeSettings } from '../../../api/url.js';

export default {
  name: 'comparePage',
  data: function () {
    return {
      allSettings: {
      },
      allTasks: [
      ],
      allTypes: [
      ],
      allIndicators: [
      ],
      allConfs: [
      ],
      search: {
        dt: [this.getBeginData(), new Date()],
        task_name: '例行_单机_11.2_8.1_V100_全量',
        index_name: 'ips',
        config_name: 'N1C1',
        summary_type: ''
      }
    };
  },
  watch: {
    allSettings: function () {
      let tmp = [];
      let tmp_conf = [];
      for (let key in this.allSettings) {
        if (this.allSettings.hasOwnProperty(key)) {
          tmp.push(key);
        }
      }
      // 设置一个默认值
      this.allTasks = tmp;
      if (this.allTasks.length > 0) {
        this.allConfs = this.allSettings[this.search.task_name];
      }
    }
  },
  mounted: async function () {
    this.initData();
    await this.getSettings();
    await this.upDateChildDatas();
  },
  components: {
    compareProd,
    compareSence
  },
  computed: {
  },
  methods: {
    getBeginData() {
      // 在end_time的基础上+1， 因为end_time代表的今天0点0分0秒的时间
      let begin_time = new Date();
      begin_time = begin_time.setDate(begin_time.getDate() - 30);
      begin_time = new Date(begin_time);
      return begin_time;
    },
    initData() {
      this.allSettings = {};
      this.allTypes = [];
      this.allIndicators = [];
      this.allConfs = [];
      this.allTasks = [];
    },
    clickTab(tag, event) {
    },
    async getSettings() {
      const { code, data, message } = await api.get(ModelsBenchmarkHomeSettings);
      if (parseInt(code, 10) === 200) {
        this.allSettings = data.task_list;
        this.allTypes = data.summary_type_list;
        this.allIndicators = data.index_list;
        this.search.summary_type = data.summary_type_list[1].type_id;
      } else {
        this.$Message.error({
            content: '请求出错: ' + message,
            duration: 30,
            closable: true
        });
      }
    },
    // 只要task_name; 将配置更新下，再默认选择第一个
    async updateTaskName() {
      this.allConfs = this.allSettings[this.search.task_name];
      this.search.config_name = this.allConfs[0];
      await this.upDateChildDatas();
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