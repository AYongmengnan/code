<template>
    <div class="person">
        <h1>监视【ref】定义的【基本类型】数据</h1>
        <h2>当前得分：{{ sum }}</h2>
        <button @click="changesum">增加得分</button>
    </div>
</template>

<script lang="ts" setup name="Person">
    import {ref,watch} from 'vue'
    let sum = ref(78)
    function changesum(){
        sum.value += 2
    }
    // 监视 watch(监视谁，回调函数)
    const stopwich = watch(sum,(newvalue,oldvalue)=>{
        console.log('得分变化',newvalue,oldvalue)
        if (newvalue > 100) {
            alert('得分已超过100，不能再增加')
            stopwich()
        }
    })
</script>

<style>
button {
    margin: 0 5px;
}
</style>