<template>
  <div>
    <div
      v-for="(item, index) in data"
      class="one-fifth-video-col"
    >
      <publishBase
        v-if="item"
        :system="item.system"
        :data="item.data"
      >
      </publishBase>
    </div>
  </div>
</template>
<script>

import publishBase from '../Base/publishBase.vue';

export default {
  props: {
    data: {
      type: [Array],
      default: function () {
        return [];
      }
    }
  },
  data: function () {
    return {
    };
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
    publishBase
  },
  mounted: function () {
    // console.log('secondtype', this.tabname);
    // console.log('this data', this.data);
  }
};
</script>

<style scoped>
  .one-fifth-video-col {
    margin-right: 2%;
    margin-left: 2%;
    margin-bottom: 0.5%;
  }
</style>
