<template>
    <div class="center-card-s">
        <div style="margin-top: 2%">
            <Row
                type="flex"
                align="middle"
                :gutter="16"
            >
                <Col span="1.5">
                    <h4>对比规则：</h4>
                </Col>
                <Col span="6">
                    <el-radio-group
                        v-model="rule"
                        border
                        size="small"
                    >
                        <span
                            :key="index"
                            :value="item.id"
                            v-for="(item, index) in contrastRules"
                        >
                            <el-radio-button v-bind:label="item.title"></el-radio-button>
                        </span>
                    </el-radio-group>
                </Col>
            </Row>
            <Row
                type="flex"
                align="middle"
                :gutter="24"
                style="margin-top: 1%"
            >
                <Col span="1.5">
                    <h4>对比指标:</h4>
                </Col>
                <Col span="6">
                    <el-radio-group
                        v-model="rule"
                        border
                        size="small"
                    >
                        <span
                            :key="index"
                            :value="item.id"
                            v-for="(item, index) in tags"
                        >
                            <el-radio-button v-bind:label="item.id"></el-radio-button>
                        </span>
                    </el-radio-group>
                </Col>
            </Row>
            
           
            
        </div>
    </div>
</template>

<script>

export default {
    name: 'PaddleComparision',
    data: function () {
        return {
            contrastRules: [
                {
                    title: '相同配置对比',
                    id: 'sameConfig',
                    checked: true
                },
                {
                    title: '动转静比动态图',
                    id: 'dynamic',
                    checked: false
                },
                {
                    title: 'FP16比FP32',
                    id: 'fp',
                    checked: false
                }
            ],
            tags: [
                {
                    id: 'ips',
                    checked: true
                },
                {
                    id: 'gpu_mem',
                    checked: false
                },
                {
                    id: 'cpu_use',
                    checked: false
                },
                {
                    id: 'gpu_use',
                    checked: false
                },
                {
                    id: 'accuracy',
                    checked: false
                }
            ],
            rule: '',
            tag: ''
        }
    }
}
</script>

<style scoped>
.center-card-s {
  margin-left: 1%;
  margin-right: 1%;
  font-size: 14px;
  color: lightslategrey;
}

</style>