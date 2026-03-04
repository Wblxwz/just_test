import { createMemoryHistory, createRouter } from 'vue-router'
import FileView from '../views/File.vue'
import DocumentationView from '../views/Documentation.vue'

const routes = [
  { path: '/', component: FileView, name: 'File' },
  { path: '/documentation', component: DocumentationView, name: 'documentation' },
]

const router = createRouter({
  history: createMemoryHistory(),
  routes,
})

export default router