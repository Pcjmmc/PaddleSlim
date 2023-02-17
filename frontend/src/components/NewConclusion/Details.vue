<template>
  <div style="margin-top:0.5%;">
    <p slot="title" style="text-align: left;font-size: 16px;">
      <span>负责人:（{{ owner.replace(/,/g, " | ") }}）</span>
      <span style="float: right">最新更新时间: {{ date }} </span>
    </p>
    <div v-for="(item, index) in risk" :key="index" style="margin-top:1%;">
      <desc-detail :item="item" :index="index"></desc-detail>
    </div>
    <Row style="margin-top:1%;">
      <Form :label-width="75">
        <Col span="24">
          <b><Form-item label="回测进度:">
            目前进行第
              <Input-number readonly size="small" :max="100" :min="0" v-model="regression.round"></Input-number>
              轮测试，共有流水线<Input-number readonly size="small" :max="100" :min="0" v-model="regression.total"></Input-number>
              条，成功<Input-number readonly size="small" :max="100" :min="0" v-model="regression.pass"></Input-number>
              条，失败<Input-number readonly size="small" :max="100" :min="0" v-model="regression.fail"></Input-number>
              条，进行中<Input-number readonly size="small" :max="100" :min="0" v-model="regression.running"></Input-number>条。
          </Form-item></b>
        </Col>
      </Form>
    </Row>
  </div>
</template>

<script>

import Cookies from 'js-cookie';
import DescDetail from './DescDetail.vue';

export default {
  name: 'Details',
  props: {
    idx: {
      type: [Number],
      default: function () {
        return 0;
      }
    },
    date: {
      type: [String],
      default: function () {
        return '';
      }
    },
    moduleid: {
      type: [Number],
      default: function () {
        return 0;
      }
    },
    modulename: {
      type: [String],
      default: function () {
        return '';
      }
    },
    owner: {
      type: [String],
      default: function () {
        return '';
      }
    },
    risk: {
      type: [Array],
      default: function () {
        return [
        ];
      }
    },
    regression: {
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
</style>
