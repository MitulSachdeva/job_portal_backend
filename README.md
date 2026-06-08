# Job Portal Backend

A RESTful Job Portal Backend API built with FastAPI, PostgreSQL, SQLAlchemy, and JWT Authentication.

## Features

* User Registration & Login
* JWT Authentication
* Role-Based Access Control (Seeker / Hirer)
* Create and View Job Listings
* Apply to Jobs
* View Applications
* PostgreSQL Database Integration
* Alembic Database Migrations
* Environment Variable Configuration
* Interactive Swagger API Documentation

## Tech Stack

* FastAPI
* PostgreSQL
* SQLAlchemy
* Alembic
* JWT Authentication
* Pydantic
* Python-Dotenv
* Uvicorn

## Project Structure

```text
backend/
│
├── alembic/
├── auth.py
├── crud.py
├── database.py
├── main.py
├── models.py
├── schemas.py
├── requirements.txt
└── .env
```

## API Endpoints

### Authentication

| Method | Endpoint  | Description              |
| ------ | --------- | ------------------------ |
| POST   | /register | Register a new user      |
| POST   | /token    | Login and get JWT token  |
| GET    | /me       | Get current user profile |

### Jobs

| Method | Endpoint       | Description               |
| ------ | -------------- | ------------------------- |
| POST   | /jobs          | Create a job (Hirer only) |
| GET    | /jobs          | Get all jobs              |
| GET    | /jobs/{job_id} | Get a specific job        |

### Applications

| Method | Endpoint                    | Description                 |
| ------ | --------------------------- | --------------------------- |
| POST   | /jobs/{job_id}/apply        | Apply for a job             |
| GET    | /jobs/{job_id}/applications | View applications for a job |

## Installation

Clone the repository:

```bash
git clone https://github.com/MitulSachdeva/job_portal_backend.git
cd job_portal_backend/backend
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file inside the backend directory:

```env
DATABASE_URL=your_postgresql_connection_string
SECRET_KEY=your_secret_key
```

## Run the Application

```bash
uvicorn main:app --reload
```

API Documentation:

```text
http://127.0.0.1:8000/docs
```

## Database Migrations

Create a migration:

```bash
alembic revision --autogenerate -m "migration_name"
```

Apply migrations:

```bash
alembic upgrade head
```

## Future Improvements

* Resume Upload Support
* Company Profiles
* Job Search & Filtering
* Email Notifications
* Docker Support
* Frontend Integration
* Deployment Pipeline

## Author

Mitul Sachdeva

## License

This project is for educational and portfolio purposes.
