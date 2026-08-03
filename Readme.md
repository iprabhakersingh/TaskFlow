# 🚀 TaskFlow - Task Management API with Notifications

A production-ready backend Task Management API built with **FastAPI**, **PostgreSQL**, **Redis**, **Celery**, and **JWT Authentication**.

TaskFlow allows users to create projects, manage tasks, assign users, receive automatic notifications for overdue tasks, and efficiently retrieve data using Redis caching.

This project was built as part of a Backend Engineer Take-Home Assignment.

---

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
  - Todo
  - In Progress
  - Done
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

# Running Locally

Clone repository

```bash
git clone <repository-url>
```

Move into project

```bash
cd taskflow
```

Create environment file

```bash
cp .env.example .env
```

Fill the environment variables.

---

## Run with Docker

```bash
docker compose up --build
```

Application

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

# Running Tests

```
pytest -v
```

The test suite covers

- Authorization
- Core API flow
- Cache invalidation
- Background notifications

---

# CI/CD

GitHub Actions automatically

- Builds Docker containers
- Starts required services
- Executes the complete pytest suite

Pipeline passes before deployment.

---

# Deployment

The application is deployed on Railway.

Services deployed

- FastAPI API
- PostgreSQL
- Redis
- Celery Worker
- Celery Beat Scheduler

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

# Author

**Prabhaker Singh**

Backend Engineer | FastAPI | PostgreSQL | Redis | Celery | Docker
