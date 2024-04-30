<template>
    <div class="person">
        <h1>监视【ref】定义的【对象类型】数据</h1>
        <h2>姓名：{{ person.name }}</h2>
        <h2>年龄：{{ person.age }}</h2>
        <button @click="changename">修改名字</button>
        <button @click="changeage">修改年龄</button>
        <button @click="changeperson">修改整个数据</button>
    </div>
</template>

<script lang="ts" setup name="Person">
    import {ref,watch,toRefs} from 'vue'
    let person = ref({
        name:'mark',
        age:18
    })
    function changename(){
        person.value.name += '.'
    }
    function changeage(){
        person.value.age += 1
    }
    function changeperson(){
        person.value = {name:'lin',age:16}
    }

    // 监视 watch(监视谁，回调函数)
    // 参数1:监视的数据
    // 参数2:监视的回调
    // 参数3:配置对象
    const stopwich = watch(person,(newvalue,oldvalue)=>{ //一般写一个value，是新值
        console.log('变化',newvalue,oldvalue)
    },
    {deep:true},
    )
</script>

<style>
button {
    margin: 0 5px;
}
</style>