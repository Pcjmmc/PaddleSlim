<template>
    <div class="center-card-s">
        <div>
            <el-input
                v-model="search_model_item"
                placeholder="搜索模型名"
                style="width: 30%;"
                size="small"
                @change="changeSearchModelName"
            >
            </el-input>
            <el-button
                icon="el-icon-search"
                circle
                size="small"
                @click="getData()"
            >
            </el-button>
            <pre style="display:inline">                                               </pre>
            <span style="display:inline;">Show</span>
            <el-select
                v-model="pagesize"
                size="small"
                style="width:6%"
                @change="changePageSize(pagesize)"
            >
                <el-option
                    :key="item"
                    :label="item"
                    :value="item"
                    v-for="item in this.pageSizeList"
                >
                </el-option>
            </el-select>
            <p style="display:inline">entries</p>
            <el-popover
                width="300"
                trigger="click"
            >
                <el-button
                    slot="reference"
                    icon="el-icon-s-grid"
                    circle
                    autofocus
                    size="mini"
                >
                </el-button>
                <el-checkbox
                    :indeterminate="isIndeterminate"
                    v-model="checkAll"
                    @change="handleCheckAllChange"
                >
                    全选
                </el-checkbox>
                <el-checkbox-group
                    v-model="contentKeyChecked"
                    style="width: 10%"
                    size="small"
                    @change="filterColumns()"
                    border
                >
                    <el-checkbox
                        :key="item"
                        :label="item"
                        v-for="item in contentKeys"
                    >
                    </el-checkbox>
                </el-checkbox-group>
            </el-popover>
        </div>
        <div style="margin-top: 1%;">
            <Table
                :data="data"
                :columns="content"
                :loading="loading"
                :no-data-text="'暂无数据'"
                border
            >
            </Table>
            <Page
                :total="total"
                :current="parseInt(pagenum)"
                :page-size="parseInt(pagesize)"
                size="small"
                style="text-align: center"
                v-on:on-change="pageChange"
              >
              </Page>
        </div>
    </div>


</template>

