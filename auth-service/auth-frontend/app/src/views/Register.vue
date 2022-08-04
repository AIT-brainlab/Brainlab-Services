<template>
    <h1>Register</h1>
    <div>
        <label>firstname</label>
        <input type="text" v-model="firstname">
    </div>
    <div>
        <label>lastname</label>
     <input type="text" v-model="lastname">
    </div>
    <div>
        <label>username</label>
     <input type="text" v-model="username">
    </div>
    <div>
        <label>password</label>
     <input type="password" v-model="password">
    </div>
    <div>
        <label>password2</label>
     <input type="password" v-model="password2">
    </div>
    <button @click="submit">SUBMIT</button>
</template>


<script lang="ts">
import { defineComponent, ref } from 'vue'
import {restAPIMethod} from "../script/RestAPIHelper"
export default defineComponent({
    setup() {
        const firstname = ref("")
        const lastname = ref("")
        const username = ref("")
        const email = ref("")
        const password = ref("")
        const password2 = ref("")

        const submit = () =>{
            // TODO: password == password2
            restAPIMethod('/auth/api/register','POST',{
                    firstname:firstname.value,
                    lastname:lastname.value,
                    username:username.value,
                    email:email.value,
                    password:password.value
                
            },(resp)=>{console.log(resp)},async (resp)=>{
                let json_detail = await resp.json()
                console.log(json_detail)
            })
        }
        return {
            firstname,lastname,username,email,password,password2,submit
        }
    },
})
</script>
