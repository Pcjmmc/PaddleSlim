<template>
  <div class="center-welcome">
    <h1>请选择产品列表</h1>
    <Row :gutter="16">
      <Col span="8" v-for="(item, index) in appData" :key="index" class="one-fifth-video-col">
        <Card :bordered="false"  :style="{backgroundColor: randomColor()}">
          <a href="javascript:void(0)" @click="enter(item)"> {{item.name}} </a>
        </Card>
      </Col>
    </Row>
  </div>
</template>

<script>
import paddleImg from '@/assets/paddle.jpeg'
import api from '../../api'
import Cookies from 'js-cookie'

export default {
  name: 'AppStore',
  data () {
    return {
      selectAppId: '',
      selectAppName: '',
      colorList: ['#05FAF7', '#07F0C0', '#55E0AD', '#36E0F0', '#35F0A5', '#A3ED4E'],
      appData: [
        {
          'id': 1,
          'name': '飞桨移核心框架'
        },
        {
          'id': 2,
          'name': '飞桨移动端部署'
        },
        {
          'id': 3,
          'name': 'PaddleClas'
        },
        {
          'id': 4,
          'name': 'PaddleOCR'
        },
        {
          'id': 5,
          'name': 'PaddleSeg'
        },
        {
          'id': 6,
          'name': 'PaddleDetection'
        },
        {
          'id': 7,
          'name': 'PaddleNLP'
        },
        {
          'id': 8,
          'name': 'PaddleGAN'
        },
         {
          'id': 9,
          'name': 'PaddleHub'
        }
      ]
    }
  },
  mounted: function () {
    console.log('select app first');
  },
  methods: {
    enter (item) {
      Cookies.set("appid", item.id);
      Cookies.set("appname", item.name);
      this.$store.commit('changeAppid', item.id);
      this.$store.commit('changeAppName', item.name);
      this.$router.push({path: '/paddle'});
    },
    randomColor() {
      return this.colorList[Math.floor(Math.random() * this.colorList.length)];
    }
  }
}
</script>
<style scoped>
  .center-welcome {
    width: 100%;
    padding-top: 20px;
    text-align: center;
    margin-left: 60px;
  }
  .one-fifth-video-col {
    margin-right: 20px;
    margin-left: 20px;
    margin-top: 20px;
    width: 19%;
    max-width: 293px;
    min-width: 293px;
  }
</style>
