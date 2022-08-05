<template>
  <div>
    <Row justify="center">
        <Col :xs="xs">
            <span style="color:red;" v-if="failed > 0 || total == 0"> {{ total }} </span>
            <span v-else style="color:green;"> {{ total }} </span>
        </Col>
        <Col :xs="0.5">
            <span> | </span>
        </Col>
        <Col :xs="xs" v-if="needSucceed">
          <span style="color:green;"> {{ succeed }} </span>
        </Col>
        <Col :xs="0.5" v-if="needSucceed">
            <span> | </span>
        </Col>
        <Col :xs="xs">
          <span style="color:red;" v-if="failed > 0 || total == 0"> {{ failed }} </span>
          <span style="color:green;" v-else> {{ failed }} </span>
        </Col>
    </Row>
  </div>
</template>
<script>
export default {
  name: 'CaseBase',
  props: {
    xs: {
      type: [Number],
      default: 4
    },
    total: {
      type: [Number],
      default: 0
    },
    succeed: {
      type: [Number],
      default: 0
    },
    needSucceed: {
      type: [Boolean],
      default: false
    },
    failed: {
      type: [Number],
      default: 0
    }
  }
};
</script>