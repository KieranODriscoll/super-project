import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import './LoginPage.css'

const LoginPage = () => {

  /**
   * Navigation function that allows navigation between other pages/routes
   * Allows redirection, back/forward navigation, updating URL
   * Allows redirection based on auth status and API responses
   */
  const navigate = useNavigate()

  /**
   * useState allows components to manage state as data changes in the app
   * formData: object, containing email and password, initially empty. Data contained within the login form.
   * setFormData - setter function for updating the form state.
   * When called, state values are update, re-renders the component and UI reflects new state
   */
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  })
  /**
   * useState allows components to manage state as data changes in the app
   * isLoading: boolean, whether the component is loading or not, initially true
   * setIsLoading - setter function for updating the isLoading state.
   * When called, state values are update, re-renders the component and UI reflects new state
   */
  const [isLoading, setIsLoading] = useState(false)

  /**
   * useState allows components to manage state as data changes in the app
   * error: initially an empty string, used to display error messages to user
   * setError - setter function for updating the error state, with a given error message
   * When called, state values are update, re-renders the component and UI reflects new state
   */
  const [error, setError] = useState('')

  /**
   * Function to handle when a user types in the login form.
   * Updates the formData state with the new input value
   * If an error message is displayed, it is cleared upon user typing
   * @param e - change event that fires when the user types in the form
   */
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    /**
     * Deconstructs the event
     * name: string, the input field that is being changed
     * value: string, the current value of the input field
     */
    const { name, value } = e.target
    /**
     * calls the setter function for the formData state
     * Updates the forData objects with the new key value pair for the input field that is being changed
     * prev: object, the previous state of the form data. If email is set and typing in password, email will not be lost
     * [name]: string, the input field that is being changed
     * value: string, the current value of the input field
     */
    setFormData((prev: { email: string; password: string }) => ({
      ...prev,
      [name]: value
    }))
    /**
     * If an error message is currently displayed, it is cleared upon user typing
     */
    if (error) setError('')
  }

  /**
   * Function to handle when the user clicks the submit button
   * Sets the isLoading state to true, to display a loading message
   * Clears the error state, to remove any error messages before re-submitting
   * @param e - change event that fires when the user clicks submit button
   */
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault() // Prevents the default form submission behaviour, internal behaviour is to browser reload/refresh
    setIsLoading(true)
    setError('')

    try {

      /**
       * Makes request to /auth/login with email and password to login the user
       * If the login is successful, the token is stored in localStorage
       * Redirects to home page
       */
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:7000'
      const response = await axios.post(`${apiUrl}/auth/login`, {
        email: formData.email,
        password: formData.password
      })

      localStorage.setItem('access_token', response.data.access_token)
      console.log('Login successful:', response.data)
      navigate('/')

    } catch (err: any) {
      console.error('Login error:', err)

      /**
       * If the login is unsuccessful, an appropriate error message will be displayed
       * No navigation occurs, user stays on the login page
       */
      if (err.response?.status === 401) {
        setError('Invalid email or password')
      } else if (err.response?.data?.detail) {
        setError(err.response.data.detail)
      } else {
        setError('Login failed. Please try again.')
      }
    } finally {
      setIsLoading(false)
    }
  }

  /**
   * Main component of the page that displays the login form
   * Contains 2 input fields, email and password and a submit button
   * event handlers are setup above for submittion logic and input change logic
   * Sets required fields for both email and password
   * One additional element, a link to the register page redirecting to /register
   */
  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-header">
          <h1>Welcome Back</h1>
          <p>Please sign in to your account</p>
        </div>

        <form onSubmit={handleSubmit} className="login-form">
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
            />
          </div>

          <button
            type="submit"
            className="login-button"
            disabled={isLoading}
          >
            {isLoading ? 'Signing In...' : 'Sign In'}
          </button>
        </form>

        <div className="login-footer">
          <p>Don't have an account? <a href="#s" onClick={() => navigate('/register')}>Sign up</a></p>
        </div>
      </div>
    </div>
  )
}

export default LoginPage 