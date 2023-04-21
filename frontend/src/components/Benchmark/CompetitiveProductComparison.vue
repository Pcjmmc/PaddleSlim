<template>
    <div class="center-card-s">
        <div style="margin-top: 2%">
            <Select>
                任务名：

            </Select>

            <Select>
                Paddle版本：
            </Select>
        </div>
        <div>
            <Button style="text-align:right">
                查询
            </Button>
            <Button style="text-align:right">
                下载
            </Button>
        </div>
    </div>
</template>

<script>

export default {
    name: 'CompetitiveProductComparison',
    data: function () {
        return {
            task: []
        };
    }
};
</script>

<style scoped>
.btn-success {
  color: #fff;
  background-color: #67c23a;
  border-color: #67c23a;
}
.center-card-s {
  margin-left: 1%;
  margin-right: 1%;
  font-size: 14px;
  color: lightslategrey;
}

</style>
