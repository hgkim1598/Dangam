import Vue from 'vue'
import Router from 'vue-router'
import FourIdioms from '@/components/FourIdioms'
import WiseSaying from '@/components/WiseSaying'
import ImageGenerate from '@/components/ImageGenerate'
import ImageCrawling from '@/components/ImageCrawling'

Vue.use(Router)

export default new Router({
  mode: 'history', // 히스토리 모드 설정
  routes: [
    {
      path: '/',
      name: 'FourIdioms', // 홈 페이지로 사용할 컴포넌트를 여기에 설정할 수 있습니다.
      component: FourIdioms // 만약 루트 경로가 별도의 홈 페이지로 사용된다면 해당 컴포넌트로 설정합니다.
    },
    {
      path: '/four',
      name: 'FourIdioms',
      component: FourIdioms
    },
    {
      path: '/wise',
      name: 'WiseSaying',
      component: WiseSaying
    },
    {
      path: '/imggen',
      name: 'ImageGenerate',
      component: ImageGenerate
    },
    {
      path: '/ImageCrawling',
      name: 'ImageCrawling', // 홈 페이지로 사용할 컴포넌트를 여기에 설정할 수 있습니다.
      component: ImageCrawling // 만약 루트 경로가 별도의 홈 페이지로 사용된다면 해당 컴포넌트로 설정합니다.
    },
    
  ]
})