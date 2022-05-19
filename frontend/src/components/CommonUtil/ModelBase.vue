<template>
    <div
        style="margin-bottom: 10px;"
    >
        <Tag style="font-size:15px">模型名: {{ modelName }} </Tag>
        <Tag
          v-if="status.toLowerCase()=='passed'"
          style="font-size:15px"
          color="success"
        >模型状态: {{ status }} </Tag>
        <Tag
          style="font-size:15px"
          color="error"
          v-else
        >模型状态: {{ status }} </Tag>
        <Table
          border
          size="small"
          :columns="Columns"
          :data="kpis"
          style="margin-right: 2%;"
        >
        </Table>
    </div>
</template>

<script>
import DetailBase from './DetailBase.vue';

export default {
  name: 'ModelBase',
  props: {
    'modelName': {
      type: [String],
      default: function () {
        return '';
      }
    },
    'kpis': {
      type: [Array],
      default: function () {
        return [];
      }
    },
    'status': {
      type: [String],
      default: function () {
        return '';
      }
    }
  },
  data: function () {
    return {
      Columns: [
        {
          type: 'expand',
          width: 50,
          render: (h, params) => {
            // console.log('params', this.modelName);
            return h(DetailBase, {
                props: {
                    kpis: params.row.data
                }
            });
          }
        },
        {
          title: '阶段名',
          key: 'step_name',
          align: 'center'
        },
        {
          title: '状态',
          key: 'status',
          align: 'center'
        }
      ]
    };
  },
  mounted: function () {
  },
  components: {
  },
  methods: {
  }
};
</script>