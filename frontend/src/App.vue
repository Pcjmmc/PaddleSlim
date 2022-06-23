<template>
  <div id="main" class="app-main">
    <router-view></router-view>
  </div>
</template>

<script>
  export default {}
</script>

<style>
  html, body {
    width: 100%;
    height: 100%;
    background: #f0f0f0;
    overflow: auto;
  }

  .app-main {
    width: 100%;
    height: 100%;
  }
  .ivu-tooltip-inner {
  max-width: 800px;
  min-height: 34px;
  padding: 8px 12px;
  color: #fff;
  text-align: left;
  text-decoration: none;
  background-color: rgba(70,76,91,.9);
  border-radius: 4px;
  -webkit-box-shadow: 0 1px 6px rgba(0,0,0,.2);
  box-shadow: 0 1px 6px rgba(0,0,0,.2);
  white-space: nowrap;
}
</style>
