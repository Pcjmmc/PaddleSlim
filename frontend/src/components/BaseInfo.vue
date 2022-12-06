<template>
  <div style="font-size:14px">
    <Row>
      <Col span="6">
        <div style="text-align:center">
          <p style="font-size:14px">branch / tag</p>
        </div>
        <div style="text-align:center">
          <Icon type="md-git-branch" />
          <a href="javascript:void(0)" @click="jumperPaddle(repoinfo.branch)">
            {{ repoinfo.branch }}
          </a>
        </div>
      </Col>
      <Divider type="vertical" style="height:40px"/>
      <Col span="8">
        <div style="text-align:center">
          <p style="font-size:14px">commit</p>
        </div>
        <div style="text-align:center;font-size:14px">
          <Icon type="md-git-commit" />
          <a href="javascript:void(0)" @click="jumper(repoinfo.name)">
            {{ repoinfo.commit }}
          </a> 
        </div>
      </Col>
      <Divider type="vertical" style="height:40px"/>
      <Col span="9">
        <div style="text-align:center">
          <p style="font-size:14px">任务成功占比</p>
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
      </Col>
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

</style>
