// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import VueRouter from 'vue-router'
import routes from './router/index'
import store from './vuex/store'
import ElementUI from 'element-ui'
import VueResource from 'vue-resource'
import Vuex from 'vuex'
import 'element-ui/lib/theme-chalk/index.css'
import 'font-awesome/css/font-awesome.min.css'
import axios from 'axios'
import $ from 'jquery'
import {loginGetUserRoleUrl} from '@/api/httpapi'

Vue.prototype.$http = axios
export const myAxios = axios

Vue.config.productionTip = false

Vue.use(Vuex)
Vue.use(VueRouter)
Vue.use(ElementUI)
Vue.use(VueResource)

const router = new VueRouter({
  routes
})

router.beforeEach((to, from, next) => {
  if (to.path == '/login') {
    store.commit("delUserId");
  }
  let user = store.state.userid
  if (to.meta.requiresAuth) {
    if (!isLogin(localStorage.userid)) {
      next({
        path: '/login',
        query: {redirect: to.fullPath}
      })
    } else {
      next()
    }
  }
  else {
    next()
  }
})

function isLogin(userid) {
  let flag
  if (store.state.userid)
    flag = true
  else {
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
      if (this.readyState == 4 && this.status == 200) {
        let res = JSON.parse(this.responseText)
        if (res['status'] == 1) {
          store.commit('setUserId', {"userid": userid})
          store.commit('setPagePower', res.data)
          flag = true
        }
        else {
          flag = false
        }
      }
    }
    xhttp.open("POST", loginGetUserRoleUrl, false)
    xhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded")
    xhttp.send(localStorage.sessionid)
  }
  console.log(flag)
  return flag
}

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  template: '<App/>',
  components: {App}
})
