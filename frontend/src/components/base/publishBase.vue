<template>
  <Card class="center-card-s">
    <Row align="middle">
      <Col :xs="{ span: 17, offset: 0 }">
        <div v-for="(item, key, index) in data" style="margin-top: 1%;">
          <span style="float:left;">
            <a
              href="javascript:void(0)"
              style="font-size:13px;"
            > {{ item.tname }} </a>
          </span>
          <span style="display:inline-block;width:350px;float:right;">
            <span style="float:left;">
              <div style="width:300px;">
                <Steps
                  :current="item.test_step"
                  :status="getStatus(item.status)"
                  size="small"
                >
                  <Step title="编译"></Step>
                  <Step title="验证"></Step>
                </Steps>
              </div>
            </span>
            <span style="float:right;">
              <a
                href="javascript:void(0)"
                style="font-size:13px;"
                @click="jumperLog(item.log_url)"
              > 日志 </a>
            </span>
          </span>
        </div>
      </Col>
      <Col :xs="{ span: 4, offset: 3 }" align="center">
        <div class="one-fifth-video-col">
          <div v-if="system.includes('Windows')">
            <Icon type="logo-windows" size="50"> </Icon>
           </div>
          <div v-else-if="system.includes('Mac')">
            <Icon type="logo-apple" size="50"> </Icon>
          </div>
          <div v-else>
            <Icon type="logo-tux" size="50"> </Icon>
          </div>
          <h4>{{ system }}</h4>
        </div>
      </Col>
    </Row>
  </Card>
</template>

<script>

export default {
  name: 'publishBase',
  props: {
    'system': {
      type: [String],
      default: function () {
        return '';
      }
    },
    'data': {
      type: [Array],
      default: function () {
        return [];
      }
    },
    'index': {
      type: [Number],
      default: function () {
        return 0;
      }
    }
  },
  data: function () {
    return {
    };
  },
  mounted: function () {
  },
  components: {
  },
  computed: {
  },
  methods: {
    jumperLog(url) {
      window.open(url, '_blank');
    },
    getStatus(status) {
      let res = '';
      if (!status) {
        return null;
      } else {
        switch (status.toLowerCase()) {
          case 'running':
            res = 'process';
            break;
          case 'success':
            res = 'finish';
            break;
          case 'failed':
            res = 'error';
            break;
          default:
            res = 'wait';
        }
      }
      return res;
    }
  }
};
</script>

<style scoped>
.center-card-s {
    width: 100%;
    max-height: 600px;
    overflow:auto;
    border-color:green;
}
.one-fifth-video-col {
  margin-right: 2%;
  margin-left: 2%;
  margin-bottom: 2%;
  margin-top: 2%;
}
</style>