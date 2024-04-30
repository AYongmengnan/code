<template>
    <div class="person">
        <h2>姓名：{{ person.name }}</h2>
        <h2>年龄：{{ person.age }}</h2>
        <button @click="chagename">修改名字</button>
        <button @click="chageage">修改年龄</button>
    </div>
</template>

<script lang="ts" setup name="Person">
    import {ref,reactive,toRefs,toRef} from 'vue'

    let person = reactive({
        name:'mark',
        age:18
    })
    let {name,age} = toRefs(person)
    let age_ = toRef(person,'age')
    function chageage(){
        // cars.value.price += 1 
        age.value += 1
    }
    function chagename(){
        name.value += '.'
    }
</script>

<style>
button {
    margin: 0 5px;
}
</style>