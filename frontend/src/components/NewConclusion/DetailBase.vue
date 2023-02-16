<template>
  <div>
      <el-tabs
        type="card"
        v-model="childname"
      >
        <el-tab-pane
          :label="item.module"
          :name="item.module"
          :key="index"
          v-for="(item, index) in allData"
        >
          <Details
            :idx="index"
            :moduleid="item.id"
            :date="item.create_time"
            :modulename="item.module"
            :owner="item.owner"
            :risk="item.risk"
            :regression="item.regression"
          ></Details>
      </el-tab-pane>
    </el-tabs>
</div>
</template>

<script>

import Details from './Details.vue';
import { dateFmt } from '../../util/help.js';

export default {
  name: 'DetailBase',
  props: {
    settings: {
      type: [Array],
      default: function () {
        return [];
      }
    },
    content: {
      type: [Array],
      default: function () {
        return [];
      }
    }
  },
  data: function () {
    return {
      childname: '编译安装',
      allData: []
    };
  },
  watch: {
  },
  components: {
    Details
  },
  mounted: async function () {
    this.allData = this.RestructData();
  },
  computed: {
  },
  methods: {
    RestructData() {
      let settings = this.settings;
      let content = this.content;
      for (var i = 0; i < settings.length; i++) {
          settings[i].risk = [];
          settings[i].regression = {
            round: 0,
            total: 0,
            pass: 0,
            fail: 0,
            running: 0
          };
          settings[i].create_time = dateFmt(new Date(), 'yyyy-MM-dd hh:mm:ss');
        for (var j = 0; j < content.length; j++) {
          if (settings[i].id === content[j].module_id) {
            // 将数据解析出来，拼装到settings
            let detail = JSON.parse(content[j].content);
            settings[i].risk = detail.risk;
            settings[i].regression = detail.regression;
            settings[i].create_time = content[j].create_time;
          }
        }
      }
      return settings;
    }
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
