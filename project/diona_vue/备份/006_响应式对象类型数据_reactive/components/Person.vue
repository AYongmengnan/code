<template>
    <div class="person">
        <h2>一辆{{cars.brand}}，{{cars.price}}w起。</h2>
        <button @click="chageprice">修改价格</button>
        <ul>
            <li v-for="game in games" :key="game.id">{{game.name}}</li>
        </ul>
        <button @click="chagegame">修改第一个游戏名字</button>
    </div>
</template>

<script lang="ts" setup name="Person">
    import {reactive} from 'vue'

    let cars = reactive({brand:'极氪001',price:26.9})
    console.log(cars)
    let games = reactive([
        {id:1001,name:'原神'},
        {id:1002,name:'崩坏'},
        {id:1003,name:'战双'}
    ])

    function chageprice(){
        cars.price += 1
    }
    function chagegame(){
        games[0].name = '英雄联盟'
    }
</script>

<style>
button {
    margin: 0 5px;
}
</style>