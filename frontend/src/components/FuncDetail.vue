<template>
  <div>
    <div v-for="(item, key, index) in detail" v-if="detail">
      <func-base
        :detail="item.case_detail"
        :secondarytype="key"
        :summarydata="item.summary_data"
      ></func-base>
    </div>
  </div>
</template>

<script>
import api from '../api/index';
import { DetailUrl } from '../api/url.js';
import FuncBase from './Detail/FuncBase.vue';
export default {
  data: function () {
    return {
      detail: null
    };
  },
  mounted: function () {
    this.getData();
  },
  components: {
    FuncBase
  },
  computed: {
  },
  methods: {
    async getData() {
      let _params = {
        'tid': this.$route.query.tid,
        'build_id': this.$route.query.build_id,
        'task_type': this.$route.query.task_type,
        'secondary_type': this.$route.query.secondary_type,
        'reponame': this.$route.query.reponame
      };
      // 自己知道自己值传递了一个secondary_type
      const { code, data, message } = await api.get(DetailUrl, _params);
      if (message === 'success') {
        this.detail = data;
      } else {
        console.log('error', code);
        this.$Message.error({content: message || this.$trans('获取编译列表失败'), duration: 5, closable: true});
      }
    }
  }
};
</script>

<style scoped>
  .tips {
    color: #ff9900;
  }
  .all-line-row {
    margin-bottom: 0.5%;
    margin-left: 0.5%;
  }
  .center-card-s {
    width: 100%;
    max-height: 600px;
    overflow:auto;
    margin-bottom: 2%
  }
</style>
