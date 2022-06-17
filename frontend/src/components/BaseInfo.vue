<template>
  <div style="font-size:15px">
    <Row type="flex" justify="start">
      <div class="branch">
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
      <Divider type="vertical" style="height:40px"/>
      <div class="commit">
        <div style="text-align:center">
          <h3>commit</h3>
        </div>
        <div style="text-align:center;font-size:13px">
          <Icon type="md-git-commit" />
          <a href="javascript:void(0)" @click="jumper(repoinfo.name)">
            {{ repoinfo.commit }}
          </a> 
        </div>
      </div>
      <Divider type="vertical" style="height:40px"/>
      <div class="abc">
        <div style="text-align:center">
          <h3>任务成功占比</h3>
        </div>
        <div style="text-align:center">
         <Progress
          :percent="processdata.percent"
          :stroke-width="15"
          status="active"
          text-inside
        >
        </Progress>
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
      switch (status.toLowerCase()) {
        case 'passed':
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
      const { href } = this.$router.resolve({name: 'CommitDetails'});
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
.abc{ height:40px; margin:0 auto}
@media screen and (min-width: 1501px) {
.abc {
  width: 800px}
}
@media screen and (max-width: 1500px) {
.abc {
  width: 600px}
}
.commit{ height:40px; margin:0 auto}
@media screen and (min-width: 1501px) {
.commit {
  width: 500px;}
}
@media screen and (max-width: 1500px) {
.commit {
  width: 400px;}
}
.branch{ height:40px; margin:0 auto}
@media screen and (min-width: 1501px) {
.branch {
  width: 300px;}
}
@media screen and (max-width: 1500px) {
.branch {
  width: 200px;}
}
</style>
