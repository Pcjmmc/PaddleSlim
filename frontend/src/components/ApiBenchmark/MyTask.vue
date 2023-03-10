<template>
  <div class="center-card-s">
    <div style="margin-top: 2%">
      <div style="cursor: pointer">
        任务状态：
        <span v-for="(item, index) in tags">
          <span v-if="item.checked">
            <Tag
              :checked="item.checked"
              color="primary"
              v-on:on-change="changeTagStatus(item)"
            >
              <p style="font-size: 14px">{{ item.desc }}</p>
            </Tag>
          </span>
          <span v-else>
            <Tag
              checkable
              :checked="item.checked"
              color="primary"
              v-on:on-change="changeTagStatus(item)"
            >
              <p style="font-size: 14px">{{ item.desc }}</p>
            </Tag>
          </span>
        </span>
      </div>
    </div>
    <div style="margin-top: 2%">
      <span>
        创建时间:
        <DatePicker
          type="daterange"
          placement="bottom-end"
          placeholder=" 开始时间 ～ 结束时间 "
          style="width: 30%"
        ></DatePicker>
      </span>
    </div>
    <div style="margin-top: 2%">
      <div>
        任务ID:
        <Input placeholder="任务ID" style="width: 150px"></Input>
        任务名:
        <Input placeholder="任务名" style="width: 300px"></Input>
        <Button
          class="btn-success"
          shape="circle"
          icon="ios-search"
        >
        Search
        </Button>
      </div>
      <div style="text-align: right">
        <Button
          icon="md-add"
          class="btn-success"
          @click="createNewJob"
        >
          新建测试任务
        </Button>
      </div>
    </div>
    <div style="margin-top: 2%">
      <div class="left" style="margin-top: 2%">
        <Table :columns="columns" :data="content"></Table>
        <Page
          :total="total"
          :current="parseInt(search.page)"
          :page-size="parseInt(search.pagesize)"
          size="small"
          style="text-align: center"
        >
        </Page>
      </div>
    </div>
    <Modal
      v-model="showModa"
      title="创建测试任务"
      width="70%"
    >
      <benchmark-exec> </benchmark-exec>
      <div slot="footer">
        <Button
          type="text"
          @click="handleReset"
        >
          重置
        </Button>
        <Button
          type="primary"
          @click="handleSubmit"
        >
          提交
        </Button>
      </div>
    </Modal>
  </div>
</template>

<script>
import BenchmarkExec from './BenchmarkExec.vue';
export default {
  name: 'ApiBenchmarkExec',
  data: function () {
    return {
      showModa: false,
      tags: [
        {
          id: 'all',
          desc: '全部',
          checked: true,
        },
        {
          id: 'running',
          desc: '运行中',
          checked: false,
        },
        {
          id: 'done',
          desc: '已完成',
          checked: false,
        },
        {
          id: 'error',
          desc: '异常',
          checked: false,
        },
      ],
      columns: [
        {
          title: '任务ID',
          key: 'id',
          align: 'center',
          fixed: 'left',
          minWidth: 100,
        },
        {
          title: '任务名',
          key: 'comment',
          align: 'center',
          fixed: 'left',
          minWidth: 100,
        },
        {
          title: 'Framework',
          key: 'framework',
          align: 'center',
          fixed: 'left',
          minWidth: 120,
        },
        {
          title: '版本详情',
          key: 'version',
          align: 'center',
          fixed: 'left',
          minWidth: 100,
        },
        {
          title: 'Python',
          key: 'python',
          align: 'center',
          fixed: 'left',
          minWidth: 100,
        },
        {
          title: 'OS',
          key: 'os',
          align: 'center',
          fixed: 'left',
          minWidth: 100,
        },
        {
          title: 'Place',
          key: 'place',
          align: 'center',
          fixed: 'left',
          minWidth: 100,
        },
        {
          title: 'CUDA',
          key: 'cuda',
          align: 'center',
          fixed: 'left',
          minWidth: 100,
        },
        {
          title: '反向',
          key: 'enable_backward',
          align: 'center',
          fixed: 'left',
          minWidth: 100,
        },
        {
          title: '配置详情',
          key: 'config',
          align: 'center',
          fixed: 'left',
          minWidth: 100,
        },
        {
          title: '任务状态',
          key: 'status',
          align: 'center',
          fixed: 'left',
          minWidth: 100,
        },
        {
          title: '创建时间',
          key: 'create_time',
          align: 'center',
          fixed: 'left',
          minWidth: 100,
        },
        {
          title: '报告',
          key: 'detail',
          align: 'center',
          fixed: 'right',
          minWidth: 100,
          render: (h, params) => {
            return h('div', [
              h(
                'Button',
                {
                  props: {
                    type: 'info',
                  },
                  on: {
                    click: () => {
                      this.handleDetail(params.row);
                    },
                  },
                },
                '查看报告'
              ),
            ]);
          },
        },
      ],
      content: [
        {
          id: 234,
          comment: 'LeLes Test',
          framework: 'paddle',
          version: 'https://ssss',
          python: '3.8',
          os: 'Linux',
          place: 'GPU',
          cuda: 'v11.6',
          enable_backward: '是',
          config: '默认',
          status: '运行中',
          create_time: '2023.03.04 20.01',
        },
      ],
      search: {
        page: '',
        total: '',
        pagesize: '',
      },
    };
  },
  methods: {
    async searchByfilter() {
      this.search.page = 1;
      await this.searchData();
    },
    async changeTagStatus(item) {
      this.$set(item, 'checked', true);
      // 将选中以外的设置成false
      for (let i = 0; i < this.tags.length; i++) {
        let id = this.tags[i].id;
        if (id !== item.id) {
          this.tags[i].checked = false;
        } else {
          this.$set(this.tags[i], 'checked', true);
          this.tags[i].checked = true;
          this.search.status = this.tags[i].id;
        }
      }
      await this.searchByfilter();
    },
    async createNewJob() {
      this.showModa = true;
    },
  },
  components: { BenchmarkExec },
};
</script>

<style scoped>
.btn-success {
  color: #fff;
  background-color: #67c23a;
  border-color: #67c23a;
}
.center-card-s {
  margin-left: 1%;
  margin-right: 1%;
  font-size: 14px;
  color: lightslategrey;
}
</style>
