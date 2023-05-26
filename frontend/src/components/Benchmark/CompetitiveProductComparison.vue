<template>
    <div class="center-card-s">
        <div style="margin-top: 2%">
            <Row
                type="flex"
                align="middle"
                :gutter="8"
            >
                <Col span="2">
                    <h4>
                    任务名
                    </h4>
                </Col>
                <Col span="6">
                    <el-select
                        v-model="searchData.task_name"
                        size="small"
                        style="width:200%"
                        @change="setVersionList"
                    >
                        <el-option
                            :key="index"
                            :value="item"
                            :label="item"
                            v-for="(item, index) in taskNameList"
                        >
                            {{ item }}
                        </el-option>
                    </el-select>
                </Col>
            </Row>
            <Row
                type="flex"
                align="middle"
                :gutter="8"
                style="margin-top:1%"
            >
                <Col span="2">
                    <h4>
                    Paddle版本
                    </h4>
                </Col>
                <Col span="6">
                    <el-select
                        v-model="versionIndex"
                        size="small"
                        style="width:100%"
                        @change="setTaskDate"
                    >
                        <el-option
                         v-for="(item, index) in versionList"
                            :value="index"
                            :key="index"
                            :label="item"
                        >
                            {{ item }}
                        </el-option>
                    </el-select>
                </Col>
            </Row>
        </div>
        <div
            style="text-align:right;margin-right:3%"
        >
            <el-button
                type="primary"
                size="small"
                @click="callAllChildMethods"
            >
                查询
            </el-button>
            <el-button
                type="primary"
                size="small"
                @click="callDownload"
            >
                下载
            </el-button>
        </div>
        <div style="text-align:right;margin-top:1%">
            <p style="display: inline;">数据补全：</p>
            <i-Switch
                v-model="searchData.is_Fill"
                style="margin-right:9%"
                >
                <template #open>
                <span>开</span>
                </template>
                <template #close>
                <span>关</span>
                </template>
            </i-Switch>
            <el-radio-group
                v-model="searchData.metric"
                border
                size="small"
                @input="callChildMethod"
            >
                <span
                    :key="index"
                    :value="item.id"
                    v-for="(item, index) in tags"
                >
                    <el-radio-button v-bind:label="item.id"></el-radio-button>
                </span>
            </el-radio-group>
        </div>
        <div>
            <el-tabs
                v-model="tabName"
                @tab-click="handleTabClick"
            >
                <el-tab-pane
                    label="汇总数据"
                    name="summaryData"
                >
                    <summary-data
                        ref="summaryData"
                    >
                    </summary-data>
                </el-tab-pane>
                <el-tab-pane
                    label="对比数据"
                    name="comparativeData"
                >
                    <comparative-data
                        ref="comparative"
                        @change-model-name="handleSearchModelNameChange"
                    >
                    </comparative-data>
                </el-tab-pane>
            </el-tabs>
        </div>
    </div>
</template>

<script>
import {BenchmarkCheckTaskList, PaddleVsOtherDataDownload} from '../../api/url';
import api from '../../api/index';
import ComparativeData from './ComparativeData.vue';
import SummaryData from './SummaryData.vue';

