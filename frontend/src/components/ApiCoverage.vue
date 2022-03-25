<template>
  <div style="width: 500px;height: 280px;" align="middle">
    <i-circle
      dashboard
      :size="280"
      :trail-width="4"
      :stroke-width="5"
      :percent="percent"
      stroke-linecap="square"
      stroke-color="#43a3fb">
      <div class="demo-Circle-custom">
        <p>{{description}}</p>
        <span>
          占总数
          <i>{{total}}</i>
          的
          <i>{{percent}}%</i>
        </span>
      </div>
    </i-circle>
    <div align="middle">
      <p>{{content}}</p>
    </div>
  </div>
</template>
<script>
export default {
  props: ["percent", "total", "description", "content"]
};
</script>
<style>
  .demo-Circle-custom{
    & h1{
        color: #3f414d;
        font-size: 28px;
        font-weight: normal;
    }
    & p{
        color: #657180;
        font-size: 14px;
        margin: 10px 0 15px;
    }
    & span{
        display: block;
        padding-top: 15px;
        color: #657180;
        font-size: 14px;
        &:before{
            content: '';
            display: block;
            width: 50px;
            height: 1px;
            margin: 0 auto;
            background: #e0e3e6;
            position: relative;
            top: -15px;
        };
    }
    & span i{
        font-style: normal;
        color: #3f414d;
    }
  }
</style>