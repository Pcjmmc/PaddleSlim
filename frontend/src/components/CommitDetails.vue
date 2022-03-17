
  <template>
    <div>
      <Split v-model="split1">
        <div slot="left" class="center-card-s">
          <div style="margin-bottom: 10px;">
            <p>{{queryParams.branch}} 覆盖的commit列表</p>
          </div>
          <div>
            <Timeline>
              <TimelineItem v-for="(item, index) in commitList" v-if="commitList" :key="index">
                <a class="content" href="javascript:void(0)" @click="setCommit(item)">{{item}}</a>
              </TimelineItem>
            </Timeline>
          </div>
        </div>
        <div slot="right" class="center-card-s">
          <div v-for="(item, key, index) in commitData.data" :key="key">
            <Divider orientation="left" style="font-size: 0.6em;font-style: italic;">{{item.scenes}}</Divider>
            <Table border
              :columns="columns"
              :data="item.data"
            >
            </Table>
          </div>
        </div>
      </Split>
    </div>
</template>

<script>

import IntegrationTest from './IntegrationTest.vue';
export default {
  name: 'CommitDetails',
  props: {},
  data: function () {
    return {
      columns: [
        {
          title: '任务',
          key: 'description',
          align: 'center',
          render: (h, params) => {
            return h('div', [h('a', {
              attrs: {
                href: 'javascript:void(0)'
              },
              on: {
                click: () => {
                  this.jumper(params.row);
                }
              }
            }, params.row.description)
            ]);
          }
        },
        {
          title: '状态',
          key: 'status',
          align: 'center',
          render: (h, params) => {
            const { status } = params.row;
            return h('div', [
                h('Tag', {
                props: {
                    color: ['pass', 'success'].indexOf(status.toLowerCase()) >= 0 ? 'green' : 'red'
                }
                }, status)
            ]);
          }
        }
      ],
      queryParams: {},
      commitList: [],
      split1: 0.3,
      commitData: '',
      selectCommit: ''
    };
  },
  mounted: function () {
    this.queryParams = this.$route.query;
    console.log('this query params', this.queryParams);
    this.getData();
    this.getCommitDetail();
    this.selectCommit = this.commitList[0];
    console.log('the selected commit is', this.selectCommit);
  },
  computed: {
  },
  components: {
    IntegrationTest
  },
  methods: {
    async getData() {
      let params = {
        branch: this.queryParams.branch
      }
      console.log('begin  search commit list  by branch and time');
      this.commitList = [
        '0ee230a7d3177f791d2a5388ab4dffdccc03f4aa',
        'e764cde64563d4ebd5ce822840a80b06e2081298',
        'ac744db1733165912b068db1c7f151dfc8a0bae7',
        '397781f1a140e93cd5f84ab6f3a876213bc426a7',
        'b031c389938bfa15e15bb20494c76f86289d77b0',
        '4a63d68eebaf8d33980509532ab45e78f6eff7b3',
        '27774eecf00dcd5ee56d2139349d33138770c8da',
        '27774eecf00dcd5ee56d2139349d33138770c8da',
        '5925b82e06dd1fc3ef9499353a89b91da6974df4',
        'aebc5a9c02a8462aa25e5981f71c8378a15d9932',
        '7e21ac92717d6f710268b64fae0cc541c15ae3a2',
        '4cd8a78ad72551ce2055e9acb6ca169099ed051c',
        '4d4a9c6c817ceed5e8510984380c4651336fe9c0',
        '5b6d834dee56c84ba9e59aad646e1286bc47451d',
        'ad92fa611a8737836c04e310bf7a6a50d8176ddb',
        '0d081cbc774008d837877c91426ef9abc07b1b84',
        '52679889d6d919d2062bd4a5520c3e14aaf003db',
        'a6b1c4c12b767f1d421b5e5a829d901738d5209e',
        '1e8432f24b846f3bfce8490cff1374aff6e96bfc',
        'a6b1c4c12b767f1d421b5e5a829d901738d5209e',
        '1e8432f24b846f3bfce8490cff1374aff6e96bfc',
        'a6b1c4c12b767f1d421b5e5a829d901738d5209e',
        '1e8432f24b846f3bfce8490cff1374aff6e96bfc',
        'a6b1c4c12b767f1d421b5e5a829d901738d5209e',
        '1e8432f24b846f3bfce8490cff1374aff6e96bfc'
      ];
    },
    setCommit(commit) {
      this.selectCommit = commit;
      console.log('the selected commit is', this.selectCommit);
      this.getCommitDetail();
    },
    async getCommitDetail() {
      let params = {
        branch: this.queryParams.branch,
        commit: this.selectCommit
      }
      console.log('get commit task info by branch and commit');
      if (this.selectCommit == '0ee230a7d3177f791d2a5388ab4dffdccc03f4aa') {
        this.commitData = {
          data: [
            {
              'scenes': '基础框架测试',
              'data': [
                {
                  'description': 'Ubuntu、Cuda11下基础框架测试(python38)',
                  'tname': 'GpuV100_LinuxUbuntu_Gcc82_Cuda11.0_Trton_Py38_FuncTest_Framework',
                  'status': 'fail'
                },
                {
                  'description': 'Ubuntu、Cuda10.2下基础框架测试(python37)',
                  'tname': 'GpuV100_LinuxUbuntu_Gcc82_Cuda10.2_Trton_Py37_FuncTest_Framework',
                  'status': 'fail'
                },
                {
                  'description': '基础框架测试(python38)',
                  'tname': 'Master_Cpu_Avx2_LinuxUbuntu_Gcc82_Mkl_Py37_FuncTest_Framework_H',
                  'status': 'fail'
                },
                {
                  'description': '基础框架测试(python37)',
                  'tname': 'Master_Cpu_Avx512_LinuxUbuntu_Gcc82_Mkl_Py38_FuncTest_Framework_H',
                  'status': 'fail'
                },
                {
                  'description': '基础框架测试(python36)',
                  'tname': 'Master_Xpu_Py36_FuncTest_Framework_H',
                  'status': 'pass'
                },
                {
                  'description': '基础框架回归(python38)',
                  'tname': 'Cpu_Mac_Openblas_Py38_FuncTest_Framework_H',
                  'status': 'pass'
                },
                {
                  'description': '基础框架回归(python39)',
                  'tname': 'Cpu_Mac_Openblas_Py39_FuncTest_Framework_H',
                  'status': 'fail'
                },
                {
                  'description': '基础框架回归(python36)',
                  'tname': 'Master_Cpu_Noavx_Win_Openblas_Py36_FuncTest_Inference_H',
                  'status': 'pass'
                }
              ]
            },
            {
              scenes: '模型套件测试',
              data: [
                {
                  'description': '模型套件Rec功能回归(python39)',
                  'tname': 'PaddleRec-Py39-Mac-ModelTest-All-D-develop',
                  'status': 'running',
                  'left_time': '2h:04m left'
                },
                {
                  'description': '模型套件NLP功能回归(python39)',
                  'tname': 'PaddleNLP_Py39_Mac_ModelTest_P0_D',
                  'status': 'pass'
                },
                {
                  'description': '模型套件NLP功能回归(python39)',
                  'tname': 'PaddleNLP_Py39_Mac_ModelTest_P0_D',
                  'status': 'pass'
                }
              ]
            }
          ]
        };
      } else {
        this.commitData = {
          data: [
            {
              'scenes': '基础框架测试',
              'data': [
                {
                  'description': 'Ubuntu、Cuda11下基础框架测试(python38)',
                  'tname': 'GpuV100_LinuxUbuntu_Gcc82_Cuda11.0_Trton_Py38_FuncTest_Framework',
                  'status': 'fail'
                },
                {
                  'description': '基础框架测试(python36)',
                  'tname': 'Master_Xpu_Py36_FuncTest_Framework_H',
                  'status': 'pass'
                },
                {
                  'description': '基础框架回归(python38)',
                  'tname': 'Cpu_Mac_Openblas_Py38_FuncTest_Framework_H',
                  'status': 'pass'
                },
                {
                  'description': '基础框架回归(python39)',
                  'tname': 'Cpu_Mac_Openblas_Py39_FuncTest_Framework_H',
                  'status': 'fail'
                },
                {
                  'description': '基础框架回归(python36)',
                  'tname': 'Master_Cpu_Noavx_Win_Openblas_Py36_FuncTest_Inference_H',
                  'status': 'pass'
                }
              ]
            },
            {
              scenes: '模型套件测试',
              data: [
                {
                  'description': '模型套件Rec功能回归(python39)',
                  'tname': 'PaddleRec-Py39-Mac-ModelTest-All-D-develop',
                  'status': 'running',
                  'left_time': '2h:04m left'
                },
                {
                  'description': '模型套件NLP功能回归(python39)',
                  'tname': 'PaddleNLP_Py39_Mac_ModelTest_P0_D',
                  'status': 'pass'
                },
                {
                  'description': '模型套件NLP功能回归(python39)',
                  'tname': 'PaddleNLP_Py39_Mac_ModelTest_P0_D',
                  'status': 'pass'
                }
              ]
            },
            {
              scenes: '预测阶段测试',
              data: [
                {
                  'description': '模型套件Rec功能回归(python39)',
                  'tname': 'PaddleRec-Py39-Mac-ModelTest-All-D-develop',
                  'status': 'running',
                  'left_time': '2h:04m left'
                },
                {
                  'description': '模型套件NLP功能回归(python39)',
                  'tname': 'PaddleNLP_Py39_Mac_ModelTest_P0_D',
                  'status': 'pass'
                },
                {
                  'description': '模型套件NLP功能回归(python39)',
                  'tname': 'PaddleNLP_Py39_Mac_ModelTest_P0_D',
                  'status': 'pass'
                }
              ]
            }
          ]
        };
      }
    },
    jumper(item) {
      // 还是根据任务的type来确定跳转到function还是model，目前暂时都用ApiDetails
      let _params = {};
      _params = Object.assign(_params, item);
      const { href } = this.$router.resolve({name: 'ApiDetails', query: _params});
      window.open(href, '_blank');
    }
  }
};
</script>
<style scoped>
.center-card-s {
  width: 98%;
  max-height: 861px;
  overflow:auto;
  margin-bottom: 2%
}
</style>