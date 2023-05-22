<template>
    <Poptip
        ref="poptip"
        placement="bottom-start"
        transfer
        max-width="300px"
    >
        <p
            v-bind:style="{color: this.color}"
        >
        {{ num }}
        </p>
        <div
            slot="content"
            class="api"
        >
             <div
                style="text-align:left; color:black"
             >
                <Row>
                    <Col span="3">
                        <p>模型库分支</p>
                    </Col>
                    <Col>
                        : {{ dealWithBlank('model_branch') }}
                    </Col>
                </Row>
                <Row>
                    <Col span="3">
                        <p>模型库commit号</p>
                    </Col>
                    <Col>
                        : {{ dealWithBlank('model_commit') }}
                    </Col>
                </Row>
                <Row>
                    <Col span="3">
                        <p>框架分支</p>
                    </Col>
                    <Col>
                        : {{ dealWithBlank('frame') }}
                    </Col>
                </Row>
                <Row>
                    <Col span="3">
                        <p>框架commit号</p>
                    </Col>
                    <Col>
                        : {{ dealWithBlank('frame_commit') }}
                    </Col>
                </Row>
                <Row>
                    <Col span="3">
                        <p>批次号</p>
                    </Col>
                    <Col>
                        : {{ dealWithBlank('task_date') }}
                    </Col>
                </Row>
                <Row>
                    <Col span="3">
                        <p>模型链接</p>
                    </Col>
                    <Col span="3">
                        <a
                        :href="info['script_url']"
                        target="_blank"
                        >
                        : {{ dealWithBlank('script_url') }}
                        </a>
                    </Col>
                </Row>
                <Row>
                    <Col span="3">
                        <p>执行脚本</p>
                    </Col>
                    <Col>
                        <a
                            style="word-wrap: break-word;"
                            href="#"
                            v-on:click="openModal('run_model_sh_url'); return false;"
                        >
                        : {{ dealWithBlank('run_model_sh_url') }}
                        </a>
                    </Col>
                </Row>
                <Row>
                    <Col span="3">
                        <p>paddlecloud-job号</p>
                    </Col>
                    <Col span="3">
                        <a
                        :href="info['pdc_job_id']"
                        target="_blank"
                        >
                        : {{ dealWithBlank('pdc_job_id') }}
                        </a>
                    </Col>
                </Row>
                <Row>
                    <Col span="3">
                        <p>训练日志链接</p>
                    </Col>
                    <Col>
                        : {{ dealWithBlank('train_log_url') }}
                    </Col>
                </Row>
                <Row>
                    <Col span="3">
                        <p>结果日志链接</p>
                    </Col>
                    <Col>
                        : {{ dealWithBlank('index_log_url') }}
                    </Col>
                </Row>
                <Row>
                    <Col span="3">
                        <p>profiler日志链接</p>
                    </Col>
                    <Col>
                        <a>
                            : {{ dealWithBlank('profiler_log_url') }}
                        </a>
                    </Col>
                </Row>
                <Row>
                    <Col span="3">
                        <p>下降原因</p>
                    </Col>
                    <Col>
                        : {{ dealWithBlank('down_reason') }}
                    </Col>
                </Row>
             </div>
        </div>
        <Modal
            v-model="modal"
            :width="modalWidth"
            :scrollable="true"
            :footer-hide="true"
            >
            <p style="word-wrap: break-word;">{{ modalContent }}</p>
        </Modal>
    </Poptip>
</template>

<script>

export default {
    name: 'Detail',
    props: {
        color: {
            type: [String],
            default: function () {
                return null;
            }
        },
        num: {
            type: [Number],
            default: function () {
                return null;
            }
        },
        info: {
            type: [Object],
            default: function () {
                return null;
            }
        }
    },
    data: function () {
        return {
            modalWidth: 0,
            modal: false,
            modalContent: ''
        };
    },
    mounted: function () {
        this.initData();
        this.setModalWidth();
    },
    methods: {
        setModalWidth() {
            this.modalWidth = window.innerWidth * 0.8;
        },
        initData() {
        },
        getData(key) {
            this.modalContent = this.info[key];
        },
        openModal(key) {
            this.getData(key);
            this.$refs.poptip.visible = false;
            this.modal = true;
        },
        dealWithBlank(key) {
            if (this.info[key] === undefined || this.info[key] === '') {
                return '暂无数据';
            } else {
                return this.info[key];
            }
        }
    }
};
</script>