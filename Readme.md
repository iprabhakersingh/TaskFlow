# 🚀 TaskFlow - Task Management API with Notifications

A production-ready backend Task Management API built with **FastAPI**, **PostgreSQL**, **Redis**, **Celery**, and **JWT Authentication**.

TaskFlow allows users to create projects, manage tasks, assign users, receive automatic notifications for overdue tasks, and efficiently retrieve data using Redis caching.

This project was built as part of a Backend Engineer Take-Home Assignment.

## Repository

https://github.com/iprabhakersingh/TaskFlow

---

| Requirement | Status |
|-------------|--------|
| Authentication | ✅ |
| Project & Task CRUD | ✅ |
| Authorization | ✅ |
| Background Notifications (Celery) | ✅ |
| Redis Caching & Invalidation | ✅ |
| Health & Metrics Endpoints | ✅ |
| Docker & Docker Compose | ✅ |
| **GitHub Actions CI (Passing)** | ✅ |
| Test Suite (Pytest) | ✅ |
| Railway Deployment | ✅ |

### Minor UI Limitation

FastAPI's Swagger UI uses the standard OAuth2 form, where the login field is labeled **"username"**. In this project, authentication is performed using the user's **email address**, so users should provide their email in the `username` field. This is a UI labeling limitation of the default Swagger form rather than a backend authentication issue.

# Features

## Authentication

- User Registration
- User Login
- JWT Authentication
- Password hashing using bcrypt
- Protected API endpoints

---

## Projects

- Create Project
- Update Project
- Delete Project
- List Projects
- Authorization (Users can only access their own projects)

---

## Tasks

Each task contains

- Title
- Description
- Status
  - Pending
  - In Progress
  - Completed
- Assignee
- Due Date

Supports

- Create Task
- Update Task
- Delete Task
- List Tasks

---

## Search & Filtering

Supports filtering tasks by

- Status
- Assignee
- Due Date Range

Pagination is also supported.

---

## Notifications

Notifications are generated automatically when

- A task becomes overdue
- A task is reassigned

Notification creation runs asynchronously using **Celery**.

Notifications are stored in the database (no email/SMS integration).

---

## Background Processing

Uses

- Celery Worker
- Celery Beat Scheduler
- Redis Message Broker

Celery Beat periodically checks overdue tasks and dispatches notification jobs.

---

## Redis Caching

Task listing endpoints are cached using Redis.

Cache is automatically invalidated whenever

- Task is created
- Task is updated
- Task is deleted
- Task status changes

This prevents stale responses while improving API performance.

---

## Monitoring

Endpoints

```
GET /health
GET /metrics
```

---

# Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Redis
- Celery
- JWT
- Passlib (bcrypt)
- Docker
- Docker Compose
- GitHub Actions
- Railway

---

# Project Structure

```
taskflow
│
├── app
│   ├── api
│   ├── core
│   ├── db
│   ├── middleware
│   ├── models
│   ├── schemas
│   ├── tasks
│   └── main.py
│
├── tests
│    ├── conftest.py
│    ├── test_authorization.py
│    ├── test_cache.py
│    ├── test_core_flow.py
│    ├── test_notifications.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# Architecture

```
                    Client
                       │
                       ▼
                FastAPI Application
                       │
      ┌────────────────┼────────────────┐
      │                │                │
      ▼                ▼                ▼
 PostgreSQL         Redis Cache     Celery Producer
      │                                  │
      │                                  ▼
      │                           Redis Broker
      │                                  │
      ▼                                  ▼
 Stored Data                    Celery Worker
                                        │
                                        ▼
                              Notification Table

                       Celery Beat
                             │
                             ▼
                 Periodic Overdue Task Checks
```

---

## Local Setup

Clone the repository

```bash
git clone <repository-url>
```

Navigate to the project

```bash
cd taskflow
```

Copy the environment file

```bash
cp .env.example .env
```

Update the environment variables.

Start the application

## Run with Docker

```bash
docker compose up --build
```
The API will be available at

```
http://localhost:8000
```

Swagger

```
http://localhost:8000/docs
```
---

# Environment Variables

Required

```
DATABASE_URL=

REDIS_URL=

SECRET_KEY=

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## Testing

The project includes an automated test suite covering authentication, authorization, CRUD operations, cache behavior, and background notification workflows.

Test suite includes:

- Authentication
- Authorization
- Project CRUD
- Task CRUD
- Redis cache behaviour
- Notification flow
- Background job triggering

The project also uses **Flake8** to enforce Python code quality and style consistency.

Run locally:

```bash
flake8
pytest -v 
```

---

## CI/CD

GitHub Actions is configured to automatically validate every push to the repository.

