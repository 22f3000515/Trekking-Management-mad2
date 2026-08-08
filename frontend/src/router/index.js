import { createRouter, createWebHistory } from "vue-router"

import Login from "../views/Login.vue"
import Register from "../views/Register.vue"

import AdminDashboard from "../views/AdminDashboard.vue"
import StaffDashboard from "../views/StaffDashboard.vue"
import UserDashboard from "../views/UserDashboard.vue"
import BookingHistory from "../views/BookingHistory.vue"


const routes = [

  {
    path: "/",
    redirect: "/login"
  },

  {
    path: "/login",
    component: Login
  },

  {
    path: "/register",
    component: Register
  },

  {
    path: "/admin",
    component: AdminDashboard
  },

  {
    path: "/staff",
    component: StaffDashboard
  },

  {
    path: "/dashboard",
    component: UserDashboard
  },

  {
  path: "/bookings",
  component: BookingHistory
}

]


const router = createRouter({

  history: createWebHistory(),

  routes

})


export default router