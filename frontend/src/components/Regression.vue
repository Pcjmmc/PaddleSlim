<template>
  <div class="one-fifth-video-col">
    <span> 占位contentXXXXX </span>
  </div>
</template>
<script>

import expandBase from './expandBase.vue';

export default {
  props: ["data"],
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
