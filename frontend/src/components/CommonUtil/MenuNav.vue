<template>
    <div style="display: inline;">
        <template v-for="(value, key, index) in data">
            <template v-if="!value.notMenu">
                <template v-if="value.sub && value.sub.length !== 0 && value.multiLayer">
                  <menuItem :name="computeName(index)">
                    <span @click="openNewPage(key)">
                      <Icon
                        size="18"
                        v-if="value.icon"
                        :type="value.icon"
                      ></Icon>
                      {{ value.desc }}
                      <Icon
                        size="18"
                        type="md-arrow-dropright"
                        slot="reference"
                      />
                    </span>
                  </menuItem>
                </template>
                <template v-else-if="value.sub && value.sub.length !== 0">
                  <Submenu
                    :key="index"
                    :name="computeName(key)"
                  >
                      <template slot="title">
                        <Icon
                          size="18"
                          :type="value.icon"
                          v-if="value.icon"
                        ></Icon>
                        {{ value.desc }}
                      </template>
                      <menu-nav
                          :data="value.sub"
                          :father-name="computeName(index)"
                          :father-link="computeLink(key)"
                      ></menu-nav>
                  </Submenu>
                </template>
                <router-link
                    v-else
                    :key="index"
                    :to="computeLink(key)"
                >
                    <menuItem :name="computeName(index)">
                        <Icon
                          size="18"
                          v-if="value.icon"
                          :type="value.icon"
                        ></Icon>
                        {{ value.desc }}
                    </menuItem>
                </router-link>
            </template>
        </template>
    </div>
</template>

<script>
export default {
  name: 'menuNav',
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
    }
  },
  data: function() {
    return {
    }
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
    },
    openNewPage(value) {
      let uri = this.computeLink(value);
      this.$store.commit('changeChildMenu', uri);
      this.$store.commit('changeOpenStatus', true);
    }
  }
};
</script>

