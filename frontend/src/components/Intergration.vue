<template>
  <div>
    <Tabs @on-click="clickTab" :value="tabName">
      <TabPane label="进度" name="10001" icon="ios-list-box">
        <div>
          <div style="margin-bottom: 1.5%">
            <row type="flex" justify="center" align="middle">
              <col>
                <ApiCoverage :percent="54" :total="13" description="成功任务数" content="集中测试整体进度"> </ApiCoverage>
              </col>
            </row>
          </div>
          <div>
            <Divider orientation="left" style="font-size: 0.5em;font-style: italic;"> PaddlePaddle测试信息 </Divider>
          </div>
          <div style="margin-bottom: 1.5%">
            <BaseInfo :repoInfo="repoInfo"> </BaseInfo>
          </div>
          <div v-for="(item, key, index) in integrationData.data" :key="key">
            <Divider orientation="left" style="font-size: 0.6em;font-style: italic;">{{item.scenes}}</Divider>
            <integration-test :data="item.data" :tag="repoInfo.tag" :versionId="repoInfo.version_id" :versionName="repoInfo.name"></integration-test>
          </div>
        </div>
      </TabPane>
      <TabPane label="风险" name="10002" icon="ios-bug">
        <bug-fix :datas="bugData" ref="mychild"></bug-fix>
      </TabPane>
    </Tabs>
  </div>
</template>

<script>
import IntegrationTest from './IntegrationTest.vue';
import BugFix from './BugFix.vue';
import ApiCoverage from './ApiCoverage.vue';
import BaseInfo from './BaseInfo.vue';

export default {
  props: ["repoInfo", "integrationData", "bugData"],
  data: function () {
    return {
      tabName: '10001'
    }
  },
  mounted: function () {
  },
  components: {
    BaseInfo,
    ApiCoverage,
    BugFix,
    IntegrationTest
  },
  computed: {
  },
  methods: {
    clickTab(name) {
      this.tabName = name;
      this.$nextTick(function () {
        this.$refs.mychild.getStatusFilters();
      });
    }
  }
};
</script>

<style scoped>
</style>
