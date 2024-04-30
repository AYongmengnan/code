<template>
    <div class="person">
        <h2>姓名：{{ name }}</h2>
        <h2>年龄：{{ age }}</h2>
        <button @click="changeName">修改名字</button>
        <button @click="changeAge">修改年龄</button>
        <button @click="showTel">查看联系方式</button>
    </div>
</template>

<script lang="ts">
    export default{
        name:'Person',
        // data(){   //vue2
        //     return {
        //         name:'mark',
        //         age:18,
        //         tel:19999999
        //     }
        // },
        // methods:{
        //     showTel(){
        //         alert(this.tel)
        //     },
        //     changeName(){
        //         this.name = 'mark lan'
        //     },
        //     changeAge(){
        //         this.age += 1
        //     }
        // }
        setup(){//setup函数中不能用this this是undefined，vue已经弱化this
            let name = 'mark'  //注意这样是 不是响应式的数据
            let age = 18
            let tel = '12345678901'
            
            function changeName(){
                name = 'mark lan' // 这样修改，但页面没有修改，因为不是响应式的
            }
            function changeAge(){
                age += 1
            }
            function showTel(){
                alert(tel)
            }
            return {name,age,changeName,changeAge,showTel}
        }
    }
</script>

<style>
button {
    margin: 0 5px;
}
</style>