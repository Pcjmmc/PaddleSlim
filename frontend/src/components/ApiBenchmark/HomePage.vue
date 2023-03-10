<template>
    <div class="one-fifth-video-col">
            <div style="font-weight: bold; line-height:200%; margin-bottom: 1%">
                <Row>
                    <Col span="3"> 例行任务(Latest)</Col>
                    <Col span="8"> Commit: {{ latest.commit }}</Col>
                    <Col span="6"> Place: {{ latest.place }}</Col>
                    <Col span="6"> 执行时间：{{ latest.create_time }}</Col>
                </Row>
                <Row>
                    <Col span="3"> 基线任务(Baseline)</Col>
                    <Col span="6"> Version: {{ baseline.version }}</Col>
                </Row>
            </div>
        <div>
            <Table
                border
                height="800"
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
import { ApiCompare } from '../../api/url.js';
export default {
    name: 'HomePage',
    data: function () {
        return {
            loading: true,
            result: [],
            baseline: {},
            latest: {},
            columns: [
                {
                    title: 'API',
                    key: 'api',
                    width: 200,
                    fixed: 'left'
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
                            title: 'Latest',
                            align: 'center',
                            width: 150,
                            render: (h, params) => {
                                return h('div', [
                                    h('p', {}, parseFloat(params.row.latest.forward))
                                ]);
                            }
                        },
                        {
                            title: 'Baseline',
                            align: 'center',
                            width: 150,
                            render: (h, params) => {
                                return h('div', [h('p', {}, params.row.baseline.forward)]);
                            }
                        },
                        {
                            title: '前向差距',
                            align: 'center',
                            width: 150,
                            sortable: true,
                            key: 'compare',
                            sortMethod: function (a, b, type) {
                                console.log(a.forward, b.forward, type);
                                if (type === 'asc') {
                                    return a.forward > b.forward ? -1 : 1;
                                } else {
                                    return a.forward > b.forward ? 1 : -1;
                                }
                            },
                            render: (h, params) => {
                                let value = params.row.compare.forward;
                                let str = this.round(value);
                                return h('div', [
                                    h(
                                        'p',
                                        {
                                            style: {
                                                color: this.setValueColor(value)
                                            }
                                        },
                                        str
                                    )
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
                            title: 'Latest',
                            align: 'center',
                            width: 150,
                            render: (h, params) => {
                                return h('div', [h('p', {}, params.row.latest.backward)]);
                            }
                        },
                        {
                            title: 'Baseline',
                            align: 'center',
                            width: 150,
                            render: (h, params) => {
                                return h('div', [h('p', {}, params.row.baseline.backward)]);
                            }
                        },
                        {
                            title: '反向差距',
                            align: 'center',
                            width: 150,
                            sortable: true,
                            key: 'compare',
                            sortMethod: function (a, b, type) {
                                console.log(a.backward, b.backward, type);
                                if (type === 'asc') {
                                    return a.backward > b.backward ? -1 : 1;
                                } else {
                                    return a.backward > b.backward ? 1 : -1;
                                }
                            },
                            render: (h, params) => {
                                let value = params.row.compare.backward;
                                let str = this.round(value);
                                return h('div', [
                                    h(
                                        'p',
                                        {
                                            style: {
                                                color: this.setValueColor(value)
                                            }
                                        },
                                        str
                                    )
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
                            title: 'Latest',
                            align: 'center',
                            width: 150,
                            render: (h, params) => {
                                return h('div', [h('p', {}, params.row.latest.total)]);
                            }
                        },
                        {
                            title: 'Baseline',
                            align: 'center',
                            width: 150,
                            render: (h, params) => {
                                return h('div', [h('p', {}, params.row.baseline.total)]);
                            }
                        },
                        {
                            title: '整体差距',
                            align: 'center',
                            width: 150,
                            sortable: true,
                            key: 'compare',
                            sortMethod: function (a, b, type) {
                                console.log(a.total, b.total, type);
                                if (type === 'asc') {
                                    return a.total > b.total ? -1 : 1;
                                } else {
                                    return a.total > b.total ? 1 : -1;
                                }
                            },
                            render: (h, params) => {
                                let value = params.row.compare.total;
                                let str = this.round(value);
                                return h('div', [
                                    h(
                                        'p',
                                        {
                                            style: {
                                                color: this.setValueColor(value)
                                            }
                                        },
                                        str
                                    )
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
        round(value) {
            return value.toFixed(4).toString() + 'x';
        },
        setValueColor(value) {
            if (value > 1.1) {
                return 'green';
            } else if (value < -1.1) {
                return 'red';
            } else {
                return 'grad';
            }
        },
        async getCompareData() {
            const { code, data, message } = await api.post(ApiCompare);
            if (parseInt(code, 10) === 200) {
                this.result = data[0].compare;
                this.baseline = data[0].baseline;
                this.latest = data[0].latest;
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

<style scoped>
.one-fifth-video-col {
    margin-right: 1%;
    margin-left: 1%;
    margin-bottom: 1%;
    margin-top: 0.5%;
    font-size: 14px;
}
</style>
