<template>
  <div>
    <div v-if="JSON.stringify(compile)!=='{}'">
      <h3>编译任务</h3>
      <Card class="center-card-s">
        <p>编译参数:</p>
        <div style="font-size:14px;margin-left: 2%;">
          <p>类型: {{ compile.env.type }}</p>
          <p>取值: {{ compile.env.value }}</p>
          <p>python: {{ compile.env.python }}</p>
          <p>系统: {{ compile.env.os }}</p>
          <p>cuda: {{ compile.env.cuda }}</p>
          <p>分支: {{ compile.env.branch }}</p>
        </div>
        <p>创建时间: {{ compile.create_time }}</p>
        <p>更新时间: {{ compile.update_time }}</p>
        <p>包地址: {{ compile.wheel }}</p>
      </Card>
    </div>
    <div v-if="JSON.stringify(mission)!=='{}'">
      <h3>测试任务</h3>
      <div v-for="(val, key, idx) in mission">
        <Card class="center-card-s">
          <div slot="title">
            <Button>{{ key }}</Button>
            <Button>{{ val.status }}</Button>
          </div>
          <div>
            <p>任务名: {{ val.description }}</p>
            <p>创建时间: {{ val.create_time }}</p>
            <p>更新时间: {{ val.update_time }}</p>
            <p>执行结果: {{ val.result }}</p>
          </div>
        </Card>
      </div>
    </div>
  </div>
</template>
<script>

import { FrameWorkJobDetail } from '../../api/url.js';
import api from '../../api/index';

export default {
  name: 'fsdetails',
  data: function () {
    return {
      id: '',
      status: '',
      compile: {},
      mission: {}
    };
  },
  watch: {
  },
  mounted: function () {
    // this.getDetails();
  },
  components: {
  },
  computed: {
  },
  methods: {
    async getDetails(id) {
      let params = {
        id: id
      };
      const {code, data, msg} = await api.get(FrameWorkJobDetail, params);
      if (parseInt(code, 10) === 200) {
        // 塞到datas的detais 字段里面
        this.id = data.id;
        this.status = data.status;
        if (typeof data.compile === 'object') {
          this.compile = data.compile;
          this.compile.env = JSON.parse(this.compile.env);
        } else {
          this.compile = {};
        }
        this.mission = typeof data.mission === 'object' ? data.mission : {};
      } else {
        this.$Message.error({
          content: '请求出错: ' + msg,
          duration: 30,
          closable: true
        });
      }
    }
  }
};
</script>

<style scoped>
  .center-card-s {
    width: 90%;
    max-height: 600px;
    overflow:auto;
    font-size: 16px;
    border-color:green;
  }
.one-fifth-video-col {
  margin-right: 2%;
  margin-left: 2%;
}
</style>