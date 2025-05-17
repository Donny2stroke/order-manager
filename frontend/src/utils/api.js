import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
})

// Interceptor for requests
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Interceptor for 401 (expired token) responses
api.interceptors.response.use(
  res => res,
  async error => {
    const originalRequest = error.config
    const refresh = localStorage.getItem('refresh_token')

    if (error.response?.status === 401 && refresh && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const { data } = await axios.post(import.meta.env.VITE_API_URL+'/token/refresh/', { refresh })
        localStorage.setItem('token', data.access)
        api.defaults.headers.common['Authorization'] = `Bearer ${data.access}`
        originalRequest.headers['Authorization'] = `Bearer ${data.access}`
        return api(originalRequest) // retry the request
      } catch (e) {
        localStorage.clear()
        window.location.href = '/login'
        return Promise.reject(e)
      }
    }

    return Promise.reject(error)
  }
)

export default api
