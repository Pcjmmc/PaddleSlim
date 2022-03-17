<template>
  <div class="one-fifth-video-col">
    <Row type="flex" justify="space-between">
      <Col span="11" v-for="(item, key, index) in data" :key="key">
        <expandBase v-if="item"
          :platform="item.platform"
          :data="item.data"
          :index="index"
          :tag="tag"
          :versionId="versionId"
          :versionName="versionName">
        </expandBase>
      </Col>
    </Row>
  </div>
</template>
<script>

import expandBase from './expandBase.vue';

export default {
  props: ["data", "tag", "versionId", "versionName"],
  data: function () {
    return {
    }
  },
  methods: {
    setColor(status) {
      let _status = status.toLowerCase();
      switch (_status) {
        case 'pass':
          return 'green';
        case 'warning':
          return 'yellow';
        default:
          return 'red';
      }
    }
  },
  components: {
    expandBase
  },
  mounted: function () {
    console.log("data", this.data)
  }
};
</script>

<style scoped>
  .one-fifth-video-col {
    margin-right: 2%;
    margin-left: 2%;
    margin-bottom: 2%;
  }
</style>
