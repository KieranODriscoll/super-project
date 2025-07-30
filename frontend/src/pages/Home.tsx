import React from 'react'
import { Link } from 'react-router-dom'
import { Database, Code, Zap, Shield } from 'lucide-react'

const Home: React.FC = () => {
    return (
        <div className="space-y-12">
            {/* Hero Section */}
            <div className="text-center space-y-6">
                <h1 className="text-4xl md:text-6xl font-bold text-gray-900">
                    Full-Stack Application
                </h1>
                <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                    A modern, scalable full-stack application built with React, FastAPI, and PostgreSQL.
                    Experience the power of containerized microservices with Docker.
                </p>
                <div className="flex justify-center space-x-4">
                    <Link
                        to="/items"
                        className="bg-primary-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-primary-700 transition-colors"
                    >
                        View Items
                    </Link>
                    <a
                        href="http://localhost:8000/docs"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="border border-gray-300 text-gray-700 px-6 py-3 rounded-lg font-medium hover:bg-gray-50 transition-colors"
                    >
                        API Docs
                    </a>
                </div>
            </div>

            {/* Features Section */}
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
                <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
                    <div className="flex items-center space-x-3 mb-4">
                        <div className="p-2 bg-blue-100 rounded-lg">
                            <Code className="h-6 w-6 text-blue-600" />
                        </div>
                        <h3 className="text-lg font-semibold text-gray-900">React Frontend</h3>
                    </div>
                    <p className="text-gray-600">
                        Modern React 18 with TypeScript, Vite, and Tailwind CSS for a responsive and beautiful UI.
                    </p>
                </div>

                <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
                    <div className="flex items-center space-x-3 mb-4">
                        <div className="p-2 bg-green-100 rounded-lg">
                            <Zap className="h-6 w-6 text-green-600" />
                        </div>
                        <h3 className="text-lg font-semibold text-gray-900">FastAPI Backend</h3>
                    </div>
                    <p className="text-gray-600">
                        High-performance Python API with automatic documentation, validation, and async support.
                    </p>
                </div>

                <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
                    <div className="flex items-center space-x-3 mb-4">
                        <div className="p-2 bg-purple-100 rounded-lg">
                            <Database className="h-6 w-6 text-purple-600" />
                        </div>
                        <h3 className="text-lg font-semibold text-gray-900">PostgreSQL</h3>
                    </div>
                    <p className="text-gray-600">
                        Robust relational database with SQLAlchemy ORM for efficient data management.
                    </p>
                </div>

                <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
                    <div className="flex items-center space-x-3 mb-4">
                        <div className="p-2 bg-orange-100 rounded-lg">
                            <Shield className="h-6 w-6 text-orange-600" />
                        </div>
                        <h3 className="text-lg font-semibold text-gray-900">Docker Ready</h3>
                    </div>
                    <p className="text-gray-600">
                        Containerized with Docker and Docker Compose for easy deployment and scaling.
                    </p>
                </div>
            </div>

            {/* Tech Stack Section */}
            <div className="bg-white p-8 rounded-lg shadow-md border border-gray-200">
                <h2 className="text-2xl font-bold text-gray-900 mb-6">Technology Stack</h2>
                <div className="grid md:grid-cols-3 gap-6">
                    <div>
                        <h3 className="text-lg font-semibold text-gray-900 mb-3">Frontend</h3>
                        <ul className="space-y-2 text-gray-600">
                            <li>• React 18 with TypeScript</li>
                            <li>• Vite for fast development</li>
                            <li>• Tailwind CSS for styling</li>
                            <li>• React Router for navigation</li>
                            <li>• Axios for API calls</li>
                        </ul>
                    </div>
                    <div>
                        <h3 className="text-lg font-semibold text-gray-900 mb-3">Backend</h3>
                        <ul className="space-y-2 text-gray-600">
                            <li>• FastAPI framework</li>
                            <li>• SQLAlchemy ORM</li>
                            <li>• PostgreSQL database</li>
                            <li>• Pydantic validation</li>
                            <li>• Alembic migrations</li>
                        </ul>
                    </div>
                    <div>
                        <h3 className="text-lg font-semibold text-gray-900 mb-3">DevOps</h3>
                        <ul className="space-y-2 text-gray-600">
                            <li>• Docker containers</li>
                            <li>• Docker Compose</li>
                            <li>• Hot reloading</li>
                            <li>• Health checks</li>
                            <li>• Production ready</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Home 