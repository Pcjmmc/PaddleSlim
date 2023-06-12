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
                <Row :gutter="16">
                    <Col span="5">
                        <p>模型库分支:</p>
                    </Col>
                    <Col span="19">
                        {{ dealWithBlank('model_branch') }}
                    </Col>
                </Row>
                <Row :gutter="16">
                    <Col span="5">
                        <p>模型库commit号:</p>
                    </Col>
                    <Col span="19">
                        {{ dealWithBlank('model_commit') }}
                    </Col>
                </Row>
                <Row :gutter="16">
                    <Col span="5">
                        <p>框架分支:</p>
                    </Col>
                    <Col span="19">
                        {{ dealWithBlank('frame') }}
                    </Col>
                </Row>
                <Row :gutter="16">
                    <Col span="5">
                        <p>框架commit号:</p>
                    </Col>
                    <Col span="19">
                        {{ dealWithBlank('frame_commit') }}
                    </Col>
                </Row>
                <Row :gutter="16">
                    <Col span="5">
                        <p>批次号:</p>
                    </Col>
                    <Col span="19">
                        {{ dealWithBlank('task_date') }}
                    </Col>
                </Row>
                <Row :gutter="16">
                    <Col span="5">
                        <p>模型链接:</p>
                    </Col>
                    <Col span="5">
                        <a
                        :href="dealWithBlank('script_url')"
                        target="_blank"
                        >
                        {{ dealWithBlank('script_url') }}
                        </a>
                    </Col>
                </Row>
                <Row :gutter="16">
                    <Col span="5">
                        <p>执行脚本:</p>
                    </Col>
                    <Col span="19">
                        <a
                            style="word-wrap: break-word;"
                            href="#"
                            v-on:click="getData('run_model_sh_url'); return false;"
                        >
                        {{ getPartUrl('run_model_sh_url') }}
                        </a>
                    </Col>
                </Row>
                <Row :gutter="16">
                    <Col span="5">
                        <p>paddlecloud-job号:</p>
                    </Col>
                    <Col span="5">
                        <a
                        :href="dealWithBlank('pdc_job_id')"
                        target="_blank"
                        >
                        {{ dealWithBlank('pdc_job_id') }}
                        </a>
                    </Col>
                </Row>
                <Row :gutter="16">
                    <Col span="5">
                        <p>训练日志链接:</p>
                    </Col>
                    <Col span="19">
                        <a
                            style="word-wrap: break-word;"
                            href="#"
                            v-on:click="getData('train_log_url'); return false;"
                        >
                        {{ getPartUrl('train_log_url') }}
                        </a>
                    </Col>
                </Row>
                <Row :gutter="16">
                    <Col span="5">
                        <p>结果日志链接:</p>
                    </Col>
                    <Col span="19">
                        <a
                            style="word-wrap: break-word;"
                            href="#"
                            v-on:click="getData('index_log_url'); return false;"
                        >
                        {{ getPartUrl('index_log_url') }}
                        </a>
                    </Col>
                </Row>
                <Row :gutter="16">
                    <Col span="5">
                        <p>profiler日志链接:</p>
                    </Col>
                    <Col span="19">
                        <a
                            style="word-wrap: break-word;"
                            href="#"
                            v-on:click="getData('profiler_log_url'); return false;"
                        >
                        {{ getPartUrl('profiler_log_url') }}
                        </a>
                    </Col>
                </Row>
                <Row :gutter="16">
                    <Col span="5">
                        <p>下降原因:</p>
                    </Col>
                    <Col span="19">
                        {{ dealWithBlank('down_reason') }}
                    </Col>
                </Row>
                <Row :gutter="16">
                    <Col span="5">
                        <p>波动值:</p>
                    </Col>
                    <Col span="19">
                        {{ dealWithBlank('wave_diff') }}
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
            <el-button
                @click="callDownload"
                icon="el-icon-download"
                autofocus
                size="mini"
                style="margin-right: 5px"
                :loading="downLoadLoading"
            >
            </el-button>
            <pre style="word-wrap: break-word;overflow-y: auto;">{{ modalContent }}</pre>
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
            type: [String],
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
            modalContent: '',
            downLoadLoading: false,
            downloadKey: ''
        };
    },
    mounted: function () {
        this.setModalWidth();
    },
    methods: {
        setModalWidth() {
            this.modalWidth = window.innerWidth * 0.65;
        },
        getPartUrl(key) {
            if (this.info === null || this.info === undefined || !(key in this.info)) {
                return '整体无数据，请重新选择';
            }
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
            if (this.info === null || this.info === undefined || !(key in this.info)) {
                return '暂无数据';
            }
            let params = {
                log_url: this.info[key].split(':')[1]
            };
            if (params.log_url === undefined || params.log_url === '') {
                return;
            }
            const data = await api.get(PaddleVsOtherReadLog, params);
            this.modalContent = data;
            this.$refs.poptip.visible = false;
            this.modal = true;
            this.downloadKey = params.log_url;
        },
        dealWithBlank(key) {
            if (this.info === null || this.info === undefined || !(key in this.info)) {
                return '暂无数据';
            }
            if (this.info[key] === undefined || this.info[key] === '') {
                return '暂无数据';
            } else {
                if (key === 'wave_diff') {
                    if (this.info[key] === '-') {
                        return '-';
                    }
                    let value = (this.info[key] * 100).toFixed(3);
                    return value + '%';
                }
                return this.info[key];
            }
        },
        async callDownload(key) {
            this.downLoadLoading = true;
            let params = {
                log_url: key
            };
            let {data, status} = await api.getLog(PaddleVsOtherReadLog, params);
            if (status === 404 || status === 500) {
                this.$Message.error({
                    content: '请求出错: 下载失败',
                    duration: 30,
                    closable: true
                });
            } else {
                // 获取内容并创建链接
                const content = Buffer.from(data.data);
                const blob = new Blob([content], {type: 'application/octet-stream'});
                const url = URL.createObjectURL(blob);
                const link = document.createElement('a');
                // 获取文件名称
                let filename = key;
                link.href = url;
                link.type = 'application/octet-stream';
                link.setAttribute('download', filename);
                document.body.appendChild(link);
                link.click();
                URL.revokeObjectURL(url);
            }
            this.downLoadLoading = false;
        }
    }
};
</script>