import axios from 'axios'

// Create a reusable Axios instance configured with the API base URL loaded from .env file
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
})

// Allega automaticamente l'intestazione di autorizzazione a tutte le richieste in uscita se il token è presente
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

/**
* Interceptor to handle 401 Unauthorized responses.
* Automatically tries to refresh the access token using the refresh token.
*/
api.interceptors.response.use(
  res => res,
  async error => {
    const originalRequest = error.config
    const refresh = localStorage.getItem('refresh_token')
    
    // If token expired and we haven't retried yet
    if (error.response?.status === 401 && refresh && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        // Attempt to refresh the access token
        const { data } = await axios.post(import.meta.env.VITE_API_URL+'/token/refresh/', { refresh })
        // Save the new token
        localStorage.setItem('token', data.access)
        // Update the headers and retry the original request
        api.defaults.headers.common['Authorization'] = `Bearer ${data.access}`
        originalRequest.headers['Authorization'] = `Bearer ${data.access}`
        return api(originalRequest) // retry the request
      } catch (e) {
        // If refresh fails, log the user out
        localStorage.clear()
        window.location.href = '/login'
        return Promise.reject(e)
      }
    }

    return Promise.reject(error)
  }
)

export default api
