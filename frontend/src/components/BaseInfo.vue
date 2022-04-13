<template>
  <div style="font-size:8px">
    <Row type="flex" justify="start">
      <div style="width:600px;height:40px;">
        <div style="text-align:center">
         <Progress
          :percent="processdata.percent"
          :stroke-width="15"
          status="active"
          text-inside
        >
        </Progress>
        </div>
        <div style="text-align:center;margin-top: 1%">
          <h5>任务成功占比</h5>
        </div>
      </div>
      <Divider type="vertical" style="height:35px"/>
      <div style="width:200px;height:40px;">
        <div style="text-align:center">
          <h3>branch / tag</h3>
        </div>
        <div style="text-align:center">
          <Icon type="md-git-branch" />
          <a href="javascript:void(0)" @click="jumperPaddle(repoinfo.branch)">
            {{ repoinfo.branch }}
          </a>
        </div>
      </div>
      <Divider type="vertical" style="height:35px"/>
      <div style="width:300px;height:40px;">
        <div style="text-align:center">
          <h3>commit</h3>
        </div>
        <div style="text-align:center">
          <Icon type="md-git-commit" />
          <a href="javascript:void(0)" @click="jumper(repoinfo.name)">
            {{ repoinfo.commit }}
          </a> 
        </div>
      </div>
    </Row>
  </div>
</template>
<script>
export default {
  props: {
    repoinfo: {
      type: Object,
      default: null
    },
    processdata: {
      type: Object,
      default: null
    }
  },
  methods: {
    setColor(status) {
      switch (status) {
        case 'Pass':
          return 'green';
        case 'warning':
          return 'yellow';
        default:
          return 'red';
      }
    },
    jumper(name) {
      let _params = {
        version: name
      }
      // 根据branch获取commit列表
      const { href } = this.$router.resolve({name: 'CommitDetails', query: _params})
      window.open(href, '_blank');
    },
    jumperPaddle(branch) {
      let href = 'https://github.com/PaddlePaddle/Paddle/tree/' + branch;
      window.open(href, '_blank');
    }
  },
  mounted () {
  }
};
</script>

<style scoped>
.video-header {
  display: flex;
  flex-wrap: wrap;
  margin-bottom: 6px;
}
</style>
