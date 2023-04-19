<template>
    <div class="center-card-s">
        <div style="margin-top: 1%">
            <Row>
                <Col span="2">Framework:</Col>
                <Col span="6">
                    <CheckboxGroup
                        v-model="search.framework"
                    >
                        <Checkbox
                            v-for="(item, index) in framework"
                            :key="index"
                            :label="item.desc"
                        >
                        </Checkbox>
                    </CheckboxGroup>
                </Col>
            </Row>
        </div>
        <div style="margin-top: 1%">
            <Row>
                <Col span="2">Python:</Col>
                <Col>
                    <CheckboxGroup v-model="search.python">
                        <Checkbox
                            v-for="(item, index) in python"
                            :key="index"
                            :label="item"
                        >
                        </Checkbox>
                    </CheckboxGroup>
                </Col>
            </Row>
        </div>
        <div style="margin-top: 1%">
            <Row>
                <Col span="2">System:</Col>
                <Col>
                    <CheckboxGroup v-model="search.system">
                        <Checkbox
                            v-for="(item, index) in system"
                            :key="index"
                            :label="item"
                        >
                        </Checkbox>
                    </CheckboxGroup>
                </Col>
            </Row>
        </div>
        <div style="margin-top: 1%">
            <Row>
                <Col span="2">Place:</Col>
                <Col>
                    <CheckboxGroup v-model="search.place">
                        <Checkbox
                            v-for="(item, index) in place"
                            :key="index"
                            :label="item"
                        >
                        </Checkbox>
                    </CheckboxGroup>
                </Col>
            </Row>
        </div>
        <div style="margin-top: 1%">
            <Row>
                <Col span="2">CUDA:</Col>
                <Col>
                    <CheckboxGroup v-model="search.cuda">
                        <Checkbox
                            v-for="(item, index) in cuda"
                            :key="index"
                            :label="item"
                        >
                        </Checkbox>
                    </CheckboxGroup>
                </Col>
            </Row>
        </div>
        <div style="margin-top: 1%">
            <Row>
                <Col span="2">Version:</Col>
                <Col>
                    <CheckboxGroup v-model="search.version">
                        <Checkbox
                            v-for="(item, index) in version"
                            :key="index"
                            :label="item"
                        >
                        </Checkbox>
                    </CheckboxGroup>
                </Col>
            </Row>
        </div>
        <div style="margin-top: 1%">
            <span>
              创建时间:
              <DatePicker
                type="daterange"
                placement="bottom-end"
                placeholder=" 开始时间 ～ 结束时间 "
                style="width: 30%"
                v-model="dt"
                v-on:on-change="searchByfilter"
              ></DatePicker>
            </span>
        </div>
        <div style="margin-top: 1%">
            <div>
              任务名:
              <Input
                v-model="search.name"
                placeholder="任务名"
                style="width: 300px"
              >
                </Input>
                commit:
              <Input
                v-model="search.commit"
                placeholder="Commit"
                style="width: 300px"
              >
                </Input>
                <Button
                class="btn-success"
                shape="circle"
                icon="ios-search"
                @click="searchByfilter"
                >
                Search
                </Button>
                <Button
                    icon="md-"
                    class="btn-success"
                    @click="getComporeReport"
                    >
                    查看对比
                </Button>
             </div>
        </div>
        <div style="margin-top: 1%">
            <div class="left" style="margin-top: 2%">
              <Table
              border
              :columns="columns"
              :data="content"
              v-on:on-select="selectTable"
              v-on:on-select-cancel="selectCancel"
              >
            </Table>
              <Page
                :total="total"
                :current="parseInt(search.page)"
                :page-size="parseInt(search.pagesize)"
                size="small"
                style="text-align: center"
                v-on:on-change="pageChange"
              >
              </Page>
            </div>
        </div>
    </div>
</template>

