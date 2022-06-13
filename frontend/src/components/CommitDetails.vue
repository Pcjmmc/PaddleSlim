
  <template>
    <div>
      <Split v-model="split1">
        <div slot="left" class="center-card-s">
          <div style="margin-bottom: 10px;">
            <p>{{ version }} commit列表 </p>
          </div>
          <div>
            <Timeline>
              <TimelineItem v-for="(item, index) in commitList" v-if="commitList" :key="index">
                <span>
                  <span>
                    {{ item.commit_time }} {{ "(" }}
                  </span>
                  <a
                    class="content"
                    href="javascript:void(0)"
                    @click="setCommit(item.commit)"
                  > {{ item.commit.substring(0, 14) }} </a>
                  {{ ")" }}
                </span>
              </TimelineItem>
            </Timeline>
          </div>
        </div>
        <div
          slot="right"
          class="center-card-s"
          v-if="commitData.length !== 0"
        >
          <p align="center" style="font-size: 16px"> {{ selectCommit }} </p>
          <div :key="index" v-for="(item, index) in commitData">
            <Divider orientation="left" style="font-size: 0.6em;font-style: italic;">{{item.scenes}}</Divider>
            <Table border
              :columns="columns"
              :data="item.data"
            >
            </Table>
          </div>
        </div>
        <div
          slot="right"
          class="center-card-s"
          v-else
        >
          <p align="center" style="font-size: 16px">{{ selectCommit }} 暂无数据 </p>
        </div>
      </Split>
    </div>
</template>

<script>
import Cookies from 'js-cookie';
import api from '../api/index';
import {CommitsUrl, CommitDetailUrl} from '../api/url.js';
import IntegrationTest from './IntegrationTest.vue';
export default {
  name: 'CommitDetails',
  props: {},
  data: function () {
    return {
      search: {
        page: 1,
        pagesize: 20
      },
      columns: [
        {
          title: '任务',
          key: 'tname',
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
            }, params.row.tname)
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
                  color: ['passed', 'success', 'pass'].indexOf(status.toLowerCase()) >= 0 ? 'success' : 'error'
                }
                }, status)
            ]);
          }
        }
      ],
      commitList: [],
      split1: 0.3,
      commitData: [],
      selectCommit: ''
    };
  },
  watch: {
    version: function () {
      this.getData();
    }
  },
  mounted: function () {
    // console.log('this query params', this.queryParams);
    this.getData();
  },
  computed: {
    version: {
      get() {
        return this.$store.state.version;
      }
    }
  },
  components: {
    IntegrationTest
  },
  methods: {
    async getData() {
      let params = {
        version: Cookies.get('version'),
        page: this.search.page,
        pagesize: this.search.pagesize
      }
      const {code, data, msg} = await api.get(CommitsUrl, params);
      if (parseInt(code, 10) === 200) {
        this.commitList = data;
        // console.log('this.commitList', this.commitList);
        this.selectCommit = this.commitList[0];
        this.getCommitDetail();
      } else {
        this.commitList = [];
        this.$Message.error({
          content: '请求出错: ' + msg,
          duration: 30,
          closable: true
        });
      }
    },
    setCommit(commit) {
      this.selectCommit = commit;
      this.getCommitDetail();
    },
    async getCommitDetail() {
      let params = {
        version: Cookies.get('version'),
        commit: this.selectCommit
      }
      const {code, data, msg} = await api.get(CommitDetailUrl, params);
      if (parseInt(code, 10) === 200) {
        this.commitData = data;
      } else {
        this.commitData = [];
        this.$Message.error({
          content: '请求commit详情出错: ' + msg,
          duration: 30,
          closable: true
        });
      }
    },
    jumper(item) {
      // 还是根据任务的type来确定跳转到function还是model，目前暂时都用ApiDetails
      let _params = {
        task_type: item.task_type,
        tid: item.tid,
        build_id: item.build_id,
        secondary_type: item.secondary_type,
        status: item.status,
        exit_code: item.exit_code,
        repo: item.repo,
        branch: item.branch,
        commit_id: item.commit_id,
        tname: item.tname,
        reponame: item.reponame,
        created: item.created
      };
      let detail_name = '';
      if (item.reponame === 'Paddle2ONNX' || item.reponame === 'PaddleHub') {
        detail_name = 'FuncDetail';
      } else if (item.task_type === 'model' || item.task_type === 'benchmark') {
        detail_name = 'model';
      } else if (item.task_type === 'frame') {
        detail_name = 'FuncDetail';
      } else if (item.task_type === 'infer') {
        detail_name = 'FuncDetail';
      } else if (item.task_type === 'dist') {
        // 如果二级分类是api的则跳转api详情页；否则按模型汇聚
        if (item.secondary_type.toLowerCase().includes('api')) {
          detail_name = 'FuncDetail';
        } else {
          detail_name = 'model';
        }
      } else if (item.task_type === 'compile') {
          _params.artifact_url = item.artifact_url;
          detail_name = 'Compile';
      } else {
        return;
      }
      const { href } = this.$router.resolve({name: detail_name, query: _params});
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