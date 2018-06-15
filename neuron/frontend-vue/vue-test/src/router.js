import Vue from 'vue'
import Router from 'vue-router'
import Menu from './components/Menu.vue'
import View1 from './components/View1.vue'
import View2 from './components/View2.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'menu',
      component: Menu
    },
    {
      path: '/view1',
      name: 'view1',
      component: View1
    },
    {
      path: '/view2',
      name: 'view2',
      component: View2
    }
  ]
})