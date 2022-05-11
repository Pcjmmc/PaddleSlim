<template>
  <Card :bordered="false" style="width:300px;margin-bottom: 3%;">
    <p slot="title" align="center">
      {{ reponame }}
    </p>
    <div v-for="(item, key, index) in data">
      <div v-for="child, idx in item">
        <Row align="middle">
          <Col
            :xs="{ span: 11 }"
            v-if="child.status && child.status.toLowerCase()=='passed'"
          >
            <i-circle
              :percent="100"
              stroke-color="#5cb85c"
              :size="15"
            >
              <Icon
                type="ios-checkmark"
                size="10"
                style="color:#5cb85c"
              ></Icon>
            </i-circle>
            <a
              v-if="item.length > 1"
              href="javascript:void(0)"
              style="font-size:13px;"
              @click="jumper(child)"
            > {{ key + '_' + idx }} </a>
            <a
              v-else
              href="javascript:void(0)"
              style="font-size:13px;"
              @click="jumper(child)"
            > {{ key }} </a>
          </Col>
          <Col
            :xs="{ span: 11 }"
            v-else-if="child.status && child.status.toLowerCase()=='failed'"
          >
            <i-circle
              :percent="100"
              stroke-color="#ff5500"
              :size="15"
            >
              <Icon
                type="ios-close"
                size="10"
                style="color:#ff5500"
              ></Icon>
            </i-circle>
            <a
              v-if="item.length > 1"
              href="javascript:void(0)"
              style="font-size:13px;"
              @click="jumper(child)"
            > {{ key + '_' + idx }} </a>
            <a
              v-else
              href="javascript:void(0)"
              style="font-size:13px;"
              @click="jumper(child)"
            > {{ key }} </a>
          </Col>
          <!--
          <Col
            :xs="{ span: 11 }"
            v-else-if="child.status && child.status.toLowerCase()=='running'"
          >
            <Icon
              type="ios-loading"
              size="20"
              class="demo-spin-icon-load"
            ></Icon>
            <Tooltip placement="right" width="400">
              <a
                href="javascript:void(0)"
                style="font-size:13px;"
                @click="jumper(child)"
              > {{ key + '_' + idx }}</a>
              <span
                slot="content"
                data-test="ring-dropdown"
                class="dropdown_40a"
              >
                <div
                  class="BuildDurationAnchor__buildDuration--tx
                  global__font-smaller--2q
                  global__font-lower--3X global__font--1w"
                >
                  <div
                    class="BuildDurationAnchor__wrapper--1R
                    global__font-smaller--2q
                    global__font-lower--3X global__font--1w"
                  >
                    <span class="BuildDurationAnchor__text--2P">{{ item.left_time }}</span>
                    <div class="BuildDurationAnchor__progress--2J" style="width: 19%;">
                      <div style="width: 526.316%;">
                        <span class="BuildDurationAnchor__text--2P">{{ item.left_time }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </span>
            </Tooltip>
          </Col>
          -->
          <Col
            v-else
            :xs="{ span: 11 }"
          >
            <Tooltip placement="top" content="未执行">
              <Icon type="ios-alert-outline" size="17"/>
              <span
                v-if="item.length > 1"
                style="font-size:13px;"
              >
                {{ key + '_' + idx }}
              </span>
              <span
                v-else
                style="font-size:13px;"
              >
                {{ key }}
              </span>
            </Tooltip>
          </Col>
          <Col :xs="{ span: 6 }">
            <span v-if="child.total > 0" style="color:green;font-size:13px;"> {{ child.total }} </span>
            <span v-else style="color:red;font-size:13px;"> {{ child.total }} </span>
            <span> | </span>
            <span
              style="color:red;font-size:13px;"
              v-if="child.failed_num > 0 || child.total == 0"
            > {{ child.failed_num }} </span>
            <span style="color:green;font-size:13px;" v-else> {{ child.failed_num }} </span>
          </Col>
          <Col :xs="{ span: 3 }">
            <a
            href="javascript:void(0)"
            style="font-size:13px;"
            @click="jumperLog(child)"
            > 日志 </a>
          </Col>
        </Row>
      </div>
    </div>
  </Card>
</template>

<script>
export default {
  name: 'baseCard',
  props: {
    'reponame': {
      type: [String],
      default: function () {
        return '';
      }
    },
    'data': {
      type: Object
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
    jumper(item) {
      let _params = {};
      _params = Object.assign(_params, item);
      let detail_name = 'ApiDetails';
      if (item.task_type === 'model') {
        detail_name = 'model';
      } else if (item.task_type === 'lite') {
        detail_name = 'lite';
      }
      const { href } = this.$router.resolve({name: detail_name, query: _params});
      window.open(href, '_blank');
    },
    jumperLog(item) {
    }
  }
};
</script>

<style scoped>
</style>