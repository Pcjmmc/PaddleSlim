<template>
  <div>
    <i-circle
        :percent="percent"
        :size="30"
        :stroke-width="8"
    >
        <span
            class="demo-i-circle-inner"
            style="font-size:12px"
        >{{ percent }}%</span>
    </i-circle>
  </div>
</template>
<script>
export default {
  name: 'cirlceBase',
  props: {
    'percent': {
      type: [Number],
      default: 0
    }
  }
};
</script>