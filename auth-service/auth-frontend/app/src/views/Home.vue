<template>
  <video width="320" height="240" controls>
    <source src="/fs?path=vdo1.mp4" type="video/mp4" />
    Your browser does not support the video tag.
  </video>
  <br>
  <img src="/fs?path=image1.png" height="100" alt="">
  <router-link to="/login">Login</router-link>
  <router-link to="/register">Register</router-link>
  <router-link to="/forget-mypassword">Forget password</router-link>
</template>

<style lang="scss" scoped>
a {
  display: grid;
}
</style>