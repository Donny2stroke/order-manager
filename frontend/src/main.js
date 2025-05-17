import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/custom.scss'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import {
  faPlus,
  faPen,
  faTrash,
  faSignOutAlt,
  faSignInAlt,
  faUser,
  faBox,
  faTags,
  faFileAlt,
  faCalendar,
  faInfoCircle,
  faSave,
  faEye,
  faTag,
  faEuroSign,
  faSearch,
  faClipboardList
} from '@fortawesome/free-solid-svg-icons'

library.add(
  faPlus,
  faPen,
  faTrash,
  faSignOutAlt,
  faSignInAlt,
  faUser,
  faBox,
  faTags,
  faFileAlt,
  faCalendar,
  faInfoCircle,
  faSave,
  faEye,
  faTag,
  faEuroSign,
  faSearch,
  faClipboardList
)


const app = createApp(App)
app.component('font-awesome-icon', FontAwesomeIcon)
app.use(router)
app.mount('#app')
