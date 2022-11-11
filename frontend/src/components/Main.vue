<template>
  <div>
    <Layout>
      <Header style="height:50px">
        <Menu mode="horizontal" theme="dark" style="height:50px">
          <div style="float:left;" class="fontsize">
            <p><font>PaddleTest</font></p>
          </div>
          <div style="float: right;">
            <MenuItem name="1">
              <div>
                <Dropdown
                  transfer
                  trigger="click"
                  v-on:on-click="handleClickApp"
                >
                  <a href="javascript:void(0)">
                    <span class="main-user-name">{{ appname }}</span>
                    <Icon type="md-arrow-dropdown"></Icon>
                  </a>
                  <DropdownMenu slot="list">
                    <DropdownItem name="changeApp"> 更换产品 </DropdownItem>
                  </DropdownMenu>
                </Dropdown>
              </div>
            </MenuItem>
            <MenuItem name="2" v-if="username">
              <div>
                <Dropdown
                  transfer
                  trigger="click"
                  v-on:on-click="handleClickUser"
                >
                  <a href="javascript:void(0)">
                    <img :src="avater" class="img-css">
                      <span>{{ username }}</span>
                    <img>
                    <Icon type="md-arrow-dropdown"></Icon>
                  </a>
                  <DropdownMenu slot="list">
                    <DropdownItem name="logout"> 退出 </DropdownItem>
                  </DropdownMenu>
                </Dropdown>
              </div>
            </MenuItem>
          </div>
        </Menu>
      </Header>
      <Layout>
        <Sider
          :style="{
            overflow: 'auto',
            height: '100vh',
            position: 'sticky',
            top: 0,
            left: 0
          }"
          ref="side1"
          hide-trigger collapsible 
          :collapsed-width="78" 
          v-model="isCollapsed"
        >
          <Menu theme="light" style="width:auto;height:100%" :class="menuitemClasses">
            <el-dropdown v-if="appid==1">
              <el-button style="width:200px">
                {{ option }}<i class="el-icon-arrow-down el-icon--right"></i>
              </el-button>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item
                  :key="index"
                  @click.native="handleClickTag(item)" 
                  v-for="(item, index) in verisonList"
                >
                {{ item.desc }}
              </el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
            <menu-nav :data="menuDesc" father-link="/paddle"></menu-nav>
            <div style="position:absolute;bottom:0px;right:0px">
              <div v-if="isCollapsed">
                <el-button type="text" icon="el-icon-s-unfold" @click="collapsedSider"></el-button>
              </div>
              <div v-else>
                <el-button type="text" icon="el-icon-s-fold" @click="collapsedSider"></el-button>
              </div>
            </div>
          </Menu>
        </Sider>
        <Layout class="main-layout-content">
          <Content
            :style="{
                minHeight: currentPageMinHeight,
                maxHeight: currentPageMaxHeight,
                position: 'relative',
                background: '#fff',
                overflow: 'hidden'}"
            >
              <!--渲染视图-->
              <router-view ref="" class="view"></router-view>
            </Content>
        </Layout>
      </Layout>
    </Layout>
  </div>
</template>

