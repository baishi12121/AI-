import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/HomeView.vue'),
      meta: { title: 'AI 社恐聊天外挂' },
    },
    {
      path: '/result/:id',
      name: 'result',
      component: () => import('@/views/ResultView.vue'),
      meta: { title: '分析结果' },
    },
    {
      path: '/history',
      name: 'history',
      component: () => import('@/views/HistoryView.vue'),
      meta: { title: '历史记录' },
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/',
    },
  ],
  scrollBehavior() {
    return { top: 0 }
  },
})

router.afterEach((to) => {
  const t = to.meta?.title as string | undefined
  if (t) document.title = t
})

export default router
