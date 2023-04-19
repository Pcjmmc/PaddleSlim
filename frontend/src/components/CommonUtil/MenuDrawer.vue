<template>
  <div>
    <Menu ref="myMenu" style="height:100%;" :open-names="openeds">
      <span v-for="(value, key, index) in data">
        <template v-if="value.sub && value.sub.length !== 0">
          <Submenu :index="key" :name="key">
            <template slot="title">
              {{ value.desc }}
            </template>
            <menu-drawer
              :data="value.sub"
              :father-name="computeName(index)"
              :father-link="computeLink(key)"
              :openeds="openeds"
            ></menu-drawer>
          </Submenu>
        </template>
        <router-link
          :key="index"
          :to="computeLink(key)"
          v-else
        >
          <MenuItem :name="computeName(index)">
            {{ value.desc }}
          </MenuItem>
        </router-link>
      </span>
    </Menu>
  </div>
</template>

<script>
import MenuNav from './MenuNav.vue';
export default {
  name: 'menuDrawer',
  props: {
    'data': {
      type: Object,
      default: null
    },
    'fatherName': {
      type: String,
      default: ''
    },
    'fatherLink': {
      type: String,
      default: ''
    },
    openeds: {
      type: Array,
      default: function () {
        return [];
      }
    }
  },
  data: function () {
    return {
    }
  },
  watch: {
    openeds() {
      this.$nextTick(() => {
        this.$refs.myMenu.updateOpened();
        this.$refs.myMenu.updateActiveName();
      })
    }
  },
  computed: {
  },
  components: {
  },
  methods: {
    computeName: function (index) {
      if (this.fatherName) {
        return `${this.fatherName}-${index + 1}`;
      } else {
        return `${index + 1}`;
      }
    },
    computeLink: function (key) {
      if (this.fatherLink) {
        if (key === 'publish' || key === 'integration') {
          // let branch = encodeURIComponent(this.$store.state.version);
          let branch = this.$store.state.version.replace('/', "-");
          return `${this.fatherLink}/${key}/${branch}`;
        } else {
          return `${this.fatherLink}/${key}`;
        }
      } else {
        return `/${key}`;
      }
    }
  }
};
</script>
<style scoped>
</style>