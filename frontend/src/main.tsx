import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from './App.tsx'
import './index.css'


/**
 * This file initalizes the React application and sets up
 * The root element is the div with id 'root' in the index.html file
 * The App component is the main application component
 * The BrowserRouter is the router that manages the navigation between pages
 * The App component is the main application component
 */
ReactDOM.createRoot(document.getElementById('root')!).render(
    <React.StrictMode>
        <BrowserRouter>
            <App />
        </BrowserRouter>
    </React.StrictMode>,
) 