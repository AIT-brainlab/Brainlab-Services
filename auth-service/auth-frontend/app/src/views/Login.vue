<template>

    <h1>Login</h1>
    <label for="">username</label>
    <input type="text" v-model="username">
    <br>
    <label for="">password</label>
    <input type="password" v-model="password">
    <br>
    <button @click="makeLoggin">Login</button>
</template>

<script lang="ts">
import {defineComponent,ref,Ref} from 'vue'
import { restAPIGet} from "../script/RestAPIHelper"
export default defineComponent({
    setup(){

        const username = ref("")
        const password = ref("")

        const makeLoggin = async () =>{
            let resp = await restAPIGet(`/auth/api/login?username=${username.value}&password=${password.value}`)
            console.log(resp)
        }

        return {username,password,makeLoggin}
    }
})
</script>

<style lang="scss" scoped>

</style>