<script>
import Cookies from 'js-cookie';
import { MenuInfoUrl, LogoutUrl } from '../api/url.js';
import api from "../api/index";
import MenuNav from './CommonUtil/MenuNav.vue';
export default {
  data: function () {
    return {
      isCollapsed: false,
      page: {
        page: 1,
        size: 50
      },
      username: Cookies.get('username'),
      avater: Cookies.get('avater'),
      appid: Cookies.get('appid'),
      appname: Cookies.get("appname"),
      menuDesc: {},
      verisonList: [],
      option: '',
      currentPageMinHeight: '861px',
      currentPageMaxHeight: ''
    };
  },
  computed: {
    BreadcrumbDescArr() {
      const pathItemArr = this.$route.path.split('/');
      let menuDict = Object.assign({}, this.menuDesc);
      let menuItemArr = [];
      for (var i = 0; i < pathItemArr.length; i++) {
        const pathItem = pathItemArr[i];
        if (pathItem && isNaN(pathItem) && menuDict.hasOwnProperty(pathItem)) {
          menuItemArr.push(menuDict[pathItem].desc);
          menuDict = menuDict[pathItem].sub;
        }
      }
      return menuItemArr;
    },
    rotateIcon () {
      return [
        'menu-icon',
        this.isCollapsed ? 'rotate-icon' : ''
      ];
    },
    menuitemClasses () {
      return [
        'menu-item',
        this.isCollapsed ? 'collapsed-menu' : ''
      ]
    },
    versionName: {
      get() {
        return this.$store.state.version;
      }
    }
  },
  components: {
    MenuNav
  },
  watch: {
    versionName: function () {
      this.option = this.versionName;
    }
  },
  mounted: async function () {
    this.appname = Cookies.get('appname');
    this.username = Cookies.get('username');
    this.avater = Cookies.get('avater');
    this.setUserInfo();
    await this.getMenu();
  },
  async created() {
    this.$root.Hub.$on('update-user-name', () => {
      this.appname = Cookies.get('appname');
      // this.username = Cookies.get('username');
    });
    await this.getMenu();
  },
  methods: {
    handleClickTag (item) {
      this.option = item.desc;
      this.$store.commit('changeVersion', this.option);
    },
    async handleClickUser(item) {
      // 清理cookie 跳转登出
      Cookies.remove('username');
      Cookies.remove('avater');
      Cookies.remove('userid');
      await api.get(LogoutUrl);
      // 将cookie清理掉，并跳转到登出页面
    },
    handleClickApp(name) {
      Cookies.remove('appid');
      Cookies.remove('appname');
      this.$store.commit('removeCurrentApp');
      this.$router.push({path: '/app_store'});
    },
    collapsedSider() {
      this.$refs.side1.toggleCollapse();
    },
    setUserInfo() {
      this.$store.commit('changeUserName', this.username);
      this.$store.commit('changeAvater', this.avater);
    },
    async getMenu() {
      // 根据appid实时获取menu菜单; 各自定义各自的菜单
      let params = {
        appid: Cookies.get("appid"),
        appname: Cookies.get("appname")
      };
      const { code, data } = await api.get(MenuInfoUrl, params);
      this.menuDesc = data;
      // 暂时定义menu
      this.verisonList = this.menuDesc["version"];
      if (this.$route.params && this.$route.params.version) {
        this.option = this.$route.params.version;
        Cookies.set('version', this.option);
        this.$store.commit('changeVersion', this.option);
      } else if (this.$store.state.version) {
        this.option = this.$store.state.version;
        Cookies.set('version', this.option);
      } else {
        this.option = this.verisonList[1].desc;
        Cookies.set('version', this.option);
        this.$store.commit('changeVersion', this.option);
      }
      this.$delete(this.menuDesc, 'version');
    }
  }
}
</script>
<style scoped>
  .layout{
    border: 1px solid #d7dde4;
    background: #f5f7f9;
    position: relative;
    border-radius: 4px;
    overflow: hidden;
  }
  .layout-header-bar{
    background: #fff;
  }
  .layout-logo-left{
    width: 90%;
    height: 30px;
    background: #5b6270;
    border-radius: 3px;
    margin: 15px auto;
  }
  .menu-icon{
    transition: all .3s;
  }
  .footer{
    right: 0;
    bottom: 0;
  }
  .rotate-icon{
    transform: rotate(-90deg);
  }
  .menu-item span{
    display: inline-block;
    overflow: hidden;
    width: 69px;
    text-overflow: ellipsis;
    white-space: nowrap;
    vertical-align: bottom;
    transition: width .2s ease .2s;
  }
  .fontsize {
    font-size: 22px;
    font-weight: bold;
    font-family: "楷体";
    /*background-image: linear-gradient(top, orange, purple);*/
    background-image: -webkit-linear-gradient(right, green, yellow, red);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  .user-dropdown {
    &-menu-con {
      /*position: absolute;*/
      /*right: 0;*/
      /*top: 0;*/
      /*width: auto;*/
      /*height: 100%;*/
      .main-user-name {
          display: inline-block;
          word-break: keep-all;
          white-space: nowrap;
          vertical-align: middle;
          overflow: hidden;
          text-overflow: ellipsis;
          text-align: right;
          font-size: 12px;
      }
    }
    &-innercon {
        height: 100%;
        padding-right: 14px;
    }
}
  .menu-item i{
    transform: translateX(0px);
    transition: font-size .2s ease, transform .2s ease;
    vertical-align: middle;
    font-size: 16px;
  }
  .collapsed-menu span{
    width: 0px;
    transition: width .2s ease;
  }
  .collapsed-menu i{
    transform: translateX(5px);
    transition: font-size .2s ease .2s, transform .2s ease .2s;
    vertical-align: middle;
    font-size: 22px;
  }
  .user-dropdown-menu-con {
    display: inline-block;
  }
  .main-layout-content {
    /*padding: 7px 9px 24px 9px;*/
    /*width: 80%;*/
    /*margin-top: 54px;*/
    /*margin-left: 198px;*/

    width: auto;
  }
  .img-css {
    display: inline-block;
    word-break: keep-all;
    white-space: nowrap;
    vertical-align: middle;
    overflow: hidden;
    text-overflow: ellipsis;
    text-align: right;
    width: 24px;
    height: 24px;
    border-radius: 24px;
  }
</style>