import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import './SignUpPage.css'

const SignUpPage = () => {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: ''
  })
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData((prev: { email: string; password: string; confirmPassword: string }) => ({
      ...prev,
      [name]: value
    }))
    if (error) setError('')
  }

  const validateForm = () => {
    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match')
      return false
    }

    if (formData.password.length < 6) {
      setError('Password must be at least 6 characters long')
      return false
    }

    return true
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!validateForm()) {
      return
    }

    setIsLoading(true)
    setError('')

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:7000'
      const response = await axios.post(`${apiUrl}/auth/register`, {
        email: formData.email,
        password: formData.password
      })

      // Store the token in localStorage
      localStorage.setItem('access_token', response.data.access_token)

      // Log success
      console.log('Signup successful:', response.data)

      // Redirect to home page
      navigate('/')

    } catch (err: any) {
      console.error('Signup error:', err)

      if (err.response?.status === 400) {
        if (err.response.data?.detail === 'Email already registered') {
          setError('An account with this email already exists')
        } else {
          setError(err.response.data?.detail || 'Invalid registration data')
        }
      } else if (err.response?.data?.detail) {
        setError(err.response.data.detail)
      } else {
        setError('Registration failed. Please try again.')
      }
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="signup-container">
      <div className="signup-card">
        <div className="signup-header">
          <h1>Create Account</h1>
          <p>Please fill in the details to create your account</p>
        </div>

        <form onSubmit={handleSubmit} className="signup-form">
          {error && (
            <div className="error-message">
              {error}
            </div>
          )}

          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleInputChange}
              placeholder="Enter your email"
              required
              disabled={isLoading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleInputChange}
              placeholder="Enter your password"
              required
              disabled={isLoading}
              minLength={6}
            />
          </div>

          <div className="form-group">
            <label htmlFor="confirmPassword">Confirm Password</label>
            <input
              type="password"
              id="confirmPassword"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleInputChange}
              placeholder="Confirm your password"
              required
              disabled={isLoading}
              minLength={6}
            />
          </div>

          <button
            type="submit"
            className="signup-button"
            disabled={isLoading}
          >
            {isLoading ? 'Creating Account...' : 'Create Account'}
          </button>
        </form>

        <div className="signup-footer">
          <p>Already have an account? <a href="#" onClick={() => navigate('/login')}>Sign in</a></p>
        </div>
      </div>
    </div>
  )
}

export default SignUpPage 