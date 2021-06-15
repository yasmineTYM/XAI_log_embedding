<template>
  <div id="app">
      <el-row>
        <el-col :span="10">
          <div style="height:550px; border:1px solid black">
             <Embed/>
          </div>
        </el-col>
         <el-col :span="14">
            <Tree/>
         </el-col>
      </el-row>
       

  </div>
</template>

<script>
import Embed from './components/Embed.vue'
import Tree from './components/Tree.vue'
export default {
  name: 'App',
  components:{
    Embed,
    Tree
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
.el-row {
    margin-bottom: 20px;
    &:last-child {
      margin-bottom: 0;
    }
  }
  .el-col {
    border-radius: 4px;
  }
  .bg-purple-dark {
    background: #99a9bf;
  }
  .bg-purple {
    background: #d3dce6;
  }
  .bg-purple-light {
    background: #e5e9f2;
  }
  .grid-content {
    border-radius: 4px;
    min-height: 36px;
  }
  .row-bg {
    padding: 10px 0;
    background-color: #f9fafc;
  }
</style>
