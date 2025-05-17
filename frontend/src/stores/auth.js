import { reactive } from 'vue'

export const auth = reactive({
  isLoggedIn: !!localStorage.getItem('token'),
  username: localStorage.getItem('username') || ''
})

export const login = (user, token, refresh) => {
  localStorage.setItem('token', token)
  localStorage.setItem('refresh_token', refresh)
  localStorage.setItem('username', user)
  auth.isLoggedIn = true
  auth.username = user
}

export const logout = () => {
  localStorage.clear()
  auth.isLoggedIn = false
  auth.username = ''
}
