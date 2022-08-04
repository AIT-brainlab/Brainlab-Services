<template>
    <h1>Forget my Password</h1>
    <label for="">username</label>
    <input type="text" v-model="username">
    <button @click="requestToken">submit</button>
</template>


<script lang="ts">
import { defineComponent, ref } from 'vue'
import { restAPIGet, restAPIMethod } from '../script/RestAPIHelper'

export default defineComponent({
    setup() {
        const username = ref("")
        const requestToken = () =>{
            restAPIMethod("/auth/api/forget-mypassword","POST",{
                username:username.value
            },
            (resp)=>{
                console.log(resp)
            },
            (resp)=>{
                console.log(resp)
            })
        }
    
        return {username,requestToken}
    },
})
</script>
