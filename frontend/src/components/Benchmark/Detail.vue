<template>
    <Poptip
        ref="poptip"
        placement="bottom-start"
        trigger="hover"
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
                    <Col span="4">
                        <p>模型库分支:</p>
                    </Col>
                    <Col>
                        {{ dealWithBlank('model_branch') }}
                    </Col>
                </Row>
                <Row>
                    <Col span="4">
                        <p>模型库commit号:</p>
                    </Col>
                    <Col>
                        {{ dealWithBlank('model_commit') }}
                    </Col>
                </Row>
                <Row>
                    <Col span="4">
                        <p>框架分支:</p>
                    </Col>
                    <Col>
                        {{ dealWithBlank('frame') }}
                    </Col>
                </Row>
                <Row>
                    <Col span="4">
                        <p>框架commit号:</p>
                    </Col>
                    <Col>
                        {{ dealWithBlank('frame_commit') }}
                    </Col>
                </Row>
                <Row>
                    <Col span="4">
                        <p>批次号:</p>
                    </Col>
                    <Col>
                        {{ dealWithBlank('task_date') }}
                    </Col>
                </Row>
                <Row>
                    <Col span="4">
                        <p>模型链接:</p>
                    </Col>
                    <Col span="4">
                        <a
                        :href="info['script_url']"
                        target="_blank"
                        >
                        {{ dealWithBlank('script_url') }}
                        </a>
                    </Col>
                </Row>
                <Row>
                    <Col span="4">
                        <p>执行脚本:</p>
                    </Col>
                    <Col>
                        <a
                            style="word-wrap: break-word;"
                            href="#"
                            v-on:click="getData('run_model_sh_url'); return false;"
                        >
                        {{ getPartUrl('run_model_sh_url') }}
                        </a>
                    </Col>
                </Row>
                <Row>
                    <Col span="4">
                        <p>paddlecloud-job号:</p>
                    </Col>
                    <Col span="4">
                        <a
                        :href="info['pdc_job_id']"
                        target="_blank"
                        >
                        {{ dealWithBlank('pdc_job_id') }}
                        </a>
                    </Col>
                </Row>
                <Row>
                    <Col span="4">
                        <p>训练日志链接:</p>
                    </Col>
                    <Col>
                        <a
                            style="word-wrap: break-word;"
                            href="#"
                            v-on:click="getData('train_log_url'); return false;"
                        >
                        {{ getPartUrl('train_log_url') }}
                        </a>
                    </Col>
                </Row>
                <Row>
                    <Col span="4">
                        <p>结果日志链接:</p>
                    </Col>
                    <Col>
                        <a
                            style="word-wrap: break-word;"
                            href="#"
                            v-on:click="getData('index_log_url'); return false;"
                        >
                        {{ getPartUrl('index_log_url') }}
                        </a>
                    </Col>
                </Row>
                <Row>
                    <Col span="4">
                        <p>profiler日志链接:</p>
                    </Col>
                    <Col>
                        <a
                            style="word-wrap: break-word;"
                            href="#"
                            v-on:click="getData('profiler_log_url'); return false;"
                        >
                        {{ getPartUrl('profiler_log_url') }}
                        </a>
                    </Col>
                </Row>
                <Row>
                    <Col span="4">
                        <p>下降原因:</p>
                    </Col>
                    <Col>
                        {{ dealWithBlank('down_reason') }}
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
            <pre style="word-wrap: break-word;">{{ modalContent }}</pre>
        </Modal>
    </Poptip>
</template>

<script>
import api from '../../api';
import {PaddleVsOtherReadLog} from '../../api/url';

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
        this.setModalWidth();
    },
    methods: {
        setModalWidth() {
            this.modalWidth = window.innerWidth * 0.5;
        },
        getPartUrl(key) {
            let url = this.info[key];
            let urlArray =  url.split('/');
            let cleanUrl = '';
            if (urlArray.length > 0) {
                cleanUrl = urlArray[urlArray.length - 1];
            } else {
                cleanUrl = this.dealWithBlank(url);
            }
            if (cleanUrl === '') {
                return '暂无数据';
            } else {
                return cleanUrl;
            }
        },
        async getData(key) {
            let params = {
                log_url: this.info[key].split(':')[1]
            };
            if (params.log_url === undefined || params.log_url === '') {
                return;
            }
            const data = await api.get(PaddleVsOtherReadLog, params);
            this.modalContent = JSON.stringify(data, null, 2);
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