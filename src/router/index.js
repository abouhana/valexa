import Vue from 'vue'
import VueRouter from 'vue-router'
import MainView from "../views/MainView";
import ProfileView from "../views/ProfileView";
import DataView from "../views/DataView";
import LoadingView from "../views/LoadingView";
import SettingsView from "../views/SettingsView";

Vue.use(VueRouter)

  const routes = [
  {
    path: '/',
    name: 'main',
    component: LoadingView
  },
  {
    path: '/profiles',
    name: 'profiles',
    component: ProfileView
  },
  {
    path: '/data',
    name: 'data',
    component: DataView
  },
  {
    path: '/settings',
    name: 'settings',
    component: SettingsView
  }
]

const router = new VueRouter({
  mode: process.env.IS_ELECTRON ? 'hash' : 'history',
  routes
})

export default router
