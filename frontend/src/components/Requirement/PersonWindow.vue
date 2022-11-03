<template>
  <div>
    <Card class="card-s-new">
      <div>
        <Form
          ref="addForm"
          :model="search"
          :rules="addRules"
          :label-width="75"
          style="width: 85%"
        >
          <Row>
            <Col span="6">
              <FormItem label="IcafeID:" prop="icafeid">
                <Input v-model="search.icafeid" placeholder="输入icafeID"/>
              </FormItem>
            </Col>
            <Col span="8" v-if="user.dName=='TPG质量效能部'">
              <FormItem label="RD:" prop="rdname">
                <Input v-model="search.rdname" placeholder="输入RD名字， 与邮箱前缀一致"/>
              </FormItem>
            </Col>
            <Col span="8" v-else>
              <FormItem label="QA:" prop="qaname">
                <Input v-model="search.qaname" placeholder="输入QA名字， 与邮箱前缀一致"/>
              </FormItem>
            </Col>
            <Col span="6">
              <FormItem label="状态:" prop="staus">
                <Select clearable v-model="search.status">
                  <Option
                    :key="index"
                    :value="item"
                    v-for="(item, index) in statusList"
                  >{{ item }}</Option>
                </Select>
              </FormItem>
            </Col>
            <Col span="2" offset="1">
              <Button type="primary" shape="circle" icon="ios-search">Search</Button>
            </Col>
          </Row>
        </Form>
      </div>
      <Row
        type="flex"
        justify="end"
        style="margin-top: 1%;"
      >
        <Col span="4">
          <Button type="primary" @click="createJob">创建需求</Button>
        </Col>
      </Row>
    </Card>
    <div style="margin-top: 2%;">
      <div v-for="item, index in content">
      </div>
      <Page
        :total="total"
        :current="parseInt(page)"
        :page-size="parseInt(pagesize)"
        size="small"
        style="text-align: center;"
        v-on:on-change="pageChange"
        >
      </Page>
    </div>
  </div>
</template>

<script>

export default {
  name: 'Personal',
  data: function () {
    return {
      total: 0,
      page: 1,
      pagesize: 10,
      user: {
        dName: '研发'
      },
      statusList: [
        '待提测',
        '测试中',
        '测试通过',
        '测试失败'
      ],
      content: [
      ],
      search: {
        icafeid: '',
        qaname: '',
        status: ''
      },
      addRules: {
      }
    };
  },
  watch: {
  },
  mounted: function () {
    this.initData();
    this.getData();
  },
  components: {
  },
  computed: {
  },
  methods: {
    handleReset() {
      this.initData();
    },
    async pageChange(pageNum) {
      this.page = pageNum;
      await this.getData();
    },
    async getData() {
      this.content = [];
    },
    initData() {
      this.search = {
        icafeid: '',
        qaname: '',
        rdname: '',
        status: ''
      };
    },
    handleSummit() {
      this.$refs.addForm.validate((valid) => {
        if (valid) {
          this.createJob();
        } else {
          this.$Message.error('请完善信息');
        }
      });
    },
    async createJob() {
      // 防止有人选了pr，选了分支，又修改了其他值
    }
  }
};
</script>

<style scoped>
.demo-split{
  height: 861px;
  overflow:auto;
}
.demo-split-pane{
  padding: 10px;
  text-align:center
}
.demo-tree {
  width: 100%;
  line-height: 2;
}
.one-fifth-video-col {
  margin-right: 2px;
  margin-left: 2px;
  margin-bottom: 2px;
  margin-top: 2px;
}
.center-card-s {
  width: 96%;
  margin-left: 2%;
  margin-right: 2%;
  max-height: 600px;
  overflow: auto;
  font-size: 15px;
  color: lightslategrey
}
.card-s-new {
  width: 96%;
  margin-left: 2%;
  margin-right: 2%;
  font-size: 15px;
  color: lightslategrey
}
.main {
  color:lightslategrey;
  margin-left: 1%;
  margin-bottom: 2%;
  font-size: 18px;
  align: center;
}
.all-line-row {
  margin-left: 2%;
  margin-right: 2%;
  margin-bottom: 2%;
  margin-top: 1%;
}
</style>

<style>
.ivu-tree ul {
  list-style: none;
  margin: 0;
  padding: 0;
  font-size: 20px;
}
.ivu-tree-title {
  display: inline-block;
  margin: 0;
  padding: 0 4px;
  border-radius: 3px;
  cursor: pointer;
  vertical-align: top;
  -webkit-transition: all .2s ease-in-out;
  transition: all .2s ease-in-out;
}
</style>