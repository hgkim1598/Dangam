import Vue from 'vue'
import Router from 'vue-router'
import FourIdioms from '@/components/FourIdioms'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'FourIdioms',
      component: FourIdioms
    },
  ]
})
