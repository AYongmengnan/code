<template>
    <div class="person">
        <h2>姓名：{{ name }}</h2>
        <h2>年龄：{{ age }}</h2>
        <button @click="changeName">修改名字</button>
        <button @click="changeAge">修改年龄</button>
        <button @click="showTel">查看联系方式</button>

    </div>
</template>

<!-- <script lang="ts">
    export default{
        name:'Person'
    }
</script> -->

<script lang="ts" setup name="Person">
    import {ref} from 'vue'
    let name = ref('mark' ) //注意这样是 不是响应式的数据
    let age = ref(18)
    let tel = '12345678901'
    console.log(name)
    console.log(age)
    console.log(tel)
    function changeName(){
        name.value = 'mark lan' // 这样修改，但页面没有修改，因为不是响应式的
        console.log(name)
    }
    function changeAge(){
        age.value += 1
        console.log(age)
    }
    function showTel(){
        alert(tel) 
    }
</script>

<style>
button {
    margin: 0 5px;
}
</style>