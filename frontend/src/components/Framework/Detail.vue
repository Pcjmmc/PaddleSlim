<template>
  <div>
    <div v-if="JSON.stringify(compile)!=='{}'">
      <h3>编译任务</h3>
      <Card class="center-card-s">
        <span>状态:</span>
        <Button type="success" v-if="compile.status==='done'">{{ compile.status }}</Button>
        <Button type="error" v-else-if="compile.status==='error'">{{ compile.status }}</Button>
        <Button type="info" v-else-if="compile.status==='running'">{{ compile.status }}</Button>
        <Button type="warning" v-else>{{ compile.status }}</Button>
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
        <p>包地址: <a :href="compile.wheel">{{ compile.wheel }}</a></p>
      </Card>
    </div>
    <div v-if="JSON.stringify(mission)!=='{}'">
      <h3>测试任务</h3>
      <div v-for="(val, key, idx) in mission">
        <Card class="center-card-s">
          <div slot="title">
            <span>任务名:</span>
            <Button type="primary">{{ getTaskName(key) }}</Button>
            <span style="margin-left: 2%;">状态:</span>
            <Button type="success" v-if="val.status==='done'">{{ val.status }}</Button>
            <Button type="error" v-else-if="val.status==='error'">{{ val.status }}</Button>
            <Button type="info" v-else-if="val.status==='running'">{{ val.status }}</Button>
            <Button type="warning" v-else>{{ val.status }}</Button>
          </div>
          <div>
            <p>创建时间: {{ val.create_time }}</p>
            <p>更新时间: {{ val.update_time }}</p>
            <p>执行结果:
              <a
                href="javascript:void(0)"
                style="font-size:13px;"
                @click="jumper(val.result)"
              > {{ val.result}} </a></p>
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
      mission: {},
      children: {
        op_function: '计算op精度测试',
        external_api_function: '功能性API测试',
        io_function: 'IO相关测试',
        distribution_api_function: '分布式API测试',
        jit_function: '动转静测试',
        jit_api_function: '动转静API单独组网测试',
        jit_models_function: '动转静模型子结构测试',
        api_benchmark: 'API性能测试',
        paddleclas: '图像识别',
        models_benchmark: '模型性能测试',
        infer: '预测部署',
        compile_function: '编译任务'
      }
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
    getTaskName(key) {
      return this.children[key];
    },
    jumper(href) {
      window.open(href, '_blank');
    },
    setColor(status) {
      let _status = status.toLowerCase();
      console.log('_status', _status);
      switch (_status) {
        case 'fail':
          return 'Error';
        case 'done':
          return 'success';
        default:
          return 'warning';
      }
    },
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