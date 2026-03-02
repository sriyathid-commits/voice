import axios, { AxiosError, AxiosRequestConfig } from 'axios'
import { API_URL } from './constants'

// Create axios instance
export const apiClient = axios.create({
  baseURL: API_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor - add auth token
apiClient.interceptors.request.use(
  (config) => {
    // Get token from localStorage
    if (typeof window !== 'undefined') {
      const authStorage = localStorage.getItem('auth-storage')
      if (authStorage) {
        try {
          const { state } = JSON.parse(authStorage)
          if (state?.token) {
            config.headers.Authorization = `Bearer ${state.token}`
          }
        } catch (error) {
          console.error('Error parsing auth storage:', error)
        }
      }
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor - handle errors
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response) {
      // Server responded with error status
      const status = error.response.status
      
      if (status === 401) {
        // Unauthorized - clear auth and redirect to login
        if (typeof window !== 'undefined') {
          localStorage.removeItem('auth-storage')
          window.location.href = '/login'
        }
      } else if (status === 403) {
        // Forbidden
        console.error('Access forbidden:', error.response.data)
      } else if (status === 404) {
        // Not found
        console.error('Resource not found:', error.response.data)
      } else if (status >= 500) {
        // Server error
        console.error('Server error:', error.response.data)
      }
    } else if (error.request) {
      // Request made but no response
      console.error('No response from server:', error.request)
    } else {
      // Error in request setup
      console.error('Request error:', error.message)
    }
    
    return Promise.reject(error)
  }
)

// Generic API request function
export async function apiRequest<T>(
  config: AxiosRequestConfig
): Promise<T> {
  const response = await apiClient.request<T>(config)
  return response.data
}

// Convenience methods
export const api = {
  get: <T>(url: string, config?: AxiosRequestConfig) =>
    apiRequest<T>({ ...config, method: 'GET', url }),
  
  post: <T>(url: string, data?: any, config?: AxiosRequestConfig) =>
    apiRequest<T>({ ...config, method: 'POST', url, data }),
  
  put: <T>(url: string, data?: any, config?: AxiosRequestConfig) =>
    apiRequest<T>({ ...config, method: 'PUT', url, data }),
  
  patch: <T>(url: string, data?: any, config?: AxiosRequestConfig) =>
    apiRequest<T>({ ...config, method: 'PATCH', url, data }),
  
  delete: <T>(url: string, config?: AxiosRequestConfig) =>
    apiRequest<T>({ ...config, method: 'DELETE', url }),
}
