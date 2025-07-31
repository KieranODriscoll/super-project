import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import './HomePage.css'

const HomePage = () => {

  /**
   * Navigation function that allows navigation between other pages/routes
   * Allows redirection, back/forward navigation, updating URL
   * Allows redirection based on auth status and API responses
   */
  const navigate = useNavigate()

  /**
   * useState allows components to manage state as data changes in the app
   * user: object of type any, the user object from the API response, initially null
   * setUser - setter function for updating the user state.
   * When called, state values are update, re-renders the component and UI reflects new state
   */
  const [user, setUser] = useState<any>(null)

  /**
   * useState allows components to manage state as data changes in the app
   * isLoading: boolean, whether the component is loading or not, initially true
   * setIsLoading - setter function for updating the isLoading state.
   * When called, state values are update, re-renders the component and UI reflects new state
   */
  const [isLoading, setIsLoading] = useState(true)


  /**
   * useEffect performs side effects in components outside normal render cycles
   * Runs code after components render, handles API calls 
   * This will run only once, when the component mounts, allowing for authenticaton check
   * Empty dependency array, means it will only run once.
   */
  useEffect(() => {
    checkAuthStatus()
  }, [])


  /**
   * Checks if the user is authenticated
   * Looks for a JWT token in local storage to determine if the user is authenticated.
   * Validates the token with /users/me endpoint to determine validity
   */
  const checkAuthStatus = async () => {
    const token = localStorage.getItem('access_token')

    // If no token exists, the user is not authenticated, redirect to login page.
    if (!token) {
      navigate('/login')
      return
    }

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:7000'

      /**
       * Makes request to /users/me with JWT token to validate the token
       * If the token is valid, user object is set with user data and isLoading is set to false
       */
      const response = await axios.get(`${apiUrl}/users/me`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })

      setUser(response.data)
      setIsLoading(false)
    } catch (error) {
      /**
       * If an error occurs during validation, the token is either tampered with or expired
       * Remove the tocken and redirect to login page, user is not authenticated
       */
      console.error('Authentication check failed:', error)
      localStorage.removeItem('access_token')
      navigate('/login')
    }
  }

  /**
   * Logs the user out, calling the /auth/logout endpoint and removes the token
   * User is no longer authenticated, redirect to login page
   */
  const handleLogout = async () => {
    const token = localStorage.getItem('access_token')

    /**
     * A token "should" always exist, but if it doesn't, the user is not authenticated
     * and cannot be logged out. Safety check to prevent undefined code paths.
    */
    if (token) {
      try {

        /**
         * Makes request to /auth/logout with JWT token in the header to logout the user.
         * Which will update the user's is_active field to false
         */
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

    /**
     * Removes the token from local storage, user is no longer authenticated
     * Redirects to login page
     */
    localStorage.removeItem('access_token')
    navigate('/login')
  }
  /**
   * If isLoading is set to true, display a component that shows a loading message
   */
  if (isLoading) {
    return (
      <div className="home-container">
        <div className="loading">Loading...</div>
      </div>
    )
  }

  /**
   * Main component of the page that displays the user's email and a logout button
   * Displayed when isLoading is set to false and user is authenticated
   */
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