#!/bin/bash

# Full-Stack Application Deployment Script
# This script helps deploy the application in different environments

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
    print_success "Docker is running"
}

# Function to check if Docker Compose is available
check_docker_compose() {
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose and try again."
        exit 1
    fi
    print_success "Docker Compose is available"
}

# Function to create .env file if it doesn't exist
setup_env() {
    if [ ! -f .env ]; then
        print_warning ".env file not found. Creating from template..."
        if [ -f env.example ]; then
            cp env.example .env
            print_success "Created .env file from template"
            print_warning "Please edit .env file with your configuration before continuing"
        else
            print_error "env.example file not found. Please create a .env file manually."
            exit 1
        fi
    else
        print_success ".env file exists"
    fi
}

# Function to build and start development environment
deploy_dev() {
    print_status "Deploying development environment..."
    
    check_docker
    check_docker_compose
    setup_env
    
    print_status "Building and starting services..."
    docker-compose up --build -d
    
    print_success "Development environment deployed successfully!"
    print_status "Services available at:"
    echo "  - Frontend: http://localhost:3000"
    echo "  - Backend API: http://localhost:8000"
    echo "  - API Documentation: http://localhost:8000/docs"
    echo "  - Database: localhost:5432"
}

# Function to deploy production environment
deploy_prod() {
    print_status "Deploying production environment..."
    
    check_docker
    check_docker_compose
    setup_env
    
    print_warning "Make sure you have configured your .env file for production!"
    read -p "Continue with production deployment? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_status "Deployment cancelled"
        exit 0
    fi
    
    print_status "Building and starting production services..."
    docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d
    
    print_success "Production environment deployed successfully!"
    print_status "Services available at:"
    echo "  - Frontend: http://localhost (or your domain)"
    echo "  - Backend API: http://localhost:8000"
    echo "  - API Documentation: http://localhost:8000/docs"
}

# Function to stop all services
stop_services() {
    print_status "Stopping all services..."
    docker-compose down
    print_success "All services stopped"
}

# Function to view logs
view_logs() {
    print_status "Showing logs for all services..."
    docker-compose logs -f
}

# Function to clean up everything
cleanup() {
    print_warning "This will remove all containers, volumes, and images. Are you sure?"
    read -p "Continue with cleanup? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_status "Cleanup cancelled"
        exit 0
    fi
    
    print_status "Cleaning up..."
    docker-compose down -v --rmi all
    print_success "Cleanup completed"
}

# Function to show status
show_status() {
    print_status "Checking service status..."
    docker-compose ps
}

# Function to show help
show_help() {
    echo "Full-Stack Application Deployment Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  dev       Deploy development environment"
    echo "  prod      Deploy production environment"
    echo "  stop      Stop all services"
    echo "  logs      View logs for all services"
    echo "  status    Show status of all services"
    echo "  cleanup   Remove all containers, volumes, and images"
    echo "  help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 dev     # Deploy development environment"
    echo "  $0 prod    # Deploy production environment"
    echo "  $0 logs    # View logs"
}

# Main script logic
case "${1:-help}" in
    dev)
        deploy_dev
        ;;
    prod)
        deploy_prod
        ;;
    stop)
        stop_services
        ;;
    logs)
        view_logs
        ;;
    status)
        show_status
        ;;
    cleanup)
        cleanup
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        show_help
        exit 1
        ;;
esac 