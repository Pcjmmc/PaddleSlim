<template>
  <div>
    <el-table
      :data="tableData"
      tooltip-effect="dark"
      align="center"
      style="width: 100%"
    >
      <el-table-column
        prop="id"
        label="ID"
        align="center"
        width="80"
      >
      </el-table-column>
      <el-table-column
        prop="mission"
        label="测试项"
        align="center"
        width="140"
      >
        <div slot-scope="scope">
          <a href="javascript:void(0)" @click="openXly(scope.row.info)">
            {{ scope.row.mission }}
          </a>
        </div>
      </el-table-column>
      <el-table-column
        prop="status"
        label="状态"
        width="100"
        align="center"
      >
        <div slot-scope="scope">
          <Tag :color="setColor(scope.row.status)">
            {{ getStatus(scope.row.status) }}
          </Tag>
        </div>
      </el-table-column>
      <el-table-column
        prop="result"
        label="结果"
        align="center"
      >
      </el-table-column>
      <el-table-column
        prop="create_time"
        align="center"
        width="155"
        label="创建时间"
      >
      </el-table-column>
      <el-table-column
        prop="report"
        align="center"
        width="90"
        label="详细报告"
      >
        <div slot-scope="scope">
          <el-button
            type="primary"
            size="mini"
            @click="openReport(scope.row)"
          >查看报告</el-button>
        </div>
      </el-table-column>
      <el-table-column
        prop="report"
        align="center"
        width="120"
        label="操作"
      >
        <div slot-scope="scope">
          <el-popconfirm
            title="确定取消？"
            @confirm="cancelJob(scope.row, scope.$index)"
          >
            <el-button
              slot="reference"
              :disabled="scope.row.status!=='running'"
              size="mini"
              type="primary"
              icon="el-icon-video-pause"
              circle
            ></el-button>
          </el-popconfirm>
          <el-popconfirm
            title="确定重跑？"
            @confirm="rerunJob(scope.row, scope.$index)"
          >
            <el-button
              slot="reference"
              :disabled="scope.row.status ==='running'"
              size="mini"
              type="warning"
              icon="el-icon-refresh-right"
              circle
            ></el-button>
          </el-popconfirm>
          <el-popconfirm
            title="确定标记异常？"
            @confirm="setFailedStatus(scope.row, scope.$index)"
          >
            <el-button
              slot="reference"
              :disabled="scope.row.status ==='running'"
              size="mini"
              type="danger"
              icon="el-icon-edit-outline"
              circle
            ></el-button>
          </el-popconfirm>
        </div>
      </el-table-column>
    </el-table>
  </div>
</template>
<script>
  import {
    FrameReportUrl,
    FrameMissionFailedUrl,
    FrameMissionRerunUrl,
    FrameMissionCancelUrl
  } from '../../api/url.js';
  import api from '../../api/index';
  export default {
    props: {
      tableData: {
        type: Array,
        default: function () {
          return [];
        }
      }
    },
    data() {
      return {
      };
    },
    methods: {
      setColor(status) {
        switch (status.toLowerCase()) {
          case 'done':
            return 'success';
          case 'success':
            return 'success';
          case 'passed':
            return 'success';
          case 'pass':
            return 'success';
          case 'running':
            return 'primary';
          case 'warning':
            return 'warning';
          case 'error':
            return 'warning';
          case 'fail':
            return 'error';
          case 'failed':
            return 'error';
          default:
            return 'error';
        }
      },
      getStatus(status) {
        console.log('status is', status);
        switch (status.toLowerCase()) {
          case 'success':
            return '成功';
          case 'done':
            return '已完成';
          case 'fail':
            return '失败';
          case 'running':
            return '运行中';
          case 'error':
            return '异常';
          default:
            return status;
        }
      },
      async openReport(item) {
        if (!item.allure_report) {
          await this.generateReport(item);
        }
        if (item.allure_report) {
          window.open(item.allure_report, '_blank');
        }
      },
      openXly(url) {
        if (url) {
          window.open(url, '_blank');
        } else {
          this.$Message.info({
            content: '下游任务没有回写任务地址!',
            duration: 5,
            closable: true
          });
        }
      },
      async generateReport(item) {
      if (!item.bos_url) {
        this.$Message.info({
          content: '暂时没有报告可查看，可以刷新页面看下任务是否结束。',
          duration: 5,
          closable: true
        });
        return;
      }
      let params = {
        bos_url: item.bos_url,
        id: item.id
      };
      const {code, data, message} = await api.post(FrameReportUrl, params);
      if (parseInt(code, 10) === 200) {
        item.allure_report = data.allure_report;
      } else {
        this.$Message.error({
          content: '请求出错: ' + message,
          duration: 30,
          closable: true
        });
      }
    },
    async cancelJob(row, index) {
      let params = {
        id: row.id
      };
      const {code, message} = await api.post(FrameMissionCancelUrl, params);
      if (parseInt(code, 10) === 200) {
        // todo
        // this.$set(this.tableData[index], 'status', 'error');
        this.$Message.info({
          content: '取消成功！',
          duration: 3,
          closable: true
        });
        this.$emit('getDetails');
      } else {
        this.$Message.error({
          content: '请求出错: ' + message,
          duration: 30,
          closable: true
        });
      }
    },
    async rerunJob(row, index) {
      let params = {
        id: row.id
      };
      const {code, message} = await api.post(FrameMissionRerunUrl, params);
      if (parseInt(code, 10) === 200) {
        // todo
        // this.$set(this.tableData[index], 'status', 'running');
        this.$Message.info({
          content: '操作成功！',
          duration: 3,
          closable: true
        });
        this.$emit('getDetails');
      } else {
        this.$Message.error({
          content: '请求出错: ' + message,
          duration: 30,
          closable: true
        });
      }
    },
    async setFailedStatus(row, index) {
      console.log('index is', index);
      let params = {
        id: row.id
      };
      const {code, message} = await api.post(FrameMissionFailedUrl, params);
      if (parseInt(code, 10) === 200) {
        // todo
        this.$Message.info({
          content: '标记成功！',
          duration: 3,
          closable: true
        });
        this.$emit('getDetails');
      } else {
        this.$Message.error({
          content: '请求出错: ' + message,
          duration: 30,
          closable: true
        });
      }
    }
    }
  };
</script>