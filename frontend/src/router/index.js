import Vue from 'vue'
import Router from 'vue-router'

const homepage = r => require.ensure([], () => r(require('@/components/main')), 'main"')
const abc = r => require.ensure([], () => r(require('@/components/mainpage/abc')), 'mainpage')
const misc = r => require.ensure([], () => r(require('@/components/mainpage/misc')), 'mainpage')
const item = r => require.ensure([], () => r(require('@/components/mainpage/item')), 'mainpage')
const ingredient = r => require.ensure([], () => r(require('@/components/mainpage/ingredient')), 'mainpage')
const coordinate = r => require.ensure([], () => r(require('@/components/chart/coordinate')), 'chart')

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'homepage',
      component: homepage
    },
    {
      path: '/misc',
      name: 'abc',
      component: abc,
      children: [
        {
          path: '',
          name: 'misc',
          component: misc
        },
        {
          path: '/item',
          name: 'item',
          component: item
        },
        {
          path: '/ingredient',
          name: 'ingredient',
          component: ingredient
        }
      ]
    },
    {
      path: '/result',
      name: 'result',
      component: coordinate
    }
  ]
})
