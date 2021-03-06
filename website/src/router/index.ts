import Vue from 'vue'
import VueRouter, { RouteConfig } from 'vue-router'

Vue.use(VueRouter)

const Home = () => import(/* webpackChunkName: "home" */ '../views/Home.vue')
const NotFound = () => import(/* webpackChunkName: "notfound" */ '../views/NotFound.vue')
const ViewStation = () => import(/* webpackChunkName: "viewstation" */ '../views/ViewStation.vue')
const RegisterStation = () => import(/* webpackChunkName: "registerstation" */ '../views/RegisterStation.vue')
const StationsList = () => import(/* webpackChunkName: "stationslist" */ '../views/StationsList.vue')
const StationsMap = () => import(/* webpackChunkName: "stationsmap" */ '../views/StationsMap.vue')
const Subscribe = () => import(/* webpackChunkName: "subscribe" */ '../views/Subscribe.vue')
const Settings = () => import(/* webpackChunkName: "settings" */ '../views/Settings.vue')

const routes: Array<RouteConfig> = [
  { path: '/', name: 'home', component: Home },
  { path: '*', name: 'notFound', component: NotFound },
  // TODO: Add pages here
  { path: '/stations/view/:stations', name: 'viewStation', component: ViewStation },
  { path: '/stations/register', name: 'registerStation', component: RegisterStation },
  { path: '/stations/list', name: 'stationsList', component: StationsList },
  { path: '/stations/map', name: 'stationsMap', component: StationsMap },
  { path: '/subscribe', name: 'subscribe', component: Subscribe },
  { path: '/settings', name: 'settings', component: Settings }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
