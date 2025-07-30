import axios from 'axios'

// Create axios instance with base configuration
export const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
    headers: {
        'Content-Type': 'application/json',
    },
    timeout: 10000, // 10 seconds
})

// Request interceptor for adding auth tokens if needed
api.interceptors.request.use(
    (config) => {
        // You can add authentication tokens here
        // const token = localStorage.getItem('token')
        // if (token) {
        //   config.headers.Authorization = `Bearer ${token}`
        // }
        return config
    },
    (error) => {
        return Promise.reject(error)
    }
)

// Response interceptor for handling errors
api.interceptors.response.use(
    (response) => {
        return response
    },
    (error) => {
        // Handle common errors
        if (error.response) {
            // Server responded with error status
            console.error('API Error:', error.response.data)
        } else if (error.request) {
            // Request was made but no response received
            console.error('Network Error:', error.request)
        } else {
            // Something else happened
            console.error('Error:', error.message)
        }
        return Promise.reject(error)
    }
) 