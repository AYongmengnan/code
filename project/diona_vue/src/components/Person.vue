<template>
    <div class="person">
        <h1>监视【reactive、ref】定义的【对象类型】数据的属性数据</h1>
        <h2>姓名：{{ person.name }}</h2>
        <h2>年龄：{{ person.age }}</h2>
        <h2>车辆：{{ person.car.c1 }}、{{ person.car.c2 }}</h2>
        <button @click="changename">修改名字</button>
        <button @click="changeage">修改年龄</button>
        <button @click="changecar1">修改车1</button>
        <button @click="changecar2">修改车2</button>
        <button @click="changecar">修改整个数据</button>
    </div>
</template>

<script lang="ts" setup name="Person">
import {reactive,watch} from 'vue'
    let person = reactive({
        name:'mark',
        age:18,
        car:{
            c1:'benci',
            c2:'baoma'
        }
    })
    function changename(){
        person.name += '.'
    }
    function changeage(){
        person.age += 1
    }
    function changecar1(){
        person.car.c1 = 'aodi'
    }
    function changecar2(){
        person.car.c2 = 'biyadi'
    }
    function changecar(){
        // Object.assign(person.car,{c1:'jike',c2:'linke'})
        person.car = {c1:'jike',c2:'linke'}
    }

    // 监视响应式对象中某个属性，且属性是基本类型的，要写成函数式
    // const stopwich = watch(()=>{return person.car},(newvalue,oldvalue)=>{ //一般写一个value，是新值
    // 监视响应式对象中某个属性，且属性是对象类型的，可以直接写也可成函数式，推荐函数式
    // const stopwich = watch(person.car,(newvalue,oldvalue)=>{
    // const stopwich = watch(()=>person.car,(newvalue,oldvalue)=>{
    // 监视多个数据
    const stopwich = watch([()=>person.name,()=>person.car.c1],(newvalue,oldvalue)=>{
        console.log('变化',newvalue,oldvalue)
    },{deep:true}
    )
</script>

<style>
button {
    margin: 0 5px;
}
</style>