<script>
import { ApiBenchmarkSetting, ApiBenchmarkJobs, ApiBenchmarkRoutine } from '../../api/url';
import api from '../../api/index';
import { CheckboxGroup } from 'iview';
import { dateFmt } from '../../util/help.js';

export default {
    name: 'QueryPage',
    data: function () {
        return {
            selection: [

            ],
            framework: [
                {
                    id: 'all',
                    desc: 'all',
                    checked: false
                },
                {
                    id: 'paddle',
                    desc: 'Paddle',
                    checked: false
                },
                {
                    id: 'torch',
                    desc: 'Torch',
                    checked: false
                }
            ],
            python: [
                'all',
                'python3.8',
                'python3.7'
            ],
            system: [
                'all',
                'Windows',
                'Linux',
                'Darwin'
            ],
            place: [
            ],
            version: [
            ],
            cuda: [

            ],
            search: {
                page: 1,
                pagesize: 15,
                name: '',
                commit: '',
                framework: ['all'],
                python: ['all'],
                os: ['all'],
                place: ['all'],
                system: ['all'],
                cuda: ['all'],
                backward: ['all'],
                version: ['all']
            },
            columns: [
                {
                type: 'selection',
                width: 60,
                align: 'center',
                fixed: 'left'
                },
                {
                title: '任务ID',
                key: 'id',
                align: 'center',
                fixed: 'left',
                minWidth: 100
                },
                {
                title: '任务名',
                key: 'comment',
                align: 'center',
                minWidth: 200
                },
                {
                title: 'Framework',
                key: 'framework',
                align: 'center',
                minWidth: 120
                },
                {
                title: 'Python',
                key: 'python',
                align: 'center',
                minWidth: 100
                },
                {
                title: 'OS',
                key: 'system',
                align: 'center',
                minWidth: 100
                },
                {
                title: 'Place',
                key: 'place',
                align: 'center',
                minWidth: 100
                },
                {
                title: 'CUDA',
                key: 'cuda',
                align: 'center',
                minWidth: 100
                },
                {
                title: '反向',
                key: 'enable_backward',
                align: 'center',
                minWidth: 100,
                render: (h, params) => {
                    return h('div', [
                        h('p', {
                        }, this.setBackward(params.row))
                    ]);
                }
                },
                {
                title: '配置详情',
                align: 'center',
                minWidth: 100,
                render: (h, params) => {
                    let str = this.setDefaultConfig(params.row.yaml_info);
                    return h('div', [
                            h('p', {
                            }, str)
                        ]);
                }
                },
                {
                title: 'Wheel包',
                key: 'version',
                align: 'center',
                minWidth: 100,
                render: (h, params) => {
                    if (params.row.wheel_link !== null) {
                    return h('div', [
                            h('Button', {
                            props: {
                                to: params.row.wheel_link,
                                target: '_blank',
                                icon: 'ios-download-outline'
                            }
                            })
                        ]);
                    } else {
                    return h('div', [
                            h('p', {
                            }, params.row)
                        ]);
                    }
                }
                },
                {
                title: '创建时间',
                key: 'create_time',
                align: 'center',
                minWidth: 120
                }
            ],
            total: 0,
            content: [
            ],
            dt: [this.getBeginData(), new Date()]
        };
    },
    mounted: function () {
        this.getSeeting();
        this.initData();
        this.searchByfilter();
    },
    methods: {
        async getSeeting() {
            const { code, data, message, all_count } = await api.get(ApiBenchmarkSetting);
            if (parseInt(code, 10) === 200) {
                this.cuda = data.cuda;
                this.system = data.system;
                this.place = data.place;
                this.python = data.python;
                this.version = data.version;
            } else {
                this.content = [];
                this.$Message.error({
                    content: '请求出错: ' + message,
                    duration: 30,
                    closable: true
                });
            }
        },
        initData() {
            this.tableSelect = [];
            this.content = [];
            this.search = {
                begin_time: null,
                end_time: null,
                page: 1,
                pagesize: 15,
                name: '',
                commit: '',
                framework: ['all'],
                python: ['all'],
                os: ['all'],
                place: ['all'],
                system: ['all'],
                cuda: ['all'],
                backward: ['all'],
                version: ['all']
            };
        },
        setStatusColor(value) {
        if (value === 'done') {
            return 'green';
        } else if (value === 'error') {
            return 'red';
        }
        },
        getBeginData() {
        // 在end_time的基础上+1， 因为end_time代表的今天0点0分0秒的时间
        let begin_time = new Date();
        begin_time = begin_time.setDate(begin_time.getDate() - 7);
        begin_time = new Date(begin_time);
        return begin_time;
        },
        setBackward(row) {
        if (row.enable_backward === 1) {
            return '是';
        } else {
            return '否';
        }
        },
        setDefaultConfig(value) {
        if (value === 'case_0') {
            return '小kernel';
        } else if (value === 'case_1') {
            return '中kernel';
        } else if (value === 'case_2') {
            return '大kernel';
        } else {
            return '全部kernel';
        }
        },
        setDisabled(row) {
        if (row.status === 'done') {
            return false;
        } else {
            return true;
        }
        },
        getComporeReport() {
        if (this.selection.length !== 2) {
            this.$Message.error({
            content: '请选择两个版本进行对比',
            duration: 1,
            closable: true
            });
        } else {
            let _params = {
            id: this.selection[0].id,
            id1: this.selection[1].id
            };
            const { href } = this.$router.resolve({name: 'ApiBenchmarkBaseReport', params: _params});
            window.open(href, '_blank');
        }
        },
        async searchByfilter() {
        this.search.page = 1;
        await this.searchData();
        },
        async handleReset() {
        await this.$refs.child.initData();
        },
        async handleSubmit() {
        await this.$refs.child.handleSummit();
        },
        async pageChange(pageNum) {
        this.search.page = pageNum;
        await this.searchData();
        },
        async searchData() {
        // 根据条件查询
        this.content = [];
        this.search.begin_time = dateFmt(this.dt[0], 'yyyy-MM-dd');
        // 在end_time的基础上+1， 因为end_time代表的今天0点0分0秒的时间
        let end_time = new Date(this.dt[1]);
        end_time = end_time.setDate(end_time.getDate() + 1);
        end_time = new Date(end_time);
        this.search.end_time = dateFmt(end_time, 'yyyy-MM-dd');
        let params = {
            page_index: this.search.page,
            limit: this.search.pagesize,
            begin_time: this.search.begin_time,
            end_time: this.search.end_time,
            comment: this.search.name ? this.search.name : null,
            commit: this.search.commit ? this.search.commit : null,
            framework: this.search.framework ? JSON.stringify(this.search.framework) : null,
            cuda: this.search.cuda ? JSON.stringify(this.search.cuda) : null,
            system: this.search.system ? JSON.stringify(this.search.system) : null,
            place: this.search.place ? JSON.stringify(this.search.place) : null,
            version: this.search.version ? JSON.stringify(this.search.version) : null,
            python: this.search.python ? JSON.stringify(this.search.python) : null
        };
        const {code, data, message, all_count} = await api.get(ApiBenchmarkJobs, params);
        if (parseInt(code, 10) === 200) {
            this.content = data;
            this.addSpecialProp();
            this.total = all_count;
        } else {
            this.content = [];
            this.$Message.error({
            content: '请求出错: ' + message,
            duration: 30,
            closable: true
            });
        }
        },
        addSpecialProp() {
        for (let i in this.content) {
            let row = this.content[i];
            if (row.status === 'done') {
            this.content[i]._disabled = false;
            } else {
            this.content[i]._disabled = true;
            }
        }
        },
        selectTable(selection) {
        this.selection = selection;
        if (selection.length > 2) {
            this.$Message.error({
            content: '只能选择两个版本进行对比',
            duration: 1,
            closable: true
            });
        }
        },
        selectCancel(selection) {
            this.selection = selection;
        }
    }
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
