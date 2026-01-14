# Auth with Flask

A simple fullstack application demonstrating **Flask**, **Python**, **MySQL**, **Docker**, and **Docker Compose**.  

This project makes use of Python features such as **Decorators** and **Type Hints / Generics**, and the codebase is **fully type-hinted wherever possible** for readability and maintainability.  
It also mimics Rust's `Result<T, E>` pattern at the **library level**, providing similar error-handling semantics without changing the Python language or compiler.  

The frontend uses **Bootstrap**, **vanilla JavaScript**, and **small custom CSS** for styling and interactivity.  

The project includes a **Docker Compose** setup to quickly run the entire application, networking the app container and the database container seamlessly.

## Features

- User authentication and authorization  
- Python Decorators and Type Hints / Generics for readability  
- Rust-inspired `Result<T, E>` pattern mimic  
- MySQL database integration  
- Fully containerized using Docker and Docker Compose  
- Frontend styling and interactivity with **Bootstrap**, **vanilla JavaScript**, and **small custom CSS**

## Requirements

- **Python:** 3.10 or higher (3.12 recommended)  
- **Docker**  
- **Docker Compose**  
- **MySQL** (for local development without Docker)  

## Setup

1. Clone the repository:  
   ```bash
   git clone https://github.com/v-inmar/auth-with-flask.git
   cd auth-with-flask

   or

   git clone https://github.com/v-inmar/auth-with-flask.git mydirectory
   cd mydirectory
   ```

## Running with Docker Compose

You can quickly start the entire application (app + database) using Docker Compose:

1. Build and start the containers:  
   ```bash
   docker-compose up --build
   ```
2. Access the application at:  
   ```
   http://localhost:5000
   ```
3. Stop the containers when done:  
   ```bash
   docker-compose down
   ```
This setup automatically networks the Flask app and MySQL database containers, so no additional configuration is required.

## Running Locally for Development

You can also run the app manually for development purposes, without Docker:

1. Create a `.env` file, check example_env file for values.
2. Create a `.flaskenv` file, check example_flaskenv file for values. 
3. Make sure a **MySQL instance is already running** with the same credentials as in `.env`.
4. Create and activate a Python virtual environment:  
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux / macOS
   venv\Scripts\activate      # Windows
   ```
5. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```
6. Run database migrations:  
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```
7. Start the Flask development server:  
   ```bash
   flask run --host="0.0.0.0" --port=5000 --debug --reload
   ```
8. Access the application at:  
   ```
   http://localhost:5000
   ```
This method allows you to work directly on the codebase and see changes live during development.

## Usage

- Register new users and log in and also log out
- Protected routes are included to showcase authorization
- Explore the authentication flows  
- Extend the app by modifying Python code or database schemas  

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.

## License
This project is licensed under the MIT License.
