<template>
  <div style="margin-top:0.5%;">
    <span :id="moduleid"></span>
    <div >
      <Card class="main-card">
        <p slot="title" style="text-align: left;font-size: 16px;">
          <span> {{ modulename }}</span>
          <span>: 负责人（{{ owner.replace(/,/g, " | ") }}）</span>
          <span style="float: right">最新更新时间: {{ date }} </span>
        </p>
        <Row type="flex" justify="start">
          <Col span="3">
            <div>
              <Button
                type="primary"
                icon="md-add"
                @click="addItem"
                :key="idx"
              >新增风险</Button>
            </div>
          </Col>
        </Row>
        <div v-for="(item, index) in risk" :key="index" style="margin-top:1%;">
          <Card>
            <Form :ref="'addForm' + index" :model="item" :rules="ruleCustom" :label-width="75">
              <Row>
                <Col span="19">
                  <Form-item label="风险:" prop="content">
                    <Input v-model="item.content" placeholder="录入问题描述"/>
                  </Form-item>
                </Col>
                <Col span="3" offset="1">
                  <Button
                    type="primary"
                    icon="md-add"
                    @click="addIcafeItem(index, item.icafe)"
                    :key="idx"
                  >新增卡片</Button>
                <!--
                  <Button type="primary" @click="associateIcafe(index, item.icafe)">关联卡片</Button>
                -->
                </Col>
                <Col span="1">
                  <i class="el-icon-delete" @click="deleteItem(index)"></i>
                </Col>
              </Row>
              <Row>
                <Col span="12">
                  <Form-item label="影响:" prop="influence">
                    <Input v-model="item.influence" placeholder="录入影响面"/>
                  </Form-item>
                </Col>
                <Col span="12" offset="0.5">
                  <Form-item label="PR链接:" prop="pr">
                    <Input v-model="item.pr" placeholder="录入pr"/>
                  </Form-item>
                </Col>
              </Row>
              <Row>
                <Col span="5">
                  <Form-item label="阻塞发版:" prop="important">
                    <Radio-group v-model="item.important">
                      <Radio label="否">
                        <span>否</span>
                      </Radio>
                      <Radio label="是">
                        <span>是</span>
                      </Radio>
                    </Radio-group>
                  </Form-item>
                </Col>
                <Col span="5">
                  <Form-item label="严重程度:" prop="level">
                    <Rate v-model="item.level"></Rate>
                  </Form-item>
                </Col>
                <Col span="8">
                  <Form-item label="风险状态:" prop="status">
                    <el-radio-group v-model="item.status">
                      <el-radio-button label="已解决"></el-radio-button>
                      <el-radio-button label="未解决"></el-radio-button>
                      <el-radio-button label="延期修复"></el-radio-button>
                    </el-radio-group>
                  </Form-item>
                </Col>
                <Col span="6">
                  <Form-item label="风险类型:" prop="type">
                    <el-radio-group v-model="item.type">
                      <el-radio-button label="功能Bug"></el-radio-button>
                      <el-radio-button label="功能Delay"></el-radio-button>
                    </el-radio-group>
                  </Form-item>
                </Col>
              </Row>
              <Row style="margin-top:1%;" v-if="item.icafe.length > 0">
                <Col span="24">
                  <Form-item label="卡片列表:">
                    <base-table :datas="item.icafe" :idx="index" @updataDate="updataDate"></base-table>
                  </Form-item>
                </Col>
              </Row>
            </Form>
          </Card>
        </div>
        <Row style="margin-top:1%;">
          <Form :label-width="75">
            <Col span="24">
              <b><Form-item label="回测进度:">
                目前进行第<Input-number size="small" :max="100" :min="0" v-model="regression.round"></Input-number>轮测试，共有流水线<Input-number size="small" :max="100" :min="0" v-model="regression.total"></Input-number>条，成功<Input-number size="small" :max="100" :min="0" v-model="regression.pass"></Input-number>条，失败<Input-number size="small" :max="100" :min="0" v-model="regression.fail"></Input-number>条，进行中<Input-number size="small" :max="100" :min="0" v-model="regression.running"></Input-number>条。
              </Form-item></b>
            </Col>
          </Form>
        </Row>
        <Row type="flex" justify="center">
          <Col span="3">
            <el-button type="primary" icon="plus-circled" @click="saveData">保存</el-button>
          </Col>
        </Row>
      </Card>
    </div>
    <!--
    <Modal
      width="60%"
      v-model="showIcafe"
      title="关联卡片"
      v-on:on-cancel="cancelShowIcafe"
      >
      <Row type="flex" justify="start">
        <Col span="3">
          <div>
            <Button
              type="primary"
              icon="md-add"
              @click="addIcafeItem"
              :key="idx"
            >新增卡片</Button>
          </div>
        </Col>
      </Row>
      <div style="margin-top: 1%;">
        <Table :columns="columns7" :data="icafe"></Table>
      </div>
    </Modal>
    -->
  </div>

</template>

<script>

import Cookies from 'js-cookie';
import { AddNewConclusionUrl } from '../../api/url.js';
import api from '../../api/index';
import BaseTable from './BaseTable.vue';

