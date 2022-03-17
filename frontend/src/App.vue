<template>
  <div class="layout">
    <Layout class="main-layout">
        <Sider ref="side1" hide-trigger collapsible :collapsed-width="78" v-model="isCollapsed">
          <Menu theme="dark" width="auto" :class="menuitemClasses">
            <menu-nav :data="menuDesc" father-link="/paddle"></menu-nav>
          </Menu>
        </Sider>
        <Layout>
          <Header :style="{padding: 0}" class="layout-header-bar">
            <Menu mode="horizontal" theme="light"> 
              <div class="layout-logo"></div>
              <div class="layout-nav">
                <MenuItem name="1">
                  <Icon @click.native="collapsedSider" :class="rotateIcon" type="md-menu" size="24"></Icon>
                </MenuItem>
                <MenuItem style="float: right;" name="2">
                  <div class="user-dropdown-menu-con">
                    <Dropdown transfer trigger="click" @on-click="handleClickUser">
                      <a href="javascript:void(0)" class="fontsize">
                        <span class="main-user-name">{{ userName }}</span>
                        <Icon type="md-arrow-dropdown"></Icon>
                      </a>
                      <DropdownMenu slot="list">
                        <DropdownItem name="logout">修改密码</DropdownItem>
                        <DropdownItem name="logout">退出登录</DropdownItem>
                      </DropdownMenu>
                    </Dropdown>
                  </div>
                </MenuItem>
              </div>
            </Menu>
          </Header>
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
  </div>
</template>

<script>
// import { menuDesc } from './util/common.js';
import { MenuInfoUrl } from './api/url.js';
import api from "./api/index";
import MenuNav from './components/CommonUtil/MenuNav.vue';
export default {
  data: function () {
    return {
      isCollapsed: false,
      page: {
        page: 1,
        size: 50
      },
      userName: '',
      menuDesc: {},
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
    }
  },
  components: {
    MenuNav
  },
  mounted: function () {
    this.userName = this.$cookies.get('username');
    this.userName = 'liuhuanling';
    this.getMenu();
  },
  created() {
    this.$root.Hub.$on('update-user-name', () => {
      this.userName = this.$cookies.get('username');
      this.userName = 'liuhuanling';
    });
    this.getMenu();
  },
  methods: {
    handleClickUser (name) {
      console.log('click log out');
    },
    collapsedSider () {
      this.$refs.side1.toggleCollapse();
    },
    async getMenu () {
      // 负责动态从数据库获取menu,因为menu在实时变化
      const { code, data } = await api.get(MenuInfoUrl);
      console.log("menudat", data)
      this.menuDesc = data;
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
  .main-header-nav {
    position: fixed;
    left: 0px;
    top: 0px;
    width: 100%;
    z-index: 20;
  }
  .user-dropdown-menu-con {
    display: inline-block;
  }
  .main-layout {
  /*padding: 7px 9px 24px 9px;*/
  /*width: 80%;*/
  /*margin-top: 54px;*/
  /*margin-left: 198px;*/

  width: 100%;
  min-height: 861px;
  overflow:auto;
}
</style>