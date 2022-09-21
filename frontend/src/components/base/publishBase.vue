<template>
  <div>
    <Card class="center-card-s">
      <Row align="middle">
        <Col :xs="{ span: 18, offset: 0 }">
          <div v-for="(item, key, index) in data" style="margin-top: 0.5%;">
            <Row>
              <span style="display:inline-block;width:60%;float:left;">
                <a
                  href="javascript:void(0)"
                  style="font-size:13px;"
                  @click="showModal(item)"
                > {{ item.tname }} </a>
              </span>
              <span style="display:inline-block;width:40%;float:right;">
                <span style="float:left;width:80%;">
                  <div>
                    <Steps
                      :current="item.test_step"
                      :status="getStatus(item.status)"
                      size="small"
                      @click.native="showModal(item)"
                    >
                      <Step title="编译"></Step>
                      <Step title="验证"></Step>
                    </Steps>
                  </div>
                </span>
                <!--
                <span style="float:right;" v-if="item.log_url">
                  <a
                    href="javascript:void(0)"
                    style="font-size:13px;"
                    @click="jumperLog(item.log_url)"
                  > 日志 </a>
                </span>
                <span style="float:right;" v-else>
                  <a
                    href="javascript:void(0)"
                    style="font-size:13px;"
                  > 日志 </a>
                </span>
                -->
              </span>
            </Row>
            <div v-if="item.showTestModal && (item.log_url || (item.check_info && item.check_info.length > 0))">
              <Row>
                <span style="display:inline-block;width:60%;float:left;">
                </span>
                <span style="display:inline-block;width:40%;float:right;">
                  <span style="float:left;width:69%;">
                    <span style="float:left;margin-left:8%;" v-if="item.log_url">
                      <Icon type="md-return-right"/>
                      <a
                        href="javascript:void(0)"
                        style="font-size:13px;"
                        @click="jumperLog(item.log_url)"
                      > 日志 </a>
                    </span>
                  </span>
                  <span style="float:right;width:31%;" v-if="item.check_info && item.check_info.length > 0">
                    <div v-for="(itm, idx) in item.check_info">
                      <Icon type="md-return-right"/>
                      <Icon
                        type="ios-close"
                        style="color:red;"
                        v-if="itm.status === 'failed'"
                      />
                      <Icon
                        type="ios-checkmark"
                        style="color:green;"
                        v-else-if="itm.status === 'success'"
                      />
                      <Icon
                        type="ios-loading"
                        v-else-if="itm.status === 'running'"
                        class="demo-spin-icon-load"
                      ></Icon>
                      <Icon type="ios-alert-outline" v-else/>
                      <a
                        href="javascript:void(0)"
                        style="font-size:13px;"
                        @click="jumperLog(itm.test_url)"
                      > {{ itm.desc }} </a>
                    </div>
                  </span>
                </span>
              </Row>
            </div>
          </div>
        </Col>
        <Col :xs="{ span: 4, offset: 2 }" align="center">
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
  </div>
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
    showModal(item) {
      // 判断测试任务个数；测试任务可能有多个，show每个测试任务的状态
      item.showTestModal = !item.showTestModal;
    },
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
.demo-spin-icon-load{
  animation: ani-demo-spin 1s linear infinite;
}
</style>