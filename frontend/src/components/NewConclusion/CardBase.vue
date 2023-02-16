<template>
  <div style="margin-left: 1%;">
    <div>
      关联卡片列表:
      <Form style="margin-left: 2%;">
       <div v-for="(item, key, index) in icafes" :key="index" v-if="item.length > 0 ">
          {{ key }}
          <div style="margin-left: 1%;">
            <Row v-for="(itm, ids) in item" :key="ids">
              <Col span="24">
                <Form-item prop="title">
                  <span>
                    <a href="item.url">{{ itm.title }}
                    </a>
                    <span>@ {{ itm.owner }}</span>
                  </span>
                </Form-item>
              </Col>
            </Row>
          </div>
        </div>
      </Form>
    </div>
  </div>
</template>

<script>

export default {
  name: 'SummaryBase',
  props: {
    icafes: {
      type: [Object],
      default: function () {
        return {};
      }
    }
  },
  data: function () {
    return {
    };
  },
  watch: {
  },
  mounted: function () {
  },
  components: {
  },
  methods: {
  }
};
</script>

<style scoped>
.center-card-s {
  width: 100%;
  max-height: 600px;
  overflow: auto;
  margin-bottom: 1%
}
.all-line-row {
  margin-top: 1%;
  margin-bottom: 1%;
  margin-left: 1%;
  margin-right: 1%;
  font-size:14px;
}
.btn-success {
  color: #fff;
  background-color: #67c23a;
  border-color: #67c23a;
}
.ivu-form-item{
  margin-bottom: 6px;
  font-size: 14px;
}
</style>
