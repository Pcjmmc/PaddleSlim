<template>
  <div id="chartPie" style="width: 500px;height: 350px;"></div>
</template>

<script>
import echarts from 'echarts';
require('echarts/theme/macarons');
export default {
  props: {
    column: {
      type: Array,
      default() {
        return [];
      }
    },
    xdata: {
      type: Array,
      default() {
        return [];
      }
    }
  },
  data() {
    return {
      chartPie: null
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.drawPieChart('chartPie');
    })
  },
  methods: {
    drawPieChart() {
      let mytextStyle = {
        color: "#333",
        fontSize: 18
      };
      let mylabel = {
        show: true,
        position: "right",
        offset: [30, 40],
        formatter: '{b} : {c} ({d}%)',
        textStyle: mytextStyle
      };
      this.chartPie = echarts.init(document.getElementById('chartPie'), 'macarons');
      this.chartPie.setOption({
        title: {
          text: 'Pie Chart',
          subtext: '风险进度',
          x: 'center'
        },
        tooltip: {
          trigger: 'item',
          formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        legend: {
          data: this.column,
          left: "center",
          top: "bottom",
          orient: "horizontal"
        },
        series: [
          {
            name: '访问来源',
            type: 'pie',
            radius: ['50%', '70%'],
            center: ['50%', '50%'],
            data: this.xdata,
            animationEasing: 'cubicInOut',
            animationDuration: 2600,
            label: {
              emphasis: mylabel
            }
          }
        ]
      });
    }
  }
}
</script>

<style scope>
</style>