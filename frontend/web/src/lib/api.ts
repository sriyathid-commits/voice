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
  (error: AxiosError<any>) => {
    // Create user-friendly error message
    let errorMessage = 'An unexpected error occurred'
    
    if (error.response) {
      // Server responded with error status
      const status = error.response.status
      const data = error.response.data
      
      if (status === 401) {
        // Unauthorized - clear auth and redirect to login
        if (typeof window !== 'undefined') {
          localStorage.removeItem('auth-storage')
          window.location.href = '/login'
        }
        errorMessage = 'Session expired. Please login again.'
      } else if (status === 403) {
        errorMessage = 'You do not have permission to access this resource'
      } else if (status === 404) {
        errorMessage = 'Resource not found'
      } else if (status === 422) {
        errorMessage = data?.message || 'Validation error. Please check your input.'
      } else if (status >= 500) {
        errorMessage = 'Server error. Please try again later.'
      } else if (data?.message) {
        errorMessage = data.message
      }
      
      console.error(`API Error [${status}]:`, errorMessage, data)
    } else if (error.request) {
      // Request made but no response
      errorMessage = 'No response from server. Please check your internet connection.'
      console.error('Network error:', error.request)
    } else {
      // Error in request setup
      errorMessage = error.message || errorMessage
      console.error('Request setup error:', error.message)
    }
    
    // Attach user-friendly message to error
    error.message = errorMessage
    
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
