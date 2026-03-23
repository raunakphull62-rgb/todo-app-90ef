# Setup Guide
## Introduction
This is a REST API for managing todo items. The API uses FastAPI as the web framework, Supabase as the database, and JWT for authentication.

## Prerequisites
* Python 3.8 or higher
* pip 20.0 or higher
* A Supabase instance
* A .env file with the following environment variables:
	+ SUPABASE_URL
	+ SUPABASE_KEY
	+ JWT_SECRET

## Installation
1. Clone the repository: `git clone https://github.com/your-username/todo-app.git`
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate` (on Linux/Mac) or `venv\Scripts\activate` (on Windows)
4. Install the dependencies: `pip install -r requirements.txt`
5. Create a .env file with the required environment variables

## Running the Application
1. Activate the virtual environment: `source venv/bin/activate` (on Linux/Mac) or `venv\Scripts\activate` (on Windows)
2. Run the application: `uvicorn main:app --host 0.0.0.0 --port 8000`

## API Endpoints
The API has two main endpoints: User and Todo. The User endpoint is used for user authentication and management, while the Todo endpoint is used for managing todo items.

## API Documentation
The API documentation is available at `http://localhost:8000/docs` after running the application.

## Environment Variables
The following environment variables are required:
* `SUPABASE_URL`: The URL of the Supabase instance
* `SUPABASE_KEY`: The key for the Supabase instance
* `JWT_SECRET`: The secret key for JWT authentication

## Railway Deployment
To deploy the application to Railway, follow these steps:
1. Create a Railway account and a new project
2. Link your GitHub repository to the Railway project
3. Configure the environment variables in the Railway project settings
4. Deploy the application to Railway

## Contributing
Contributions are welcome! Please submit a pull request with your changes and a brief description of what you've changed.