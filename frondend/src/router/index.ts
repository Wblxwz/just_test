import { createMemoryHistory, createRouter } from 'vue-router'
import FileView from '../views/File.vue'
import DocumentationView from '../views/Documentation.vue'
import ProcessView from '../views/Process.vue'

const routes = [
  { path: '/', redirect: '/file' },
  { path: '/file', component: FileView, name: 'file' },
  { path: '/documentation', component: DocumentationView, name: 'documentation' },
  { path: '/process', component: ProcessView, name: 'process' },
]

const router = createRouter({
  history: createMemoryHistory(),
  routes,
})

export default router