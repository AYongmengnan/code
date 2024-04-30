<!-- 
    三种标签
    1、template：html
    2、script：js、ts
    3、style：样式
-->
<template>
    <div class="app">
        <h1>hello word</h1>
        <Person/>
    </div>
</template>

<script lang="ts">
import Person from './components/Person.vue'
export default {
    name:'App',//组件名
    components:{Person}//组册组件
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