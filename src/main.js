// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import vuetify from '@/plugins/vuetify'
import App from './App'
import router from './router'
import axios from 'axios'
import md5 from 'js-md5'
import VueCookies from 'vue-cookies'

Vue.config.productionTip = false

Vue.config.debug = true
axios.defaults.withCredentials = true
axios.defaults.baseURL = process.env.API_ROOT
Vue.prototype.$axios = axios
Vue.prototype.$md5 = md5
Vue.prototype.$cookies = VueCookies

/* eslint-disable no-new */

axios.interceptors.request.use(
	config => {
	    if (localStorage.getItem("user_token")) {
	        config.headers.Authorization = 'Bearer '+ localStorage.getItem("user_token")
	    }
	    return config
	},
	err => {
	    return Promise.reject(err)
})

axios.defaults.xsrfHeaderName = 'X-CSRFToken'
axios.defaults.xsrfCookieName = 'csrftoken'

router.beforeEach((to, from, next) => {
  if(to.meta.requireAuth) {
    if(localStorage.getItem("user_token")){
      next()
    }else{
      alert("請先登入")
    }
  }else{
    next()
  }
 })

 new Vue({
  el: '#app',
  router,
  vuetify,
  components: { App },
  template: '<App/>'
})
