<template>
  <div id="app" style="border: 1px solid black;border-radius: 5px;">
     
          <el-row style="height:980px;" v-if="SHOW_DETAIL">
            <el-col :span="5">
              <Embed/>
            </el-col>
            <el-col :span="19">
              <Tree/>
            </el-col>
          </el-row>
          <el-row style="height:980px" v-if="SHOW_OVERVIEW">
            <Overview/>
          </el-row>
      

  </div>
</template>

<script>
import Embed from './components/Embed.vue'
import Tree from './components/Tree.vue'
import Overview from './components/Overview.vue'
export default {
  name: 'App',
  components:{
    Embed,
    Tree,
    Overview
  },
  data(){
        return{
            
        }
  },
  computed:{
     SHOW_DETAIL(){
        return this.$store.getters.SHOW_DETAIL
      },
      SHOW_OVERVIEW(){
        return this.$store.getters.SHOW_OVERVIEW
      }
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
.scatter_row{
    background-color:#515E63; 
    height:34px;
    border-radius: 5px;
    
}
.scatter_row .el-input__inner {
    border-radius: 8px;
    padding-right: 20px;
    height: 28px;
    width:120px;
    background-color:#515E63;
    color: white;
}
</style>
