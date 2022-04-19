<template>
  <Card :bordered="false" style="width:300px;margin-bottom: 3%;">
    <p slot="title" align="center">
      {{ reponame }}
    </p>
    <div v-for="(item, key, index) in data">
      <span v-if="item.status && item.status.toLowerCase()=='passed'">
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
          href="javascript:void(0)"
          style="font-size:10px;"
          @click="jumper(item)"
        > {{ key }} </a>
      </span>
      <span v-else-if="item.status && item.status.toLowerCase()=='failed'">
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
          href="javascript:void(0)"
          style="font-size:10px;"
          @click="jumper(item)"
        > {{ key }} </a>
      </span>
      <span v-else-if="item.status && item.status.toLowerCase()=='running'">
        <Icon
          type="ios-loading"
          size="20"
          class="demo-spin-icon-load"
        ></Icon>
        <Tooltip placement="right" width="400">
          <a
            href="javascript:void(0)"
            style="font-size:10px;"
            @click="jumper(item)"
          > {{ key }} </a>
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
      </span>
      <span v-else>
        <Tooltip placement="top" content="未执行">
          <Icon type="ios-alert-outline" size="17"/>
          <span style="font-size:10px;">
            {{ key }}
          </span>
        </Tooltip>
      </span>
      <span style="margin-left: 30%;">
        <span style="color:green;"> {{ 50 }} </span>
        <span> | </span>
        <span style="color:red;" v-if="true"> {{ 2 }} </span>
        <span style="color:green;" v-else=""> {{ 2 }} </span>
      </span>
      <span style="float:right;">
        <a
        href="javascript:void(0)"
        style="font-size:10px;"
        @click="jumper(item)"
        > 日志 </a>
      </span>
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
  }
};
</script>

<style scoped>
</style>