export default {
  name: 'NewResult',
  props: {
    idx: {
      type: [Number],
      default: function () {
        return 0;
      }
    },
    date: {
      type: [String],
      default: function () {
        return '';
      }
    },
    moduleid: {
      type: [Number],
      default: function () {
        return 0;
      }
    },
    modulename: {
      type: [String],
      default: function () {
        return '';
      }
    },
    owner: {
      type: [String],
      default: function () {
        return 'xieyunshen';
      }
    },
    risk: {
      type: [Array],
      default: function () {
        return [
        ];
      }
    },
    regression: {
      type: [Object],
      default: function () {
        return {};
      }
    }
  },
  data: function () {
    return {
      showIcafe: false,
      addIcafe: false,
      icafe: [],
      index: -1,
      username: Cookies.get('username'),
      ruleCustom: {
        content: [
          { required: true, message: '请填写问题描述！', trigger: 'blur' }
        ],
        influence: [
          { required: true, message: '请填写影响面！', trigger: 'blur' }
        ]
      }
      // columns7: [
      //   {
      //     title: '标题',
      //     align: 'center',
      //     key: 'title',
      //     render: (h, params) => {
      //       let ret = []
      //       if (params.row.title) {
      //         ret.push(
      //           h('div', [h('a', {
      //           attrs: {
      //             href: 'javascript:void(0)'
      //           },
      //           on: {
      //             click: () => {
      //               this.jumper(params.row.url);
      //             }
      //           }
      //         }, params.row.title)]))
      //       } else {
      //         ret.push(
      //           h("Input", {
      //             props: {
      //               value: params.row.url,
      //               placeholder: '请输入卡片序列号!'
      //             },
      //             on: {
      //               input: val => {
      //                 params.row.url = val;
      //                 // 发送请求，获取相关信息
      //               },
      //               'on-blur': async () => {
      //                 await this.getIcafeInfo(params.index, params.row);
      //               }
      //             }
      //           })
      //         )
      //       }
      //       return h(
      //         'div',
      //         ret
      //       )
      //     }
      //   },
      //   {
      //     title: '负责人',
      //     align: 'center',
      //     key: 'owner'
      //   },
      //   {
      //     title: '操作',
      //     align: 'center',
      //     key: 'operation',
      //     render: (h, params) => {
      //       let ret = []
      //       ret.push(
      //         h(
      //           'Button',
      //           {
      //             props: {
      //               type: 'error',
      //               size: 'small'
      //             },
      //             style: {
      //               marginRight: '5px'
      //             },
      //             on: {
      //               click: () => {
      //                 this.deleteIcafeItem(params.index, params.row);
      //               }
      //             }
      //           },
      //           '删除'
      //         )
      //       )
      //       return h(
      //         'div',
      //         ret
      //       )
      //     }
      //   }
      // ]
    };
  },
  watch: {
  },
  mounted: function () {
  },
  components: {
    BaseTable
  },
  methods: {
    addItem() {
      // 在后面追剧一条新的内容
      this.risk.unshift(
        {
          content: '',
          level: 5,
          important: '否',
          influence: '',
          status: '未解决',
          type: '功能Bug',
          pr: '',
          icafe: []
        }
      );
    },
    deleteItem(index) {
      // 新增1条数据，刚开始是没有id的，是得入库之后产生
      if (this.risk.length < 1) {
        return false;
      }
      this.risk.splice(index, 1);
    },
    addIcafeItem(index, icafe) {
      // 在后面追剧一条新的内容
      this.risk[index].icafe.push(
        {}
      )
    },
    async submit() {
      // 一回车就提交；提交的时候应该提交方向、负责人、以及提交内容等
      // 每次都是新的整体提交内容
      console.log('最后的数据是', this.risk);
    },
    hasPersmission() {
      // 判断负责人跟登陆的人是否一致
      return this.owner === this.username;
    },
    updataDate(idx, icafe) {
      this.$set(this.risk[idx].icafe, icafe);
    },
    async associateIcafe(index, icafe) {
      // 关联icafe todo
      this.index = index;
      this.icafe = icafe;
      this.showIcafe = true;
    },
    jumper(url) {
      // 根据branch获取commit列表
      window.open(url, '_blank');
    },
    cancelShowIcafe() {
      // 关闭窗口 todo
    },
    async saveData() {
      // 循环里面的refs
      let num = 0;
      this.risk.forEach((element, index) => {
        console.log('index is', 'addForm' + index);
        this.$refs['addForm' + index][0].validate((valid) => {
          if (!valid) {
            num++;
            return false;
          }
        })
      })
      console.log('num is', num);
      if (!num) {
        await this.createData();
      }
    },
    async createData() {
      let content = {
        risk: this.risk,
        regression: this.regression
      };
      let params = {
        module_id: this.moduleid,
        content: JSON.stringify(content)
      };
      const {code, data, message} = await api.post(AddNewConclusionUrl, params);
      if (parseInt(code, 10) === 200) {
        // 如果点击保存，这里就保存成今天的日期
        this.$emit('searchByfilter');
        this.$Message.success({
          content: '保存成功',
          duration: 3.3,
          closable: true
        })
        console.log('通过校验，提交数据', params);
      } else {
        this.$Message.error({
          content: '你没有权限修改，请联系负责人！',
          duration: 10,
          closable: true
        })
      }
    }
  }
};
</script>

<style scoped>
.center-card-s {
  width: 100%;
  max-height: 600px;
  overflow: auto;
  margin-bottom: 1%
}
.all-line-row {
  margin-top: 1%;
  margin-bottom: 1%;
  margin-left: 1%;
  margin-right: 1%;
  font-size:14px;
}
.btn-success {
  color: #fff;
  background-color: #67c23a;
  border-color: #67c23a;
}
.main-card {
  border: 1px solid #809399;
  margin-bottom: 20px;
}
.regression-size {
  font-size: 18px;
}
</style>
