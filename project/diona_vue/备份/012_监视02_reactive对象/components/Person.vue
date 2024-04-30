<template>
    <div class="person">
        <h1>监视【reactive】定义的【对象类型】数据</h1>
        <h2>姓名：{{ person.name }}</h2>
        <h2>年龄：{{ person.age }}</h2>
        <button @click="changename">修改名字</button>
        <button @click="changeage">修改年龄</button>
        <button @click="changeperson">修改整个数据</button>
    </div>
</template>

<script lang="ts" setup name="Person">
    import { link } from 'fs';
import {reactive,watch} from 'vue'
    let person = reactive({
        name:'mark',
        age:18
    })
    function changename(){
        person.name += '.'
    }
    function changeage(){
        person.age += 1
    }
    function changeperson(){
        Object.assign(person,{name:'link',age:20})
    }

    // 监视 reactive 对象数据是默认开启深度监控
    const stopwich = watch(person,(newvalue,oldvalue)=>{ //一般写一个value，是新值
        console.log('变化',newvalue,oldvalue)
    }
    )
</script>

<style>
button {
    margin: 0 5px;
}
</style>