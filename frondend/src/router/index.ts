import { createMemoryHistory, createRouter } from 'vue-router'
import FileView from '../views/File.vue'
import DocumentationView from '../views/Documentation.vue'
import ScriptView from '../views/Script.vue'

const routes = [
  { path: '/', redirect: '/file' },
  { path: '/file', component: FileView, name: 'file' },
  { path: '/documentation', component: DocumentationView, name: 'documentation' },
  { path: '/script', component: ScriptView, name: 'script' },
]

const router = createRouter({
  history: createMemoryHistory(),
  routes,
})

export default router