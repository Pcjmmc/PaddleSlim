<template>
  <Card :bordered="false" style="width:300px;margin-bottom: 3%;">
    <p slot="title" align="center">
      {{ reponame }}
    </p>
    <div v-for="(item, key, index) in data">
      <div v-for="child, idx in item">
        <Row align="middle">
          <Col
            :xs="{ span: 15 }"
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
            > {{ key + '_' + child.show_name }} </a>
            <a
              v-else-if="child.show_name !== null && child.show_name !== ''"
              href="javascript:void(0)"
              style="font-size:13px;"
              @click="jumper(child)"
            > {{ key + '_' + child.show_name }} </a>
            <a
              v-else
              href="javascript:void(0)"
              style="font-size:13px;"
              @click="jumper(child)"
            > {{ key }} </a>
            <Tooltip placement="top">
              <Icon
                custom="iconfont icon-warning"
                v-if="checkExpired(latestcommittime, child.commit_time)"
              />
                <div slot="content">
                <p>距离最新的commit超过3天</p>
              </div>
            </Tooltip>
          </Col>
          <Col
            :xs="{ span: 15 }"
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
            > {{ key + '_' + child.show_name }} </a>
            <a
              v-else-if="child.show_name !== null && child.show_name !== ''"
              href="javascript:void(0)"
              style="font-size:13px;"
              @click="jumper(child)"
            > {{ key + '_' + child.show_name }} </a>
            <a
              v-else
              href="javascript:void(0)"
              style="font-size:13px;"
              @click="jumper(child)"
            > {{ key }} </a>
            <Tooltip placement="top">
              <Icon
                custom="iconfont icon-warning"
                v-if="checkExpired(latestcommittime, child.commit_time)"
              />
                <div slot="content">
                <p>距离最新的commit超过3天</p>
              </div>
            </Tooltip>
          </Col>
          <!--
          <Col
            :xs="{ span: 15 }"
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
            :xs="{ span: 15 }"
          >
            <Tooltip placement="top" content="未执行">
              <Icon type="ios-alert-outline" size="17"/>
              <span
                v-if="item.length > 1"
                style="font-size:13px;"
              >
                {{ key + '_' + child.show_name }}
              </span>
              <span
                v-else-if="child.show_name !== null && child.show_name !== ''"
                style="font-size:13px;"
              >
                {{ key + '_' + child.show_name }}
              </span>
              <span
                v-else
                style="font-size:13px;"
              >
                {{ key }}
              </span>
            </Tooltip>
          </Col>
          <Col :xs="{ span: 2 }">
            <span v-if="child.total > 0" style="color:green;font-size:13px;"> {{ child.total }} </span>
            <span v-else style="color:red;font-size:13px;"> {{ child.total }} </span>
          </Col>
          <Col :xs="{ span: 1 }">
            <span> | </span>
          </Col>
          <Col :xs="{ span: 2 }">
            <span
              style="color:red;font-size:13px;"
              v-if="child.failed_num > 0 || child.total == 0"
            > {{ child.failed_num }} </span>
            <span style="color:green;font-size:13px;" v-else> {{ child.failed_num }} </span>
          </Col>
          <Col :xs="{ span: 3 }">
            <a
            href="javascript:void(0)"
            @click="jumperLog(child.log_url)"
            style="font-size:13px;"
            > 日志 </a>
          </Col>
        </Row>
      </div>
    </div>
  </Card>
</template>

<script>
import { isExpired } from '../../util/help.js';
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
    },
    'latestcommittime': {
      type: [Number],
      default: function () {
        return null;
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
    checkExpired(time1, time2) {
      return isExpired(time1, time2);
    },
    jumper(item) {
      let _params = {
        task_type: item.task_type,
        tid: item.tid,
        build_id: item.build_id,
        secondary_type: item.secondary_type,
        status: item.status,
        exit_code: item.exit_code,
        repo: item.repo,
        branch: item.branch,
        commit_id: item.commit_id,
        tname: item.tname,
        reponame: item.reponame,
        created: item.created,
        commit_time: item.commit_time
      };
      // _params = Object.assign(_params, item);
      let detail_name = '';
      if (item.reponame === 'Paddle2ONNX' || item.reponame === 'PaddleHub') {
        detail_name = 'FuncDetail';
      } else if (item.task_type === 'model') {
        detail_name = 'model';
      } else if (item.task_type === 'dist') {
        // 如果二级分类是api的则跳转api详情页；否则按模型汇聚
        if (item.secondary_type.toLowerCase().includes('api')) {
          detail_name = 'FuncDetail';
        } else {
          return;
        }
      }
      const { href } = this.$router.resolve({name: detail_name, query: _params});
      window.open(href, '_blank');
    },
    jumperLog(url) {
    window.open(url, '_blank');
  }
  }
};
</script>

<style scoped>
@import "../../assets/font_m3t1ua85h0a/iconfont.css";
</style>