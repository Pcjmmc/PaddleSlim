<template>
  <div>
    <div
      v-for="(item, index) in data"
      class="one-fifth-video-col"
    >
      <compileBase
        v-if="item && tabname==='compile'"
        :system="item.system"
        :data="item.data"
        :index="index"
        :tag="tag"
        :latestcommittime="latestcommittime"
        :versionid="versionid"
        :versionname="versionname"
      >
      </compileBase>
      <modelBase
        v-else-if="item && tabname==='model'"
        :system="item.system"
        :data="item.data"
        :index="index"
        :tag="tag"
        :latestcommittime="latestcommittime"
        :versionid="versionid"
        :versionname="versionname"
      >
      </modelBase>
      <expandBase
        v-else
        :system="item.system"
        :data="item.data"
        :index="index"
        :tag="tag"
        :latestcommittime="latestcommittime"
        :versionid="versionid"
        :versionname="versionname"
      >
      </expandBase>
    </div>
  </div>
</template>
<script>

import expandBase from './Base/expandBase.vue';
import modelBase from './Base/modelBase.vue';
import compileBase from './Base/compileBase.vue';

export default {
  props: {
    data: {
      type: [Array],
      default: function () {
        return [];
      }
    },
    tag: {
      type: [String],
      default: ''
    },
    versionid: {
      type: [Number],
      default: function () {
        return null;
      }
    },
    latestcommittime: {
      type: [Number],
      default: function () {
        return null;
      }
    },
    versionname: {
      type: [String],
      default: ''
    },
    secondtype: {
      type: [Array],
      default: function () {
        return [];
      }
    },
    tabname: {
      type: [String],
      default: ''
    }
  },
  data: function () {
    return {
    }
  },
  methods: {
    setColor(status) {
      let _status = status.toLowerCase();
      switch (_status) {
        case 'pass':
          return 'green';
        case 'warning':
          return 'yellow';
        default:
          return 'red';
      }
    }
  },
  components: {
    expandBase,
    compileBase,
    modelBase
  },
  mounted: function () {
    // console.log('secondtype', this.tabname);
    // console.log('this data', this.data);
  }
};
</script>

<style scoped>
  .one-fifth-video-col {
    margin-right: 2%;
    margin-left: 2%;
    margin-bottom: 0.5%;
  }
</style>
