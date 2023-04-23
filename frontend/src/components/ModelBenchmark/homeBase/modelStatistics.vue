<template>
  <div>
    <span>
      <span style="float:left;width:70%">
        <Card style="width: 100%;">
          <font style="font-size: 12px;">
            数据汇总(模型数/配置数)
          </font>
          <div style="text-align:center; margin-top:2%;">
            <Row>
              <Col
                :key="index"
                v-for="(item, index) in datas"
                span="5"
              >
                <div style="margin-bottom: 5%;">
                  <p style="font-size: 16px;">
                    <b>
                      {{ item.model_num }} / {{ item.config_num }}
                    </b>
                  </p>
                  <p style="font-size: 14px;">
                    {{ item.repo_name }}
                  </p>
                </div>
              </Col>
            </Row>
          </div>
        </Card>
      </span>
    </span>
  </div>
</template>
<script>

export default {
  props: {
    datas: {
      type: Array,
      default: function () {
        return [];
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
  computed: {},
  methods: {
  }
};
</script>

<style scoped>
.btn-success {
  color: #fff;
  background-color: #67c23a;
  border-color: #67c23a;
}
</style>