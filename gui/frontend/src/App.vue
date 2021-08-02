<template>
  <div id="app" style="border: 1px solid black;border-radius: 5px;">
      <!-- <el-row style="height:360px; border-bottom:1px solid grey">
        <Embed/>
      </el-row> -->
      
      <!-- <el-row style="height:620px">
         <Tree/>
      </el-row> -->
      <el-row style="height:980px;">
        <el-col :span="5">
          <Embed/>
        </el-col>
        <el-col :span="19">
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


</style>
