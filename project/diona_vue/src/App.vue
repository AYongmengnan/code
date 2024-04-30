<!-- 
    三种标签
    1、template：html
    2、script：js、ts
    3、style：样式
-->
<template>
    <!-- <div class="app">
        <Person/>
        
    </div> -->
    <VideoPlayer/>
</template>

<script lang="ts">
import Person from './components/Person.vue'
import VideoPlayer from './components/VideoPlayer.vue'
export default {
    name:'App',//组件名
    components:{Person,VideoPlayer}//注册组件
}
</script>

<style>
    .app {
        background-color: #ddd;
        box-shadow: 0 0 10px;
        border-radius: 20px;
        padding: 20px;
    }
</style>