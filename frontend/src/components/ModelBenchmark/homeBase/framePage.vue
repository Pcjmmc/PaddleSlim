<template>
  <div style="margin-top:1%;">
    <el-tabs
      v-model="tabName"
      type="card"
      @tab-click="clickTab"
    >
      <el-tab-pane
        label="Paddle模型数"
        name="paddle"
      >
      </el-tab-pane>
      <el-tab-pane
        label="竞品模型数"
        name="other"
      >
      </el-tab-pane>
      <frame-statistics :datas="datas"></frame-statistics>
    </el-tabs>
  </div>
</template>
<script>

import frameStatistics from './frameStatistics.vue';

export default {
  name: 'framePage',
  data: function () {
    return {
      tabName: 'paddle',
      datas: {
        pie: {
          option: [],
          datas: []
        },
        colum: {
          option: [],
          datas: {}
        }
      }
    };
  },
  watch: {
  },
  mounted: function () {
    this.getDatas();
  },
  components: {
    frameStatistics
  },
  computed: {},
  methods: {
    clickTab(name) {
      this.tabName = name.name;
      console.log('this.tabName', this.tabName);
      this.datas = {
        pie: {
          option: ['Clas', 'NLP', 'Seg', 'Speech', 'Video', 'OCR', 'Detection'],
          datas: [
            {value: 107, name: 'Clas'},
            {value: 10, name: 'NLP'},
            {value: 22, name: 'Speech'},
            {value: 30, name: 'Video'},
            {value: 5, name: 'OCR'},
            {value: 25, name: 'Detection'}
          ]
        },
        colum: {
          option: ['Clas', 'NLP', 'Seg', 'Speech', 'Video', 'OCR', 'Detection'],
          datas: {
            Clas: {FP32: 2, FP16: 1},
            NLP: {FP32: 10, FP16: 3},
            Seg: {FP32: 5, FP16: 6},
            Speech: {FP32: 6, FP16: 10},
            Video: {FP32: 9, FP16: 11},
            Detection: {FP32: 8, FP16: 12},
            OCR: {FP32: 7, FP16: 10}
          }
        }
      };
      console.log('this new datas', this.datas);
    },
    async getDatas() {
      this.datas = {
        pie: {
          option: ['Clas', 'NLP', 'Seg', 'Speech', 'Video', 'OCR', 'Detection'],
          datas: [
            {value: 100, name: 'Clas'},
            {value: 10, name: 'NLP'},
            {value: 20, name: 'Speech'},
            {value: 30, name: 'Video'},
            {value: 15, name: 'OCR'},
            {value: 25, name: 'Detection'}
          ]
        },
        colum: {
          option: ['Clas', 'NLP', 'Seg', 'Speech', 'Video', 'OCR', 'Detection'],
          datas: {
            Clas: {FP32: 20, FP16: 1},
            NLP: {FP32: 10, FP16: 3},
            Seg: {FP32: 5, FP16: 6},
            Speech: {FP32: 6, FP16: 10},
            Video: {FP32: 9, FP16: 21},
            Detection: {FP32: 8, FP16: 13},
            OCR: {FP32: 7, FP16: 11}
          }
        }
      };
    }
  }
};
</script>

<style scoped>
</style>