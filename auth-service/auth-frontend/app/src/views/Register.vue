<template>
    <h1>Register</h1>
    
    <div>
        <label>username</label>
     <input type="text" v-model="username">
    </div>
     <div>
        <label>email</label>
     <input type="text" v-model="email">
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
import { useRouter } from 'vue-router'
export default defineComponent({
    setup() {

        const router = useRouter()
        const username = ref("")
        const email = ref("")
        const password = ref("")
        const password2 = ref("")

        const submit = () =>{
            // TODO: password == password2
            restAPIMethod('/auth/api/register','POST',{
                    username:username.value,
                    email:email.value,
                    password:password.value
                
            },(resp)=>{router.push("/")},async (resp)=>{
                let json_detail = await resp.json()
                console.log(json_detail)
            })
        }
        return {
            username,email,password,password2,submit
        }
    },
})
</script>
