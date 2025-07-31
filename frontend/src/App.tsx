import { Routes, Route } from 'react-router-dom'
import LoginPage from './components/LoginPage'
import SignUpPage from './components/SignUpPage'
import HomePage from './components/HomePage'
import './App.css'

/**
 * Main application component
 * Defines the routes for the application
 * 3 routes for this application:
 * / - Home page, authenticated view
 * /login - Login page, unauthenticated view
 * /register - Registration page, unauthenticated view
 */
function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<SignUpPage />} />
      </Routes>
    </div>
  )
}

export default App 