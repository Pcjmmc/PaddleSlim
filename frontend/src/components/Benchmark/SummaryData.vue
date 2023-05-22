<template>
    <div class="center-card-s">
        <Collapse
            v-model="panelNames"
            @on-change="onPanelChange"
        >
            <Panel
                name="1"
            >
                环境信息
                <template #content>
                    <Card>
                        <p>任务名：{{ dealWithBlankData(env, 'task_name') }}</p>
                        <p>批次号：{{ dealWithBlankData(env, 'task_date') }}</p>
                        <p>GPU类型：{{ dealWithBlankData(env, 'devices_type') }}</p>
                        <p>CUDA版本：{{ dealWithBlankData(env, 'cuda_version') }}</p>
                        <p>cudnn版本：{{ dealWithBlankData(env, 'cudnn_version') }}</p>
                        <p>Paddle分支：{{ dealWithBlankData(env, 'frame_branch') }}</p>
                        <p>Paddle commit：{{ dealWithBlankData(env, 'frame_commit') }}</p>
                        <p>Paddle commit时间：{{ dealWithBlankData(env, 'frame_commit_dt') }}</p>
                        <p>镜像：{{ dealWithBlankData(env, 'docker_image') }}</p>
                        <p>模型优先级：{{ dealWithBlankData(env, 'model_priority_list') }}</p>
                        <p>模型类型覆盖：{{ dealWithBlankData(env, 'model_type_list') }}</p>
                        <p>模型库覆盖：{{ dealWithBlankData(env, 'model_repo_list') }}</p>
                    </Card>
                </template>
            </Panel>
            <Panel name="2">
                Paddle与竞品对比汇总
                <template #content>
                    <el-radio-group
                        v-model="tagSelected"
                        @input="changeTag"
                        border
                        size="small"
                    >
                        <span
                            :key="index"
                            :value="item"
                            v-for="(item, index) in tags"
                        >
                            <el-radio-button v-bind:label="item"></el-radio-button>
                        </span>
                    </el-radio-group>
                    <Table
                        :data="dataTorchShow"
                        :columns="columnsTorch"
                        :span-method="handleSpanMethod"
                        border
                    >
                    </Table>
                </template>
            </Panel>
            <Panel name="3">
                Paddle与例行对比汇总(配置级别)
                <template #content>
                    <Table
                        :data="dataConfig"
                        :columns="columnsConfig"
                        border
                    >
                    </Table>
                </template>
            </Panel>
            <Panel name="4">
                覆盖模型信息统计(配置级别)
                <template #content>
                    <Table
                        :data="dataModel"
                        :columns="columnsModel"
                        border
                    >
                    </Table>
                </template>
            </Panel>
            <Panel name="5">
                动转静与动态图对比汇总(配置级别)
                <template #content>
                    <Table
                        :data="dataCompareSummary"
                        :columns="columnsCompareSummary"
                        border
                    >
                    </Table>
                </template>
            </Panel>
            <Panel name="6">
                FP16与FP32对比汇总
                <template #content>
                    <Table
                    :data="dataFpCompare"
                    :columns="columnsFpCompare"
                    border
                    >
                    </Table>
                </template>
            </Panel>
        </Collapse>
    </div>
</template>

<script>
import api from '../../api/index';
import {BenchmarkPaddleVsOtherData} from '../../api/url';

