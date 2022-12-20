<template>
  <div style="text-align:center;width:auto;">
    <div>
      <p slot="title" style="font-size:10px;">
        子卡片
      </p>
      <div
        :key="index"
        :value="item"
        v-for="(item, index) in child"
      >
        <a href="javascript:void(0)" @click="jumper(item)">
          {{ item }}
        </a>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: 'baseChild',
  props: {
    'child': {
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
    jumper(key) {
      let url = `https://console.cloud.baidu-int.com/devops/icafe/issue/DLTP-${key}/show`;
      window.open(url, '_blank');
    }
  }
};
</script>
