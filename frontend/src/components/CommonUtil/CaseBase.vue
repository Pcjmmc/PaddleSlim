<template>
  <div>
    <Row justify="center">
        <Col :xs="4">
            <span style="color:red;" v-if="failed > 0 || total == 0"> {{ total }} </span>
            <span v-else style="color:green;"> {{ total }} </span>
        </Col>
        <Col :xs="0.5">
            <span> | </span>
        </Col>
        <Col :xs="4">
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
    total: {
      type: [Number],
      default: 0
    },
    failed: {
      type: [Number],
      default: 0
    }
  }
}
</script>