import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
// Custom SCSS for styling overrides
import './assets/custom.scss'
// Bootstrap JS
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
// Font Awesome configuration
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
// Importing all the icons used throughout the application
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
// Adding the selected icons to the global library
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

// Create Vue application instance
const app = createApp(App)
// Register FontAwesomeIcon as a global component
app.component('font-awesome-icon', FontAwesomeIcon)
// Apply router to the application
app.use(router)
// Mount the app to the DOM
app.mount('#app')
