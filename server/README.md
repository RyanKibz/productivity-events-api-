
# Productivity Events API

## Project Overview

The Productivity Events API is a RESTful backend application
built using Flask and Python.

It allows users to register, log in, and manage their
personal productivity events.

Each user can only access, update, or delete events
that belong to their account.

## Technologies Used

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Bcrypt
- Flask-WTF
- SQLite
- Pipenv

## Features

- User registration and login
- Session-based authentication
- Secure password hashing
- CSRF protection
- Create, read, update, and delete events
- User-specific event access
- Event pagination
- Database migrations
- Database seeding

## Installation

Navigate to the server directory:

```bash
cd server
```

Install dependencies:

```bash
pipenv install
```

Activate the virtual environment:

```bash
pipenv shell
```

## Database Setup

Run database migrations:

```bash
flask --app app db upgrade
```

Seed the database with sample data:

```bash
python seed.py
```

## Running the Application

Start the Flask development server:

```bash
flask --app app run --port 5555
```

The API will be available at:

http://127.0.0.1:5555

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /csrf-token | Generate a CSRF token |
| POST | /signup | Register a user |
| POST | /login | Log in |
| POST | /logout | Log out |
| GET | /check_session | Check current session |
| GET | /me | Get current user |
| GET | /events | Get paginated user events |
| POST | /events | Create an event |
| GET | /events/:id | Get an event |
| PATCH | /events/:id | Update an event |
| DELETE | /events/:id | Delete an event |

## Authentication and Security

The application uses Flask sessions for authentication.

Passwords are securely hashed using Flask-Bcrypt.

CSRF protection is implemented using Flask-WTF.
Requests that modify data must include a valid
CSRF token in the X-CSRFToken header.

Users cannot access or modify events belonging
to other users.

## Pagination

The GET /events endpoint supports pagination
using page and per_page query parameters.

Example:

GET /events?page=1&per_page=10

## Author
 
 SEREM RYAN KIBET

