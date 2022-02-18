import Vue from 'vue'
import Router from 'vue-router'

const homepage = r => require.ensure([], () => r(require('@/components/main')), 'main"')
const abc = r => require.ensure([], () => r(require('@/components/mainpage/abc')), 'mainpage')
const misc = r => require.ensure([], () => r(require('@/components/mainpage/misc')), 'mainpage')
const item = r => require.ensure([], () => r(require('@/components/mainpage/item')), 'mainpage')
const ingredient = r => require.ensure([], () => r(require('@/components/mainpage/ingredient')), 'mainpage')
const inventory = r => require.ensure([], () => r(require('@/components/mainpage/inventory')), 'mainpage')
const employee = r => require.ensure([], () => r(require('@/components/mainpage/employee')), 'mainpage')
const coordinate = r => require.ensure([], () => r(require('@/components/chart/coordinate')), 'chart')
const lineChart = r => require.ensure([], () => r(require('@/components/mainpage/lineChart')), 'mainpage')
const turnover = r => require.ensure([], () => r(require('@/components/chart/turnover')), 'chart')
const cost = r => require.ensure([], () => r(require('@/components/chart/cost')), 'chart')
const ingredientCost = r => require.ensure([], () => r(require('@/components/chart/ingredientCost')), 'chart')

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
      component: abc,
      children: [
        {
          path: '',
          name: 'misc',
          meta: { requireAuth: true },
          component: misc
        },
        {
          path: '/item',
          name: 'item',
          meta: { requireAuth: true },
          component: item
        },
        {
          path: '/ingredient',
          name: 'ingredient',
          meta: { requireAuth: true },
          component: ingredient
        }
      ]
    },
    {
      path: '/inventory',
      name: 'inventory',
      meta: { requireAuth: true },
      component: inventory
    },
    {
      path: '/employee',
      name: 'employee',
      meta: { requireAuth: true },
      component: employee
    },
    {
      path: '/coordinate',
      name: 'coordinate',
      meta: { requireAuth: true },
      component: coordinate
    },
    {
      path: '/turnover',
      component: lineChart,
      children: [
        {
          path: '',
          name: 'turnover',
          meta: { requireAuth: true },
          component: turnover
        },
        {
          path: '/cost',
          name: 'cost',
          meta: { requireAuth: true },
          component: cost
        },
        {
          path: '/ingredientCost',
          name: 'ingredientCost',
          meta: { requireAuth: true },
          component: ingredientCost
        }
      ]
    }
  ]
})
