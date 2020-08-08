import Vue from 'vue'
import Router from 'vue-router'
import main from '@/components/main'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: main,
      children: [
        {
          path: '/misc',
          name: 'abc',
          component: () => import('@/components/mainpage/abc.vue'),
          children: [
            {
              path: '',
              name: 'misc',
              component: () => import('@/components/mainpage/misc.vue')
            },
            {
              path: '/item',
              name: 'item',
              component: () => import('@/components/mainpage/item.vue')
            },
            {
              path: '/ingredient',
              name: 'ingredient',
              component: () => import('@/components/mainpage/ingredient.vue')
            }
          ]
        },
        {
          path: '/result',
          name: 'result',
          component: () => import('@/components/chart/bar.vue')
        }
      ]
    }
  ]
})
