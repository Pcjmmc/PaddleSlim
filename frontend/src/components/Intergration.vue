<template>
  <div>
    <Tabs value="name1">
      <TabPane label="进度" name="name1" icon="ios-list-box">
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
      <TabPane label="风险" name="name2" icon="ios-bug">
        <div>
          <bug-fix :data="bugData.data"></bug-fix>
        </div>
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
    }
  },
  mounted: function () {

  },
  watch: {

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
  }
};
</script>

<style scoped>
</style>
