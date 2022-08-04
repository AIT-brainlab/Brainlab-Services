import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router'
import Home from '../views/Home.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/login',
    // name: 'login',
    component: () => import("../views/Login.vue")
  },
  {
    path: '/register',
    // name: 'register',
    component: () => import("../views/Register.vue")
  },
  {
    path: '/forget-mypassword',
    // name: 'forget-mypassword',
    component: () => import("../views/ForgetPassword.vue")
  },
  {
    path: '/reset-password',
    // name: 'forget-mypassword',
    component: () => import("../views/ResetPassword.vue")
  },

]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router