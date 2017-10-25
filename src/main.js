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
import 'element-ui/lib/theme-default/index.css'
import 'font-awesome/css/font-awesome.min.css'
import axios from 'axios'
import $ from 'jquery'

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
  if (store.state.userid != '') {
    return true
  }
  else {
    if (!localStorage.userid) {
      return false
    }
    else {
      store.commit('setUserId', {"userid": userid})
      store.commit('setPagePower', {
        datafilter: 1,
        dataupdatebasic: 1,
        dataupdatefocus: 1,
        dataupdatescore: 1,
        indexmajor: 1,
        indexstudents: 1,
        officedataexpore: 1,
        officesuggestions: 1,
        person: 1,
        systemroleteam: 1,
        systemusers: 1,
        systemuserteam: 1,
      })
      return true
    }
  }
}

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  template: '<App/>',
  components: {App}
})
