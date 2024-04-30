<template>
    <div class="person">
        first name:<input type="text" v-model="firstname"><br>
        last name: <input type="text" v-model="lastname"><br>
        full name: <span>{{fullname}}</span>
        <button @click="changefullname">修改全名</button>
    </div>
</template>

<script lang="ts" setup name="Person">
    import {ref,computed} from 'vue'
    let firstname = ref('mark')
    let lastname = ref('lan')

    // // 这样的计算属性只可读，不能改
    // let fullname = computed(
    //     ()=>{
    //         return firstname.value.slice(0,1).toUpperCase() + firstname.value.slice(1) + ' ' + lastname.value.slice(0,1).toUpperCase() + lastname.value.slice(1)
    //     }
    // )


    let fullname = computed({
        get(){
            return firstname.value.slice(0,1).toUpperCase() + firstname.value.slice(1) + ' ' + lastname.value.slice(0,1).toUpperCase() + lastname.value.slice(1)
        },
        set(value){
            const names = value.split(' ')
            firstname.value = names[0]
            lastname.value = names[1]
        }    
    }
    )
    function changefullname(){
        fullname.value = 'Mark Lan'
    }


</script>

<style>
button {
    margin: 0 5px;
}
</style>