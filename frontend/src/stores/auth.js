import { reactive } from 'vue'

export const auth = reactive({
  isLoggedIn: !!localStorage.getItem('token'),
  username: localStorage.getItem('username') || ''
})

/**
* Handles user login.
* Stores token,  refresh token and username in localStorage and updates the auth state.
*/
export const login = (user, token, refresh) => {
  localStorage.setItem('token', token)
  localStorage.setItem('refresh_token', refresh)
  localStorage.setItem('username', user)
  auth.isLoggedIn = true
  auth.username = user
}

/**
* Handles user logout.
* Clears localStorage and resets the reactive auth state.
*/
export const logout = () => {
  localStorage.clear()
  auth.isLoggedIn = false
  auth.username = ''
}
