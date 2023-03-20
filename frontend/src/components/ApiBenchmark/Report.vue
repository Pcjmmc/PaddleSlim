<template>
    <div class="one-fifth-video-col">
        <div style="font-weight: bold; line-height:200%; margin-bottom: 1%">
        <Divider orientation="left">我的任务</Divider>
            <Row :gutter="16">
                <Col span="2"> id: {{ $route.params.id }}</Col>
                <Col span="8"> commt: {{ myself.commit }}</Col>
                <Col span="3"> Place: {{ myself.place }}</Col>
                <Col span="3"> Python: {{ myself.python }}</Col>
                <Col span="3"> CUDA: {{ myself.cuda }}</Col>
                <Col span="5"> 创建时间: {{ myself.create_time }}</Col>
            </Row>
        <Divider orientation="left">基线任务/对比任务</Divider>
            <Row :gutter="16">
                <Col span="2"> id: {{ getCompareId() }}</Col>
                <Col span="8"> commt: {{ baseline.commit }}</Col>
                <Col span="3"> Place: {{ baseline.place }}</Col>
                <Col span="3"> Python: {{ baseline.python }}</Col>
                <Col span="3"> CUDA: {{ baseline.cuda }}</Col>
                <Col span="5"> 创建时间: {{ baseline.create_time }}</Col>
            </Row>
        <Divider orientation="left">API性能数据汇总</Divider>
        <Row>
            <Col span="4"></Col>
            <Col span="4">性能较好：{{ summary.good }}</Col>
            <Col span="6">性能接近：{{ summary.same }}</Col>
            <Col span="10">性能较差：{{ summary.bad }}</Col>
        </Row>

        </div>
        <div>
            <Table
                border
                :loading="loading"
                :columns="columns"
                :data="result"
            >
            </Table>
        </div>
    </div>
</template>