<script>
import api from '../../api/index';
import {BenchmarkPaddleVsOtherData} from '../../api/url';
import detailinfo from '../Benchmark/Detail.vue';
export default {
    name: 'ComparativeData',
    props: {
        fatherData: {
            type: [Object],
            default: function () {
                return null;
            }
        }
    },
    data: function () {
        return {
            search_model_item: '',
            pagesize: '',
            pagenum: 1,
            total: 0,
            modal: false,
            pageSizeList: [
                10,
                25,
                50,
                100
            ],
            content: [],
            contentBak: [],
            waveDiffList: {},
            data: [],
            contentKeyChecked: [],
            contentKeys: [],
            isIndeterminate: true,
            checkAll: false,
            paddleDetail: {},
            paddleDetailInfo: {},
            isWatch: true,
            loading: true,
            sessionCheckedName: 'paddleComparativeRemeber'
        };
    },
    created() {
        this.monitoring();
        const unwatch = this.$watch('fatherData.task_date', (newValue) => {
            if (newValue && this.isWatch) {
                this.getData();
                this.isWatch = false;
                unwatch();
            }
        });
    },
    mounted() {
        this.initData();
    },
    methods: {
        initData() {
            this.pagesize = 10;
        },
        monitoring() {
            this.$on('acceptFatherData', (res) => {
                if (this.fatherData.task_date) {
                    this.pagenum = 1;
                    this.getData();
                }
            });
        },
        getDeviceList(data) {
            return data.split(',');
        },
        dealWithContent(device_num_list) {
            this.content = [];
            this.contentBak = [];
            this.contentKeys = [];
            let deviceNumList = this.getDeviceList(device_num_list);
            this.contentBak.push(
                {title: '序号',
                type: 'index',
                width: 80,
                fixed: 'left',
                indexMethod: (row, index) => {
                    return this.pagesize * (this.pagenum - 1) + index + 1;
                }
            });
            this.contentBak.push({
                title: '配置名',
                key: 'config_name',
                minWidth: 100,
                resizable: true
            });
            deviceNumList.forEach(deviceNum => {
                this.contentBak.push({
                    title: 'Paddle_' + deviceNum,
                    key: 'paddle_' + deviceNum,
                    width: 150,
                    resizable: true,
                    sortable: true,
                    sortMethod: function (a, b, type) {
                        if (type === 'asc') {
                            if (a === '-') {
                                return 1;
                            } else if (b === '-') {
                                return -1;
                            } else {
                                return a > b ? 1 : -1;
                            }
                        } else {
                            if (a === '-') {
                                return -1;
                            } else if (b === '-') {
                                return 1;
                            } else {
                            return a > b ? -1 : 1;
                            }
                        }
                    },
                    render: (h, params) => {
                        let initValue = params.row['paddle_' + deviceNum];
                        if (initValue === '-') {
                            return h('div', [
                                h('p', {
                                },
                                '-'
                                )
                            ]);
                        } else {
                            let value = parseFloat(initValue, 10).toFixed(3);
                            let color = this.setPaddleValueColor(params.row, 'paddle_' + deviceNum);
                            let info = this.constructPaddleDetail(params.row, 'paddle_' + deviceNum);
                            return h(detailinfo, {
                                props: {
                                    color: color,
                                    num: value,
                                    info: info
                                }
                            });
                        }
                    }
                });
                this.contentBak.push({
                    title: 'Pytorch_' + deviceNum,
                    key: 'pytorch_' + deviceNum,
                    width: 150,
                    resizable: true,
                    render: (h, params) => {
                        let initValue = params.row['pytorch_' + deviceNum];
                        if (initValue === '-') {
                            return h('div', [
                                h('p', {
                                },
                                '-'
                                )
                            ]);
                        } else {
                            let value = parseFloat(initValue, 10).toFixed(3);
                            let color = this.setPaddleValueColor(params.row, 'pytorch_' + deviceNum);
                            let info = this.constructPaddleDetail(params.row, 'pytorch_' + deviceNum);
                            return h(detailinfo, {
                                props: {
                                    color: color,
                                    num: value,
                                    info: info
                                }
                            });
                        }
                    }
                });
                this.contentBak.push({
                    title: 'diff_' + deviceNum + '(paddle-pytorch)',
                    key: 'paddle_vs_other_' + deviceNum,
                    width: 120,
                    resizable: true,
                    sortable: true,
                    sortMethod: function (a, b, type) {
                        if (type === 'asc') {
                            if (a === '-') {
                                return 1;
                            } else if (b === '-') {
                                return -1;
                            } else {
                                return a > b ? 1 : -1;
                            }
                        } else {
                            if (a === '-') {
                                return 1;
                            } else if (b === '-') {
                                return -1;
                            } else {
                            return a > b ? -1 : 1;
                            }
                        }
                    },
                    render: (h, params) => {
                        let initValue = params.row['paddle_vs_other_' + deviceNum];
                        let value = '';
                        if (initValue === '-') {
                            value = '-';
                        } else {
                            value = parseFloat(initValue, 10).toFixed(3) + '%';
                        }
                        return h('div', [
                            h('p', {
                                style: {
                                color: this.setDiffStatusColor(params.row, 'paddle_vs_other_' + deviceNum)
                                }
                            }, value)
                        ]);
                    }
                });
            });
            this.contentBak.forEach(item => {
                this.content.push(item);
                this.contentKeys.push(item.title);
                this.contentKeyChecked.push(item.title);
            });
            if (sessionStorage.hasOwnProperty(this.sessionCheckedName)) {
                let sessionChecked = JSON.parse(sessionStorage.getItem(this.sessionCheckedName));
                if (sessionChecked && sessionChecked[this.fatherData.task_date]) {
                    this.contentKeyChecked = sessionChecked[this.fatherData.task_date];
                    this.content = this.contentBak.filter(col => {
                        return this.contentKeyChecked.includes(col.title);
                    });
                }
            }
        },
        dealWithTableData(device_num_list, paddle_vs_other_data) {
            this.data = [];
            // 获取具体数据
            // framework类型
            let frameworkList = ['paddle', 'pytorch'];
            // 当前存在数据的设备类型
            let deviceNumList = this.getDeviceList(device_num_list);
            // 以下的循环是用来获取Paddle Pytorch中的具体数值
            for (let config in paddle_vs_other_data) {
                // 每一个Config 变成一列
                let json = {};
                let outValue = paddle_vs_other_data[config];
                json.config_name = config;
                frameworkList.forEach(framework => {
                    let value = outValue[framework];
                    let newJson = {};
                    for (let i = 0; i < deviceNumList.length; i++) {
                        // get device name
                        let deviceNum = deviceNumList[i];
                        // get inner data
                        let innerValue = value[deviceNum];
                        // get detail info to show
                        if (innerValue.value !== '-') {
                            let detail = {};
                            detail.model_branch = innerValue.model_branch;
                            detail.model_commit = innerValue.model_commit;
                            detail.frame = innerValue.frame;
                            detail.frame_branch = innerValue.frame_branch;
                            detail.task_date = innerValue.task_date;
                            detail.script_url = innerValue.script_url;
                            detail.run_model_sh_url = innerValue.run_model_sh_url;
                            detail.pdc_job_id = innerValue.pdc_job_id;
                            detail.train_log_url = innerValue.train_log_url;
                            detail.index_log_url = innerValue.index_log_url;
                            detail.profiler_log_url = innerValue.profiler_log_url;
                            detail.down_reason = innerValue.down_reason;
                            this.paddleDetail[config + '_' + framework + '_' + deviceNum] = detail;
                        }
                        // get true value to show
                        json[framework + '_' + deviceNum] = innerValue.value;
                        // get wave_diff to store (use to set Paddle Color)
                        this.waveDiffList[config + '_' + framework + '_' + deviceNum] = innerValue.wave_diff;
                        let task_date = innerValue.task_date;
                        if (framework === 'paddle' &&
                            task_date !== this.fatherData.task_date &&
                            innerValue.value !== '-') {
                            newJson[framework + '_' + deviceNum] = 'demo-table-info-cell-paddle';
                            json.cellClassName = newJson;
                        }
                    }
                });
                //  获取diff数据列表
                let diffValueList = outValue.paddle_vs_other;
                // 将对应的diff数据列表存入data中
                deviceNumList.forEach(deviceNum => {
                    json['paddle_vs_other_' + deviceNum] = diffValueList[deviceNum];
                });
                this.data.push(json);
            }
        },
        async getData() {
            this.loading = true; // loading
            let params = {
                task_name: this.fatherData.task_name,
                task_date: this.fatherData.task_date,
                metric_list: [this.fatherData.metric],
                is_Fill: this.fatherData.is_Fill,
                pagenum: this.pagenum,
                pagesize: this.pagesize
            };
            if (this.search_model_item !== null && this.search_model_item.length > 0) {
                params.search_model_item = this.search_model_item;
            } else {
                params.search_model_item = '';
            }
            const {code, message, device_num_list,
                paddle_vs_other_data, total_num} = await api.post(BenchmarkPaddleVsOtherData, params);
            if (parseInt(code, 10) === 200) {
                this.total = total_num;
                this.dealWithContent(device_num_list);
                this.dealWithTableData(device_num_list, paddle_vs_other_data);
                this.loading = false;
            } else {
                this.$Message.error(
                    {
                        content: '请求出错：' + message,
                        duration: 10,
                        closable: true
                    }
                );
            }
        },
        async pageChange(pageNum) {
            this.pagenum = pageNum;
            await this.getData();
        },
        async changePageSize(pageSize) {
            this.pagesize = pageSize;
            this.pagenum = 1;
            await this.getData();
        },
        setPaddleValueColor(row, key) {
            let config = row.config_name;
            let str = this.waveDiffList[config + '_' + key];
            if (str === undefined) {
                return;
            }
            let value = parseFloat(str, 10);
            if (value > 5) {
                return 'red';
            }
        },
        constructPaddleDetail(row, key) {
            let detailName = row.config_name + '_' + key;
            return this.paddleDetail[detailName];
        },
        setDiffStatusColor(row, key) {
            let str = row[key];
            let value =  parseFloat(str, 10);
            if (value > 5) {
                return 'green';
            } else if (value < -5) {
                return 'red';
            }
        },
        handleCheckAllChange(val) {
            this.contentKeyChecked = val ? this.contentKeys : [];
            this.indeterminate = false;
            this.content = val ? this.contentBak : [];
            let sessionRecord = {};
            if (sessionStorage.hasOwnProperty(this.sessionCheckedName)) {
                sessionRecord = JSON.parse(sessionStorage.getItem(this.sessionCheckedName));
            }
            sessionRecord[this.fatherData.task_date] = val ? this.contentKeys : [];
            sessionStorage.setItem(this.sessionCheckedName, JSON.stringify(sessionRecord));
        },
        filterColumns() {
            let count = this.contentKeyChecked.length;
            this.checkAll = count === this.contentKeys.length;
            this.isIndeterminate = count > 0 && count < this.contentKeys.length;
            this.content = this.contentBak.filter(col => {
                return this.contentKeyChecked.includes(col.title);
            });
            let sessionRecord = {};
            if (sessionStorage.hasOwnProperty(this.sessionCheckedName)) {
                sessionRecord = JSON.parse(sessionStorage.getItem(this.sessionCheckedName));
            }
            sessionRecord[this.fatherData.task_date] = this.contentKeyChecked;
            sessionStorage.setItem(this.sessionCheckedName, JSON.stringify(sessionRecord));
        },
        changeSearchModelName() {
            this.$emit('change-model-name', this.search_model_item);
        }
    }
};
</script>

<style>

.ivu-table .demo-table-info-cell-paddle {
    background-color: #bab8b7;
    color: #fff;
}

.center-card-s {
  margin-left: 1%;
  margin-right: 1%;
  font-size: 14px;
  color: lightslategrey;
}

</style>
