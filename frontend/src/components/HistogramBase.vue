<template>
  <div>
    <div id="main1" style="width: 500px;height: 350px;"></div>
  </div>
</template>
<script>
  import echarts from 'echarts'
  export default {
    name: '',
    props: ["xData", "count"],
    data () {
      return {
      }
    },
    methods: {
      drawPie(id) {
        this.charts = echarts.init(document.getElementById(id));
        this.charts.setOption(
          {
            title: {
              'text': 'bug 修复状态分布'
            },
            tooltip: {},
            legend: {
              data: ['卡片数']
            },
            xAxis: {
              data: this.xData
            },
            yAxis: {},
            series: [{
              name: 'bug数',
              type: 'bar',
              barWidth: '30%',
              data: this.count,
              itemStyle: {
                normal: {
                  color: function(params) {
                    var colorList = ['#C1232B', '#B5C334', '#FCCE10', '#E87C25', '#27727B', '#FE8463', '#9BCA63', '#FAD860', '#F3A43B', '#60C0DD', '#D7504B', '#C6E579', '#F4E001', '#F0805A', '#26C0C0'];
                    return colorList[params.dataIndex]
                  }
                },
                emphasis: {
                  // 阴影模糊系数
                  shadowBlur: 10,
                  // 属性设置或返回形状与阴影的水平距离,或称X轴偏移量
                  shadowOffsetX: 0,
                  shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
              }
            }]
          }
        )
      }
    },
    // 调用
    mounted() {
      this.$nextTick(function() {
        this.drawPie('main1');
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