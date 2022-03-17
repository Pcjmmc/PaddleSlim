<template>
  <div style="font-size:10px">
    <Row>
      <Card :bordered="false" style="width:400px">
        <div style="text-align:center">
          <h3>branch / tag</h3>
        </div>
        <div style="text-align:center">
          <Icon type="md-git-branch" />
          <a href="https://github.com/PaddlePaddle/Paddle/tree/develop">
            {{repoInfo.branch}}
          </a>
        </div>
      </Card>
      <Divider type="vertical" style="height:80px" />
      <Card  :bordered="false" style="width:400px">
        <div style="text-align:center">
          <h3>commit</h3>
        </div>
        <div style="text-align:center">
          <Icon type="md-git-commit" />
          <a href="javascript:void(0)" @click="jumper(repoInfo.branch)">
            {{repoInfo.commit}}
          </a> 
        </div>
      </Card>
      <!--
      <Divider type="vertical" style="height:80px" />
      <Card :bordered="false">
        <div style="text-align:center">
          <h3>Auther & Message</h3>
        </div>
        <div style="text-align:center">
          <Icon type="md-person" />
          <label>
            {{repoInfo.auth}}
            {{repoInfo.descrition}}
          </label>
        </div>
      </Card>
      -->
    </Row>
  </div>
</template>
<script>
export default {
  props: ["repoInfo"],
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
    jumper(branch, commit) {
      let _params = {
        branch: branch
      }
      // 根据branch获取commit列表
      const { href } = this.$router.resolve({name: 'CommitDetails', query: _params})
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
