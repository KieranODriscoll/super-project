import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import './HomePage.css'

const HomePage = () => {
  const navigate = useNavigate()
  const [user, setUser] = useState<any>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    checkAuthStatus()
  }, [])

  const checkAuthStatus = async () => {
    const token = localStorage.getItem('access_token')

    if (!token) {
      navigate('/login')
      return
    }

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:7000'
      const response = await axios.get(`${apiUrl}/users/me`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })

      setUser(response.data)
      setIsLoading(false)
    } catch (error) {
      console.error('Authentication check failed:', error)
      localStorage.removeItem('access_token')
      navigate('/login')
    }
  }

  const handleLogout = async () => {
    const token = localStorage.getItem('access_token')

    if (token) {
      try {
        const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:7000'
        await axios.post(`${apiUrl}/auth/logout`, {}, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })
      } catch (error) {
        console.error('Logout error:', error)
      }
    }

    localStorage.removeItem('access_token')
    navigate('/login')
  }

  if (isLoading) {
    return (
      <div className="home-container">
        <div className="loading">Loading...</div>
      </div>
    )
  }

  return (
    <div className="home-container">
      <div className="home-card">
        <div className="home-header">
          <h1>Logged In</h1>
          <p>Welcome back, {user?.email}!</p>
        </div>

        <button
          onClick={handleLogout}
          className="logout-button"
        >
          Logout
        </button>
      </div>
    </div>
  )
}

export default HomePage 