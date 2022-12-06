<template>
  <div class="all-line-row">
    <!--搜索组件-->
    <div>
      <Row
        type="flex"
        justify="left"
        style="margin-top: 1%;"
      >
        <Col span="1">
          <p font-size="14px;">方向:</p>
        </Col>
        <Col span="4" offset="0.1">
          <Select
            clearable
            v-model="search.task_type"
            v-on:on-change="selectTaskType"
          >
            <Option
              :key="index"
              :value="item.key"
              v-for="(item, index) in taskTypeList"
            >{{ item.desc }}</Option>
          </Select>
        </Col>
        <Col span="1" offset="1">
          <p font-size="14px;">任务:</p>
        </Col>
        <Col span="6" offset="0.1">
          <Select
            placeholder="请选择任务"
            v-model="tid"
            clearable
            filterable
            v-on:on-change="selectTask"
          >
            <Option
              :key="item.id"
              :value="item.id"
              v-for="item in taskList"
            >{{ item.tname }}</Option>
          </Select>
        </Col>
        <Col span="1" offset="1">
          <p font-size="14px;">日期:</p>
        </Col>
        <Col span="8" offset="0.1">
          <DatePicker
            type="daterange"
            placement="bottom-end"
            placeholder="选择时间"
            v-model="search.dt"
            style="width:100%"
            v-on:on-change="selectTask"
          ></DatePicker>
        </Col>
      </Row>
    </div>
    <div v-if="builds.length>0">
      <div style="margin-top: 2%;">
        <Table
          border
          :columns="buildColumns"
          :data="builds"
        ></Table>
        <!--分页-->
        <Page
          :total="total"
          :current="parseInt(params.page)"
          :page-size="parseInt(params.size)"
          size="small"
          style="text-align: center;"
          v-on:on-change="pageChange"
        ></Page>
      </div>
    </div>
</div>
</template>

<script>
import api from '../api/index';
import { BuildUrl, JobUrl, ScenesUrl } from '../api/url.js';
import { dateFmt, timestampToTime } from '../util/help.js';

export default {
  data: function () {
    return {
      taskTypeList: [],
      builds: [],
      taskList: [],
      function_case: [],
      tid: '',
      total: 0,
      params: {
        page: 1,
        size: 50
      },
      search: {
        task_type: 'compile',
        dt: [new Date(), new Date()]
      },
      buildColumns: [
        {
          title: 'repo名',
          key: 'repo',
          width: 150,
          align: 'center',
          fixed: 'left'
        },
        {
          title: '分支',
          key: 'branch',
          width: 100,
          align: 'center'
        },
        {
          title: 'commit信息',
          key: 'commit_id',
          width: 350,
          align: 'center'
        },
        {
          title: '编译id',
          align: 'center',
          width: 100,
          render: (h, params) => {
            return h('div', [
              h('a', {
                href: 'javascript:void(0);',
                style: {
                  marginRight: '5px'
                },
                on: {
                  click: () => {
                    this.jumper(params.row);
                  }
                }
              }, params.row.build_id)
            ]);
          }
        },
        {
          title: '执行时间',
          key: 'created',
          width: 200,
          align: 'center',
          render: (h, params) => {
            return h('div', [
              h('p', {
                style: {
                  marginRight: '5px'
                }
              }, this.changeTimestamp(params.row.created))
            ]);
          }
        },
        {
          title: '状态',
          key: 'status',
          align: 'center',
          fixed: 'right'
        }
      ]
    };
  },
  mounted: function () {
    this.getScenesList();
    this.getTaskData();
  },
  components: {
  },
  methods: {
    async selectTaskType() {
      this.getTaskData();
    },
    async selectTask() {
      this.builds = [];
      let _params = {
        begin_time: dateFmt(this.search.dt[0], 'yyyy-MM-dd'),
        end_time: dateFmt(this.search.dt[1], 'yyyy-MM-dd'),
        tid: this.tid,
        page_index: this.params.page,
        limit: this.params.size
      };
      // 有tid再发请求
      if (_params.tid) {
        const { code, data, message, all_count } = await api.get(BuildUrl, _params);
        if (message === 'success' && parseInt(code, 10) === 200) {
          this.builds = data;
          this.total = all_count;
        } else {
          this.$Message.error({content: message || this.$trans('获取编译列表失败'), duration: 5, closable: true});
        }
      } else {
        this.builds = [];
        this.total = 0;
      }
    },
    async getTaskData() {
      let params = {
        task_type: this.search.task_type,
        need_all: true
      };
      const { code, data, message } = await api.get(JobUrl, params);
      if (message === 'success' && parseInt(code, 10) === 200) {
        this.taskList = data;
      } else {
        this.$Message.error({content: message || this.$trans('获取任务列表失败'), duration: 5, closable: true});
      }
    },
    pageChange(pageNum) {
      this.params.page = pageNum;
      this.selectTask();
    },
    getProjectInfo() {
      for (let idx in this.taskList) {
        if (this.taskList.hasOwnProperty(idx)) {
          let item = this.taskList[idx];
          if (item.id === this.tid) {
            return item;
          }
        }
      }
      return null;
    },
    async getScenesList() {
      const {code, data, message} = await api.get(ScenesUrl);
      if (parseInt(code, 10) === 200) {
        this.taskTypeList = data.taskTypeList;
      } else {
        this.taskTypeList = [];
        this.$Message.error({
          content: '请求出错: ' + message,
          duration: 30,
          closable: true
        });
      }
    },
    changeTimestamp(timestamp, offset = 8) {
      let date = timestampToTime(timestamp, offset);
      let dt = dateFmt(date, 'yyyy-MM-dd hh:mm:ss');
      return dt;
    },
    jumper(row) {
      let item = this.getProjectInfo();
      let _params = {
        task_type: item.task_type,
        tid: row.tid,
        build_id: row.build_id,
        secondary_type: item.secondary_type,
        status: row.status,
        exit_code: row.exit_code,
        repo: row.repo,
        reponame: item.reponame,
        branch: row.branch,
        commit_id: row.commit_id,
        tname: item.tname,
        created: row.created,
        commit_time: row.commit_time
      };
      let detail_name = '';
      if (item.reponame === 'Paddle2ONNX' || item.reponame === 'PaddleHub') {
        detail_name = 'FuncDetail';
      } else if (item.task_type === 'model' || item.task_type === 'benchmark') {
        detail_name = 'model';
      } else if (item.task_type === 'frame') {
        // 框架的secondary_type是数组
        if (Array.isArray(item.secondary_type)) {
          _params.secondary_type = item.secondary_type.join(',');
        }
        detail_name = 'FuncDetail';
      } else if (item.task_type === 'infer') {
        detail_name = 'FuncDetail';
      } else if (item.task_type === 'dist') {
        // 如果二级分类是api的则跳转api详情页；否则按模型汇聚
        if (item.secondary_type.toLowerCase().includes('api')) {
          // console.log('secondary_type', item.secondary_type);
          detail_name = 'FuncDetail';
        } else {
          // console.log('model secondary_type', item.secondary_type);
          detail_name = 'model';
        }
      } else if (item.task_type === 'compile') {
          _params.artifact_url = row.artifact_url;
          detail_name = 'Compile';
      } else {
        return;
      }
      const { href } = this.$router.resolve({name: detail_name, query: _params});
      window.open(href, '_blank');
    }
  }
};
</script>

<style scoped>
.all-line-row {
  margin-top: 1%;
  margin-bottom: 1%;
  margin-left: 1%;
  margin-right: 1%;
  font-size:14px;
}
</style>
