<template>
  <div>
    <Card>
      <Form :ref="'addForm' + index" :model="item" :label-width="75">
        <Row>
          <Col span="18">
            <Form-item label="风险:" prop="content">
            <Input readonly v-model="item.content" placeholder="录入问题描述"/>
            </Form-item>
          </Col>
        </Row>
        <Row>
          <Col span="9">
            <Form-item label="影响:" prop="influence">
            <Input readonly v-model="item.influence" placeholder="录入影响面"/>
            </Form-item>
          </Col>
          <Col span="9" offset="0.5">
            <Form-item label="PR链接:" prop="pr">
            <Input readonly v-model="item.pr" placeholder="录入pr"/>
            </Form-item>
          </Col>
        </Row>
        <Row>
          <Col span="4">
            <Form-item label="阻塞发版:" prop="important">
              <Radio-group v-model="item.important">
                <Radio :label="item.important">
                </Radio>
              </Radio-group>
            </Form-item>
          </Col>
          <Col span="7">
            <Form-item label="严重程度:" prop="level">
              <Rate disabled v-model="item.level"></Rate>
            </Form-item>
          </Col>
          <Col span="4">
            <Form-item label="状态:" prop="status">
              <el-radio-group v-model="item.status">
                <el-radio-button :label="item.status"></el-radio-button>
              </el-radio-group>
            </Form-item>
          </Col>
          <Col span="4">
            <Form-item label="类型:" prop="type">
              <el-radio-group v-model="item.type">
                <el-radio-button :label="item.type"></el-radio-button>
              </el-radio-group>
            </Form-item>
          </Col>
        </Row>
        <Form-item label="卡片列表:" v-if="item.icafe.length > 0">
          <div v-for="(it, id) in item.icafe">
            <Row style="margin-top:1%;" >
              <Col span="22">
                <a :href="it.url"> {{ it.title }} </a> @{{ it.owner }}
              </Col>
            </Row>
          </div>
        </Form-item>
      </Form>
    </Card>
  </div>
</template>
<script>

export default {
  name: 'DescDetail',
  props: {
    index: {
      type: [Number],
      default: function () {
        return 0;
      }
    },
    item: {
      type: [Object],
      default: function () {
        return {};
      }
    }
  },
  data: function () {
    return {
      columns7: [
        {
          title: '标题',
          align: 'center',
          key: 'title',
          render: (h, params) => {
            let ret = []
            if (params.row.title) {
              ret.push(
                h('div', [h('a', {
                attrs: {
                  href: 'javascript:void(0)'
                },
                on: {
                  click: () => {
                    this.jumper(params.row.url);
                  }
                }
              }, params.row.title)]))
            } else {
              ret.push(
                h("Input", {
                  props: {
                    value: params.row.url,
                    placeholder: '请输入卡片序列号!'
                  },
                  on: {
                    input: val => {
                      params.row.url = val;
                      // 发送请求，获取相关信息
                    },
                    'on-blur': async () => {
                      await this.getIcafeInfo(params.index, params.row);
                    }
                  }
                })
              )
            }
            return h(
              'div',
              ret
            )
          }
        },
        {
          title: '负责人',
          align: 'center',
          key: 'owner'
        }
      ]
    };
  },
  watch: {
  },
  mounted: function () {
  },
  components: {
  },
  methods: {
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
.ivu-form-item{
  margin-bottom: 6px;
  font-size: 14px;
}
</style>
