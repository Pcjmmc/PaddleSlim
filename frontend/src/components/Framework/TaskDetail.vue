<template>
  <div>
    <div style="margin-top: 2%">
      <Form
      :label-width="75"
      >
        <Row :gutter="16">
          <Col span="8">
            <div style="width: 400px;margin-right: 2%">
              <FormItem label="任务id:" prop="searchId">
                <Input v-model="searchId" placeholder="输入id"/>
              </FormItem>
            </div>
          </Col>
          <Col span="8">
            <div style="margin-right: 2%">
              <Button
                type="primary"
                shape="circle"
                icon="ios-search"
                @click="searchData"
              >Search</Button>
            </div>
          </Col>
        </Row>
      </Form>
    </div>
    <div v-if="datas.length > 0 ">
      <h3 class="center-sss">任务列表</h3>
      <Collapse
        v-for="(item, index) in datas"
        :key="index"
        class="center-card-s"
        v-on:on-change="getDetail(item.id)"
      >
        <Panel :key="item.id">
          <span style="margin-right: 1%;">
            任务ID: {{ item.id }}
          </span>
          <span style="margin-right: 1%">
            任务名: {{ item.description }}
          </span>
          <span style="display:inline-block;width:350px;float:right;margin-right:2%;">
            <span style="float:left;">
              状态:
              <Button
                type="success"
                style="width:80px"
                v-if="item.status==='done'"
              >{{ item.status }}</Button>
              <Button
                type="error"
                style="width:80px"
                v-else-if="item.status==='error'"
              >{{ item.status }}</Button>
              <Button
                type="info"
                style="width:80px"
                v-else-if="item.status==='running'"
              >{{ item.status }}</Button>
              <Button
                type="warning"
                style="width:80px"
                v-else
              >{{ item.status }}</Button>
            </span>
            <span style="float:right;">
              创建时间: {{ item.create_time }}
            </span>
          </span>
          <!--
          <span
            :key="val"
            v-for="(val, key, idx) in JSON.parse(item.mission)"
          >
            <Button
              shape="circle"
              class="one-fifth-video-col"
            >
              <p> {{ key }} </p>
            </Button>
          </span>
          -->
          <p slot="content">
            <detail :ref="item.id"></detail>
          </p>
        </Panel>
      </Collapse>
      <Page
        :total="total"
        simple
        size="small"
        style="text-align: center;"
        :current="parseInt(search.page_index)"
        :page-size="parseInt(search.limit)"
        v-on:on-change="pageChange"
        >
      </Page>
    </div>
  </div>
</template>

<script>
import { FrameWorkJobListUrl } from '../../api/url.js';
import api from '../../api/index';
import { randomColor } from '../../util/help.js';
import { ColorList } from '../../util/common.js';
import Detail from './Detail.vue';

export default {
  name: 'PaddleDetail',
  data: function () {
    return {
      value1: {},
      branch: [
      ],
      cuda: [
      ],
      os: [
      ],
      python: [
      ],
      testType: [
      ],
      createData: {},
      datas: [],
      total: 0,
      searchId: '',
      search: {
        page_index: 1,
        limit: 15
      }
    };
  },
  watch: {
  },
  mounted: function () {
    this.initData();
    this.getDatas();
  },
  components: {
    Detail
  },
  computed: {
  },
  methods: {
    initData() {
      this.searchId = '';
    },
    setColor() {
      return randomColor(ColorList);
    },
    async getDatas(search_id) {
      let params = {
        page_index: this.search.page_index,
        limit: this.search.limit
      };
      if (search_id) {
        params.id = search_id;
      }
      const {code, data, msg, all_count} = await api.get(FrameWorkJobListUrl, params);
      if (parseInt(code, 10) === 200) {
        this.datas = data;
        this.total = all_count;
      } else {
        this.datas = [];
        this.$Message.error({
          content: '请求出错: ' + msg,
          duration: 30,
          closable: true
        });
      }
    },
    async getDetail(key) {
      this.$refs[key][0].getDetails(key);
    },
    // handleReset(auto) {
    //   this.setCreateModal = false;
    //   this.$refs.child.handleClose();
    // },
    // handelUpdateSubmit(auto) {
    //   // console.log('调用子组件的提交');
    //   this.$refs.child.handleSummit();
    // },
    async pageChange(pageNum) {
      this.search.page_index = pageNum;
      await this.getDatas(this.searchId);
    },
    async searchData() {
      this.search.page_index = 1;
      await this.getDatas(this.searchId);
    }
  }
};
</script>

<style scoped>
.center-card-s {
  width: 96%;
  margin-left: 1%;
  margin-right: 2%;
  max-height: 600px;
  overflow:auto;
  font-size: 16px;
  color:lightslategrey
}
.center-sss {
  width: 96%;
  margin-left: 1%;
  margin-right: 2%;
  max-height: 600px;
  overflow:auto;
  font-size: 18px;
  color:lightslategrey
}
.one-fifth-video-col {
  margin-right: 2px;
  margin-left: 2px;
  margin-bottom: 2px;
  margin-top: 2px;
}
</style>

<style>
</style>