export default {
    name: 'SummaryData',
    data: function () {
        return {
            panelNames: [],
            everPaneNames: [],
            fatherData: {},
            tags: [],
            tagSelected: '',
            dataTorch: {},
            dataTorchShow: [],
            dataConfig: [],
            dataModel: [],
            columnsTorch: [
                {
                    title: '模型类型',
                    key: 'model_type',
                    align: 'center',
                    fixed: 'left',
                    minWidth: 100
                },
                {
                    title: '运行配置',
                    key: 'run_config',
                    minWidth: 100
                },
                {
                    title: 'FP配置',
                    key: 'fpconfig',
                    minWidth: 100
                },
                {
                    title: '版本1_VS_BASE版本(GSB模型级别)',
                    key: 'GSB_model',
                    minWidth: 100
                },
                {
                    title: '版本1_VS_BASE版本(配置级别)',
                    key: 'GSB_config',
                    minWidth: 100
                }
            ],
            columnsConfig: [
                {
                    title: '模型类型',
                    key: 'model_type',
                    align: 'center',
                    fixed: 'left',
                    minWidth: 100
                },
                {
                    title: '运行配置',
                    key: 'run_config',
                    minWidth: 100
                },
                {
                    title: 'FP配置',
                    key: 'fpconfig',
                    minWidth: 100
                },
                {
                    title: 'paddle(成功配置数/总配置数)',
                    key: 'success_config',
                    minWidth: 100
                },
                {
                    title: '相对标准值下降5%以上个数',
                    key: 'down_standard',
                    minWidth: 100
                },
                {
                    title: '相对标准值上升5%以上个数',
                    key: 'up_standard',
                    minWidth: 100
                },
                {
                    title: '相对稳定版下降5%以上个数',
                    key: 'down_stable',
                    minWidth: 100
                },
                {
                    title: '相对稳定版上升5%以上个数',
                    key: 'up_stable',
                    minWidth: 100
                },
                {
                    title: '相对前五次均值下降5%以上个数',
                    key: 'down_med',
                    minWidth: 100
                },
                {
                    title: '相对前五次均值上升5%以上个数',
                    key: 'up_med',
                    minWidth: 100
                }
            ],
            columnsModel: [
                {
                    title: '模型库',
                    key: 'model',
                    align: 'center',
                    fixed: 'left',
                    minWidth: 100
                },
                {
                    title: '动态图模型数',
                    key: 'dynamic_model_num',
                    minWidth: 100
                },
                {
                    title: '静态图模型数',
                    key: 'static_model_num',
                    minWidth: 100
                },
                {
                    title: '动转静模型数',
                    key: 'transfer_model_num',
                    minWidth: 100
                },
                {
                    title: 'Paddle模型总数/总配置数',
                    key: 'total_num',
                    minWidth: 100
                },
                {
                    title: 'Paddle FP32模型数',
                    key: 'FP32_num',
                    minWidth: 100
                },
                {
                    title: 'Paddle FP16模型数',
                    key: 'FP16_num',
                    minWidth: 100
                },
                {
                    title: 'Paddle 波动<5%模型数',
                    key: 'paddle_good_num',
                    minWidth: 100
                }
            ],
            columnsCompareSummary: [],
            dataCompareSummary: [],
            columnsFpCompare: [],
            dataFpCompare: []
        };
    },
    monitoring() {
        this.$on('acceptFatherData', (res) => {
            this.fatherData = res;
            this.updateSelectedPanels();
        });
    },
    methods: {
        updateSelectedPanels() {
            for (let i = 0; i < this.panelNames.length; i++) {
                let panelName = this.panelNames[i];
                switch (panelName) {
                    case '1': {
                        this.getEnviromentsInfo();
                        break;
                    }
                    case '2': {
                        this.getTorchCompare();
                        break;
                    }
                    case '3': {
                        this.getConfigData();
                        break;
                    }
                    case '4': {
                        this.getModelData();
                        break;
                    }
                    case '5': {
                        this.getCompareSummery();
                        break;
                    }
                    case '6': {
                        this.getFpCompare();
                        break;
                    }
                }
            }
            this.everPaneNames = this.panelNames;
        },
        onPanelChange() {
            for (let i = 0; i < this.panelNames.length; i++) {
                let name = this.panelNames[i];
                if (!this.everPaneNames.includes(name)) {
                    this.everPaneNames.push(name);
                    switch (name) {
                        case '1': {
                            this.getEnviromentsInfo();
                            break;
                        }
                        case '2': {
                            this.getTorchCompare();
                            break;
                        }
                        case '3': {
                            this.getConfigData();
                            break;
                        }
                        case '4': {
                            this.getModelData();
                            break;
                        }
                        case '5': {
                            this.getCompareSummery();
                            break;
                        }
                        case '6': {
                            this.getFpCompare();
                            break;
                        }
                    }
                }
            }
        },
        async getEnviromentsInfo() {
            let task_date = this.fatherData.task_date;
            console.log(task_date);
            let params = {
                taskDate: task_date
            };
            const {code, message, data} = await api.post(BenchmarkPaddleVsOtherData, params);
            if (parseInt(code, 10) === 200) {
                this.env = data;
            } else {
                this.$Message.error({
                    content: '请求出错:' + message,
                    duration: 30,
                    closable: true
                });
            }
        },
        async getTorchCompare() {
            this.dealWithTorchCompareData();
            // let params = {
            //     task_date: this.fatherData['task_date'],
            //     zhibiao_list: JSON.stringify([this.fatherData.metric]),
            //     complete: this.fatherData.is_Fill
            // };
            // const {code, message, data} = await api.post(BenchmarkPaddleVsOtherData, params);
            // if (parseInt(code, 10) === 200) {
            //     this.torchCompare = data;
            //     this.dealWithTorchCompareData();
            // } else {
            //     this.$Message.error({
            //         content: '请求出错:' + message,
            //         duration: 30,
            //         closable: true
            //     });
            // }
        },
        dealWithBlankData(value, key) {
            if (value === null || value === '') {
                return '调试中';
            }
            if (value[key] === undefined || value[key] === '-') {
                return '暂无信息';
            } else {
                return value[key];
            }
        },
        // handleSpanMethod ({ row, column, rowIndex, columnIndex }) {
        //     if (columnIndex < 2) {
        //         let rowCount = 1;
        //         for (let i = rowIndex + 1; i < this.dataTorchShow.length; i++) {
        //             if (this.dataTorchShow[i][column.key] === row[column.key] &&
        //             this.dataTorchShow[i]['model_type'] === row['model_type']) {
        //                 rowCount++;
        //             } else {
        //                 break;
        //             }
        //         }
        //         return [rowCount, 1];
        //     }
        // },
        dealWithTorchCompareData() {
            this.tags = [];
            this.dataTorch = {};
            for (let key in this.torchCompare) {
                this.tags.push(key);
                let singleApp = [];
                let value = this.torchCompare[key];
                let model_type_index = 0;
                for (let model_type in value) {
                    let model_type_value  =  value[model_type];
                    let run_config_index = 0;
                    for (let run_config in model_type_value) {
                        let run_config_value = model_type_value[run_config];
                        for (let fpconfig in run_config_value) {
                            let json = {};
                            json.model_type = model_type;
                            json.run_config = run_config;
                            json.fpconfig = fpconfig;
                            let torch = run_config_value[fpconfig].vs_pytorch;
                            let torch_model = torch.model_level;
                            let torch_config = torch.config_level;
                            let compareNumString = '';
                            for (let numKey in torch_model) {
                                let num =  torch_model[numKey];
                                compareNumString += num + ':';
                            }
                            json.GSB_model = compareNumString.slice(0, -1);
                            compareNumString = '';
                            for (let numKey in torch_config) {
                                let num =  torch_config[numKey];
                                compareNumString += num + ':';
                            }
                            json.GSB_config = compareNumString.slice(0, -1);
                            json.model_type_index = model_type_index;
                            json.run_config_index = run_config_index;
                            model_type_index++;
                            run_config_index++;
                            singleApp.push(json);
                        }
                    }
                }
                this.dataTorch[key] = singleApp;
            }
            console.log(this.dataTorch);
            this.tagSelected = this.tags[0];
            this.dataTorchShow = this.dataTorch[this.tagSelected];
        },
        changeTag() {
            this.dataTorchShow = this.dataTorch[this.tagSelected];
        },
        async getConfigData() {
            this.dealWithConfigData(this.dataConfigBak);
            // let params = {
            //     task_date: this.fatherData['task_date'],
            //     zhibiao_list: JSON.stringify([this.fatherData.metric]),
            //     complete: this.fatherData.is_Fill,
            //     summary_type: 1
            // };
            // const {code, message, data} = await api.post(BenchmarkPaddleVsOtherData, params);
            // if (parseInt(code, 10) === 200) {
            //     this.dealWithTorchCompareData(data);
            // } else {
            //     this.$Message.error({
            //         content: '请求出错:' + message,
            //         duration: 30,
            //         closable: true
            //     });
            // }
        },
        dealWithConfigData(data) {
            this.dataConfig = [];
            for (let model_type in data) {
                if (model_type === 'total') {
                    break;
                }
                let model_type_layer = data[model_type];
                for (let run_config in model_type_layer) {
                    let run_config_layer = model_type_layer[run_config];
                    for (let fpconfig in run_config_layer) {
                        let fpconfig_layer = run_config_layer[fpconfig];
                        let json = {};
                        json.model_type = model_type;
                        json.run_config = run_config;
                        json.fpconfig = fpconfig;
                        let success = fpconfig_layer.success_num;
                        let fail = fpconfig_layer.fail_num;
                        let total = success + fail;
                        json.success_config = success + '/' + total;
                        json.down_standard = fpconfig.base_down_num;
                        json.up_standard = fpconfig.base_up_num;
                        json.down_stable = fpconfig.stable_down_num;
                        json.up_stable = fpconfig.stable_up_num;
                        json.down_med = fpconfig.mean_down_num;
                        json.up_med = fpconfig.mean_up_num;
                        this.dataConfig.push(json);
                    }
                }
            }
            let totalValue = data.total;
            let json = {};
            json.model_type = '汇总';
            json.run_config = '-';
            json.fpconfig = '-';
            let success = totalValue.success_num;
            let fail = totalValue.fail_num;
            let total = success + fail;
            json.success_config = success + '/' + total;
            json.down_standard = totalValue.base_down_num;
            json.up_standard = totalValue.base_up_num;
            json.down_stable = totalValue.stable_down_num;
            json.up_stable = totalValue.stable_up_num;
            json.down_med = totalValue.mean_down_num;
            json.up_med = totalValue.mean_up_num;
            this.dataConfig.push(json);
            console.log(this.dataConfig);
        },
        async getModelData() {
            this.dealWithModelData(this.dataModelBak);
            // let params = {
            //     task_date: this.fatherData['task_date'],
            //     zhibiao_list: JSON.stringify([this.fatherData.metric]),
            //     complete: this.fatherData.is_Fill
            // };
            // const {code, message, data} = await api.post(BenchmarkPaddleVsOtherData, params);
            // if (parseInt(code, 10) === 200) {
            //     this.dealWithModelData(data);
            // } else {
            //     this.$Message.error({
            //         content: '请求出错:' + message,
            //         duration: 30,
            //         closable: true
            //     });
            // }
        },
        dealWithModelData(data) {
            // 有些字段没对齐 需要再对齐一下
            this.dataModel = [];
            for (let model in data) {
                let json = {};
                let model_layer = data[model];
                json.model = model;
                for (let key in model_layer) {
                    let value = model_layer[key];
                    if (key === 'gather_num') {
                        json.total_num = value.total_num;
                        json.paddle_good_num = value.stable_num;
                    } else if (key === 'model_type') {
                        json.static = value.static;
                    } else if (key === 'fp_mode') {
                        json.FP32_num = value.fp32;
                        json.FP16_num = value.fp16;
                    }
                }
                this.dataModel.push(json);
            }
        },
        async getCompareSummery() {
            this.contentCompareSummary(this.dataCompareSummaryBak);
            this.dealWithCompareSummary(this.dataCompareSummaryBak);
            // let params = {
            //     task_date: this.fatherData['task_date'],
            //     zhibiao_list: JSON.stringify([this.fatherData.metric]),
            //     complete: this.fatherData.is_Fill,
            //     summary_type: 1
            // };
            // const {code, message, data} = await api.post(BenchmarkPaddleVsOtherData, params);
            // if (parseInt(code, 10) === 200) {
            //     this.contentCompareSummary(data);
            //     this.dealWithCompareSummary(data);
            // } else {
            //     this.$Message.error({
            //         content: '请求出错:' + message,
            //         duration: 30,
            //         closable: true
            //     });
            // }
        },
        contentCompareSummary(data) {
            this.columnsCompareSummary = [];
            this.columnsCompareSummary.push(
                {
                    title: '运行配置',
                    key: 'config',
                    width: 100,
                    fixed: 'left',
                    resizable: true
                });
            this.columnsCompareSummary.push({
                    title: 'FP配置',
                    key: 'fpconfig',
                    width: 100,
                    resizable: true
                });
            for (let config in data) {
                let value = data[config];
                let firstKey = Object.keys(value)[0];
                let innerValue = value[firstKey];
                for (let column in innerValue) {
                    this.columnsCompareSummary.push({
                        title: column,
                        key: column,
                        minWidth: 100,
                        resizable: true
                    });
                }
            }
            console.log(this.columnsCompareSummary);
        },
        dealWithCompareSummary(data) {
            this.dataCompareSummary = [];
            for (let config in data) {
                let value = data[config];
                for (let fpconfig in value) {
                    let innerValue = value[fpconfig];
                    let json = {};
                    json.config = config;
                    json.fpconfig = fpconfig;
                    for (let column in innerValue) {
                        let str = '';
                        let numValue = innerValue[column];
                        for (let key in numValue) {
                            str += numValue[key] + ':';
                        }
                        str = str.slice(0, -1);
                        json[column] = str;
                    }
                    this.dataCompareSummary.push(json);
                }
            }
            console.log(this.dataCompareSummary);
        },
        async getFpCompare() {
            this.columnFpCompare(this.dataFpCompareBak);
            this.dealWithFpCompare(this.dataFpCompareBak);
            // let params = {
            //     task_date: this.fatherData['task_date'],
            //     zhibiao_list: JSON.stringify([this.fatherData.metric]),
            //     complete: this.fatherData.is_Fill,
            //     summary_type: 1
            // };
            // const {code, message, data} = await api.post(BenchmarkPaddleVsOtherData, params);
            // if (parseInt(code, 10) === 200) {
            //     this.columnFpCompare(data);
            //     this.dealWithFpCompare(data);
            // } else {
            //     this.$Message.error({
            //         content: '请求出错:' + message,
            //         duration: 30,
            //         closable: true
            //     });
            // }
        },
        columnFpCompare(data) {
            this.columnsFpCompare = [];
            this.columnsFpCompare.push(
                {
                    title: '动/静态',
                    key: 'isStatic',
                    width: 100,
                    fixed: 'left',
                    resizable: true
                });
            this.columnsFpCompare.push({
                    title: '模型库',
                    key: 'config',
                    width: 100,
                    resizable: true
            });
            for (let config in data) {
                let value = data[config];
                let firstKey = Object.keys(value)[0];
                let innerValue = value[firstKey];
                for (let column in innerValue) {
                    this.columnsFpCompare.push({
                        title: column,
                        key: column,
                        minWidth: 100,
                        resizable: true
                    });
                }
            }
            console.log(this.columnsFpCompare);
        },
        dealWithFpCompare(data) {
            this.dataFpCompare = [];
            for (let config in data) {
                let value = data[config];
                for (let fpconfig in value) {
                    let innerValue = value[fpconfig];
                    let json = {};
                    json.isStatic = config;
                    json.config = fpconfig;
                    for (let column in innerValue) {
                        let str = '';
                        let numValue = innerValue[column];
                        for (let key in numValue) {
                            str += numValue[key] + ':';
                        }
                        str = str.slice(0, -1);
                        json[column] = str;
                    }
                    this.dataFpCompare.push(json);
                }
            }
            console.log(this.dataFpCompare);
        }
    }
};
</script>