The CI pipeline performs the following steps:

- Checks out the repository
- Sets up Python 3.11
- Installs project dependencies
- Runs Flake8 for code quality checks
- Creates the required `.env` file for the CI environment
- Builds the complete Docker Compose stack
- Waits for all services to become healthy
- Executes the complete Pytest test suite
- Shuts down the Docker containers after testing

**Current Status:** ✅ All Flake8 checks and Pytest test cases are passing successfully.![CI](https://github.com/iprabhakersingh/TaskFlow/actions/workflows/ci.yml/badge.svg)

### CI Status

- ✅ Flake8 linting passed
- ✅ Docker Compose build passed
- ✅ Pytest test suite passed
- ✅ GitHub Actions pipeline passing

---

## Development Process

The repository contains incremental commits demonstrating the development process rather than a single final commit, allowing reviewers to observe the project's evolution.

# Deployment (Railway)

Railway Deployment:

https://taskflow-production-28d0.up.railway.app/

Swagger UI:

https://taskflow-production-28d0.up.railway.app/docs

### Components (Services)

- **TaskFlow** – FastAPI application serving the REST API.
- **PostgreSQL** – Primary relational database.
- **Redis** – Message broker and caching layer.
- **Celery Worker** – Executes asynchronous background tasks.
- **Celery Beat** – Schedules periodic tasks (e.g., checking overdue tasks).

The FastAPI application communicates with PostgreSQL for persistent storage and Redis for caching and task queuing. Celery Worker consumes tasks from Redis, while Celery Beat periodically schedules background jobs.

## Deployment Steps

1. Push the project to GitHub.
2. Create a new Railway project.
3. Deploy the FastAPI application from the GitHub repository.
4. Add a PostgreSQL service.
5. Add a Redis service.
6. Configure all required environment variables.
7. Create separate Railway services for:
   - Celery Worker
   - Celery Beat
8. Redeploy the services.
9. Verify the deployment using the `/docs` endpoint.

Once deployed, the application becomes accessible through the Railway-generated public URL.

---

## Architecture

```
                 Railway
                    │
     ┌──────────────┴──────────────┐
     │                             │
 FastAPI API                  PostgreSQL
     │
     ├──────────────► Redis
     │                    │
     │                    ├── Celery Worker
     │                    └── Celery Beat

```
---

# API Documentation

Swagger UI

```
/docs
```

OpenAPI JSON

```
/openapi.json
```

---

# Design Decisions

### JWT Authentication

JWT was selected because it provides a stateless authentication mechanism suitable for REST APIs.

---

### Redis Cache

Redis was introduced to reduce repeated database reads for frequently accessed task lists while maintaining consistency through cache invalidation.

---

### Celery

Notification creation is handled asynchronously so API responses remain fast and background work is processed independently.

---

### PostgreSQL

Chosen as the primary relational database because of its reliability and production readiness.

---

# Trade-offs

Due to time constraints, the following improvements were not implemented.

- Refresh Tokens
- Role-based access control (Admin/User)
- Email notification integration
- WebSocket live notifications
- Advanced monitoring dashboards
- API rate limiting
- Distributed tracing
- Container orchestration (Kubernetes)

---

# What I'd Do With More Time

If given additional time, I would

- Add comprehensive API documentation examples
- Implement refresh token rotation
- Introduce RBAC with roles and permissions
- Add WebSocket-based real-time notifications
- Integrate email delivery
- Improve observability using Prometheus and Grafana
- Increase automated test coverage
- Add Kubernetes deployment manifests
- Improve performance benchmarking

---

# Assignment Requirements Status

| Requirement | Status |
|-------------|--------|
| Authentication | ✅ |
| Project CRUD | ✅ |
| Task CRUD | ✅ |
| Authorization | ✅ |
| Background Jobs | ✅ |
| Redis Cache | ✅ |
| Cache Invalidation | ✅ |
| Health Endpoint | ✅ |
| Metrics Endpoint | ✅ |
| Docker | ✅ |
| Docker Compose | ✅ |
| Railway Deployment | ✅ |
| GitHub Actions CI | ✅ |
| Test Suite | ✅ |

---

## Learning & Design Approach

This project was developed as a backend engineering assignment with the goal of applying production-oriented backend concepts, including authentication, authorization, background processing, caching, containerization, automated testing, CI/CD, and cloud deployment. The implementation prioritizes clean architecture, readability, and maintainability while satisfying the assignment requirements.

# Author

**Prabhaker Singh**

Backend Engineer | FastAPI | PostgreSQL | Redis | Celery | Docker

## License

This project was developed for a Backend Engineer Take-Home Assignment and is intended for educational and evaluation purposes.
