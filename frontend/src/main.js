// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import vuetify from '@/plugins/vuetify'
import App from './App'
import router from './router'
import axios from 'axios'

Vue.config.productionTip = false

Vue.config.debug = true
axios.defaults.withCredentials = true
axios.defaults.baseURL = process.env.API_ROOT
Vue.prototype.$axios = axios

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  vuetify,
  components: { App },
  template: '<App/>'
})