export default {
    name: 'CompetitiveProductComparison',
    data: function () {
        return {
            tabName: 'summaryData',
            searchModelName: '',
            task: {},
            taskNameList: [],
            versionList: [],
            versionIndex: '',
            taskDateList: [],
            searchData: {
                task_name: '',
                task_date: '',
                is_Fill: '',
                metric: ''
            },
            tags: [
                {
                    id: 'ips',
                    checked: true
                },
                {
                    id: 'gpu_mem',
                    checked: false
                },
                {
                    id: 'cpu_use',
                    checked: false
                },
                {
                    id: 'gpu_use',
                    checked: false
                },
                {
                    id: 'accuracy',
                    checked: false
                }
            ]
        };
    },
    mounted: function () {
        this.getTaskList();
        this.setTabName();
        this.initData();
        this.callAllChildMethods();
    },
    methods: {
        initData() {
            this.versionIndex = 0;
            this.searchData.is_Fill = Boolean(false);
            this.searchData.metric = this.tags[0].id;
            this.$set(this.searchData, 'task_name', this.taskNameList[0]);
            this.$set(this.searchData, 'task_date', this.taskDateList[0]);
        },
        handleTabClick(tag) {
            sessionStorage.setItem('current_tab', tag.name);
        },
        setTabName() {
            this.tabName = sessionStorage.getItem('current_tab');
            if (this.tabName === null || this.tabName.length === 0) {
                this.tabName = 'summaryData';
            }
        },
        setVersionList(name) {
            var versionData = this.task[name];
            if (versionData === null || versionData === undefined) {
                this.$Message.error(
                    {
                        content: '抱歉当前的任务没有可以选择的版本，请重新选择',
                        duration: 1,
                        closable: true
                    }
                );
            }
            let versionList = [];
            let taskDateList = [];
            let index = 0;
            for (let key in versionData) {
                if (versionData.hasOwnProperty(key)) {
                    var value = versionData[key];
                    let version = value.paddle_version;
                    let task_date = value.task_date;
                    versionList.push(version);
                    taskDateList.push(task_date);
                    if (index === 0) {
                        this.$set(this, 'versionIndex', 0);
                        this.$set(this.searchData, 'task_date', taskDateList[0]);
                    }
                }
            }
            this.$set(this, 'versionList', versionList);
            this.$set(this, 'taskDateList', taskDateList);
        },
        dealWithTaskData(data) {
            if (data === null || data.length === 0) {
                this.$Message.error({
                    content: '抱歉当前没有可以选择的任务',
                    duration: 1,
                    closable: true
                });
            }
            var i = 0;
            for (let key in data) {
                if (data.hasOwnProperty(key)) {
                    this.taskNameList.push(key);
                    if (i === 0) {
                        this.$set(this.searchData, 'task_name', key);
                        this.setVersionList(key);
                    }
                    i++;
                }
            }
        },
        setTaskDate() {
            this.$set(this.searchData, 'task_date', this.taskDateList[this.versionIndex]);
        },
        async getTaskList() {
            this.task = [];
            const {code, message, data} = await api.get(BenchmarkCheckTaskList);
            if (parseInt(code, 10) === 200) {
                this.task = data;
                this.dealWithTaskData(this.task);
            } else {
                this.$Message.error({
                    content: '请求出错:' + message,
                    duration: 30,
                    closable: true
                });
            }
        },
        async callDownload() {
            let params = {
                task_name: this.searchData.task_name,
                task_date: this.searchData.task_date,
                metric_list: [this.searchData.metric],
                is_Fill: this.searchData.is_Fill,
                get_mode: 'download',
                search_model_item: this.searchModelName
            };
            const {code, message, data} = await api.post(PaddleVsOtherDataDownload, params);
            if (parseInt(code, 10) === 200) {
                const excelData = data;
                let blob = new Blob([excelData],
                { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
                let url = URL.createObjectURL(blob);
                let link = document.createElement('a');
                link.href = url;
                link.download = 'your-file-name.xlsx';
                document.body.appendChild(link);
                link.click();
            } else {
                this.$Message.error({
                    content: '请求出错:' + message,
                    duration: 30,
                    closable: true
                });
            }
        },
        callAllChildMethods() {
            this.callChildMethod();
            this.callSummaryChildMethod();
        },
        callChildMethod() {
            this.$refs.comparative.$emit('acceptFatherData', this.searchData);
        },
        callSummaryChildMethod() {
            this.$refs.summaryData.$emit('acceptFatherData', this.searchData);
        },
        handleSearchModelNameChange(modelName) {
            this.searchModelName = modelName;
        }
    },
    components: {
        ComparativeData,
        SummaryData
    }
};
</script>

<style scoped>
.btn-success {
  color: #fff;
  width: 10%;
  background-color: #1d98e4cb;
  border-color: #1d98e4cb;
  margin-right: 1%;
}

.center-card-s {
  margin-left: 1%;
  margin-right: 1%;
  font-size: 14px;
  color: lightslategrey;
}

</style>