<script>
import api from '../../api/index';
import { ApiBenchmarkBaseCompare } from '../../api/url.js';
export default {
    name: 'ApiBenchmarkBaseReport',
    props: {
        id: {
            type: [Number],
            default: function () {
                return null;
            }
        },
        id1: {
            type: [Number],
            default: function () {
                return null;
            }
        }
    },
    data: function () {
        return {
            jobIds: [],
            loading: true,
            result: [],
            baseline: {},
            myself: {},
            summary: {},
            columns: [
                {
                    title: 'API',
                    key: 'api',
                    width: 200,
                    fixed: 'left',
                    filter: {
                        type: 'input'
                    }
                },
                {
                    title: 'Casename',
                    key: 'case_name',
                    width: 150,
                    fixed: 'left'
                },
                {
                    title: '前向',
                    align: 'center',
                    children: [
                        {
                            title: '我的任务',
                            align: 'center',
                            width: 150,
                            className: 'demo-table-info-forward-column',
                            render: (h, params) => {
                                return h('div', [
                                    h('p', {}, parseFloat(params.row.my_job.forward))
                                ]);
                            }
                        },
                        {
                            title: 'Baseline',
                            align: 'center',
                            width: 150,
                            className: 'demo-table-info-forward-column',
                            render: (h, params) => {
                                return h('div', [h('p', {}, params.row.latest.forward)]);
                            }
                        },
                        {
                            title: '前向差距',
                            align: 'center',
                            width: 150,
                            sortable: true,
                            key: 'compare',
                            className: 'demo-table-info-forward-column',
                            sortMethod: function (a, b, type) {
                                if (type === 'asc') {
                                    return a.forward > b.forward ? 1 : -1;
                                } else {
                                    return a.forward > b.forward ? -1 : 1;
                                }
                            },
                            render: (h, params) => {
                                let value = parseFloat(params.row.compare.forward);
                                let str = this.round(value);
                                return h('div', [
                                    h('p', {
                                        style: {
                                            color: this.setValueColor(value)
                                        }
                                    }, str)
                                ]);
                            }
                        }
                    ]
                },
                {
                    title: '反向',
                    align: 'center',
                    children: [
                        {
                            title: '我的任务',
                            align: 'center',
                            width: 150,
                            className: 'demo-table-info-backward-column',
                            render: (h, params) => {
                                return h('div', [h('p', {}, params.row.my_job.backward)]);
                            }
                        },
                        {
                            title: 'Baseline',
                            align: 'center',
                            width: 150,
                            className: 'demo-table-info-backward-column',
                            render: (h, params) => {
                                return h('div', [h('p', {}, params.row.latest.backward)]);
                            }
                        },
                        {
                            title: '反向差距',
                            align: 'center',
                            width: 150,
                            sortable: true,
                            key: 'compare',
                            className: 'demo-table-info-backward-column',
                            sortMethod: function (a, b, type) {
                                if (type === 'asc') {
                                    return a.backward > b.backward ? 1 : -1;
                                } else {
                                    return a.backward > b.backward ? -1 : 1;
                                }
                            },
                            render: (h, params) => {
                                let value = parseFloat(params.row.compare.backward);
                                let str = this.round(value);
                                return h('div', [
                                    h('p', {
                                        style: {
                                            color: this.setValueColor(value)
                                        }
                                    }, str)
                                ]);
                            }
                        }
                    ]
                },
                {
                    title: '整体',
                    align: 'center',
                    children: [
                        {
                            title: '我的任务',
                            align: 'center',
                            width: 150,
                            className: 'demo-table-info-total-column',
                            render: (h, params) => {
                                return h('div', [h('p', {}, params.row.my_job.total)]);
                            }
                        },
                        {
                            title: 'Baseline',
                            align: 'center',
                            width: 150,
                            className: 'demo-table-info-total-column',
                            render: (h, params) => {
                                return h('div', [h('p', {}, params.row.latest.total)]);
                            }
                        },
                        {
                            title: '整体差距',
                            align: 'center',
                            width: 150,
                            sortable: true,
                            key: 'compare',
                            className: 'demo-table-info-total-column',
                            sortMethod: function (a, b, type) {
                                console.log(a.total, b.total, type);
                                if (type === 'asc') {
                                    return a.total > b.total ? 1 : -1;
                                } else {
                                    return a.total > b.total ? -1 : 1;
                                }
                            },
                            render: (h, params) => {
                                let value = parseFloat(params.row.compare.total);
                                let str = this.round(value);
                                return h('div', [
                                    h('p', {
                                        style: {
                                            color: this.setValueColor(value)
                                        }
                                    }, str)
                                ]);
                            }
                        }
                    ]
                }
            ]
        };
    },
    mounted: function () {
        this.getCompareData();
    },
    methods: {
        getCompareId() {
            if (this.$route.params.id1 === -1 || this.$route.params.id1 === '-1') {
                return '基线无ID';
            } else {
                return this.$route.params.id1;
            }
        },
        round(value) {
            return value.toFixed(4).toString() + 'x';
        },
        setValueColor(value) {
            if (value >= 1.15) {
                return 'green';
            } else if (value < -1.15) {
                return 'red';
            } else {
                return '';
            }
        },
        async getCompareData() {
            let params = {
                id: this.$route.params.id || this.id,
                id1: this.$route.params.id1 || this.id1
            };
            // console.log(params);
            const { code, data, message } = await api.post(ApiBenchmarkBaseCompare, params);
            if (parseInt(code, 10) === 200) {
                this.result = data[0].compare;
                this.myself = data[0].my_job;
                this.baseline = data[0].latest;
                this.summary = data[0].summary;
                this.loading = false;
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

<style>
.one-fifth-video-col {
    margin-right: 1%;
    margin-left: 1%;
    margin-bottom: 1%;
    margin-top: 0.5%;
    font-size: 14px;
}
.ivu-table td.demo-table-info-forward-column {
    background-color: #fffeff;
}
.ivu-table td.demo-table-info-backward-column {
    background-color: #faffff;
}
.ivu-table td.demo-table-info-total-column {
    background-color: #fffff8;
}
</style>
