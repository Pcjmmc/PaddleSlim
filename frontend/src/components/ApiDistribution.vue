<template>
  <!--为echarts准备一个具备大小的容器dom-->
  <div id="main1" style="width: 500px;height: 350px;"></div>
</template>
<script>
import echarts from 'echarts'
export default {
  name: '',
  data () {
    return {
      charts: '',
      opinion: ['成功', '失败', '跳过'],
      opinionData: [
        {value: 100, name: '成功', label: {show: true, formatter: '{d}%', position: 'outer', fontSize: 10}},
        {value: 10, name: '失败', label: {show: true, formatter: '{d}%', position: 'outer', fontSize: 10}},
        {value: 3, name: '跳过', label: {show: true, formatter: '{d}%', position: 'outer', fontSize: 10}}
      ]
    }
  },
  methods: {
    drawPie(id) {
      this.charts = echarts.init(document.getElementById(id))
      this.charts.setOption({
        graphic: {
          type: "text",
          left: "center",
          top: "center",
          style: {
              // 数据总量
              text: 100 + 10 + 3,
              textAlign: "center",
              fill: "black",
              fontSize: 30
          }
        },
        title: {
        text: 'Api测试结果分布',
        left: 'center'
        },
        legend: {
          orient: 'vertical',
          left: '10',
          data: this.opinion
        },
        series: [
          {
            name: 'Api测试分布',
            type: 'pie',
            color: ['green', 'red', 'grey'],
            radius: ['50%', '70%'],
            avoidLabelOverlap: false,
            labelLine: {
              show: true
            },
            data: this.opinionData,
            emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          }
        }
        ]
      })
    }
  },
  mounted() {
    this.$nextTick(function() {
      this.drawPie('main1')
    })
  }
}
</script>
<style scoped>
    * {
        margin: 0;
        padding: 0;
        list-style: none;
    }
</style>