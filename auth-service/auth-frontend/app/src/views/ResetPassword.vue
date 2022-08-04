<template>
    <h1>Enter new password</h1>
    <label for="">new password</label>
    <input type="password" v-model="password">
    <label for="">new password again</label>
    <input type="password" v-model="password2">
    <button @click="submit">submit</button>
</template>


<script lang="ts">
import { defineComponent, ref } from 'vue'
import { useRoute } from 'vue-router'
import { restAPIMethod } from '../script/RestAPIHelper'
export default defineComponent({
    setup() {
        const password = ref("")
        const password2 = ref("")
        // TODO password==password2

        const route = useRoute()
        
        const submit = () => {
        restAPIMethod('/auth/api/forget-mypassword/reset',"PUT",{
            new_password:password.value,
            token:route.query['token']
        },
        (resp) => {console.log(resp)},
        (resp) => {console.log(resp)} 
        )
        }
        return {password,password2,submit}
    },
})
</script>
