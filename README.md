# Reliable API Handling with Asynchronous Scheduling

## Problem Statement

Application APIs typically have asynchronous requirements. These requests can include updating large datasets or depending on unpredictable services, and therefore need effective background scheduling to ensure requests can be fulfilled consistently and reliably. The goal is to find suitable libraries for scheduling asynchronous tasks in Python.

The challenge involves implementing server-side code using the chosen library to handle request asynchronous processing. Additionally, potential silent failures caused by the scheduler's inability to launch jobs due to system congestion or resource limits needs to be handled. This is crucial for ensuring reliable execution in a production environment.

---

### Libraries for Handling Asynchronous Tasks (in Python)

#### Celery

[Celery GitHub Link](https://github.com/celery/celery)

Celery is a robust distributed task processing system in Python, allowing the execution of tasks across multiple processes or even different machines. Celery enables us to create a distributed task processing system in Python, allowing use of wide range of message brokers (e.g Redis, RabbitMQ) to schedule and handle background tasks.

Celery is a well known and widely used library for handling complex task scheduling and processing needs. It includes features like task prioritization, backends for results, and scheduling periodic tasks.

#### Dramatiq

[Dramatiq GitHub Link](https://github.com/Bogdanp/dramatiq)

Dramatiq is a lightweight task queue system for Python. It simplifies the process of handling asynchronous tasks, providing a quick and straightforward way to manage tasks concurrently. It is designed with a clear syntax and a focus on simplicity, and is suitable for smaller projects and scenarios where ease of use is a priority.

Though not as well known and used as Celery, Dramatiq is a fast and reliable background task processing library in itself, also allowing integration with message brokers similar to Celery for effective background task scheduling.

---

### Asynchronous Task Handler Implementation

This project implements a solution for asynchronous task handling using **FastAPI** framework in combination with **Celery**. FastAPI serves as the web framework, handling API requests, while Celery takes care of executing background tasks asynchronously. 

#### Handling Silent Failure Cases

In order to handle the silent failure cases, situations where Celery, the task scheduler, may fail to launch a job due to system congestion or resource limits, the following approach has been implemented.

1. Database Logging

The project incorporates logging records of each background task / request to a database table as a persistent store, where relevant task information is recorded. This includes task IDs, request data, timestamps, and task status.

2. Continuous Monitoring

A separate task monitoring process runs continuously at scheduled intervals, ensuring that any pending tasks are regularly checked. Thus, by identifying and retrying pending tasks, the project minimizes the impact of silent failures on the overall reliability of asynchronous task processing.

3. Logging and Remark Updates

When the failed tasks are retried, the task status in the database is updated. The remarks are logged to the database to provide insights into the reason for the silent failure, helping in troubleshooting and analysis.

---

### Getting Started

To set up and run the project, follow these steps:

#### Prerequisites
- Docker: [Install Docker](https://docs.docker.com/engine/install/)
- Docker Compose: [Install Docker Compose](https://docs.docker.com/compose/install/)

#### Steps
1. Clone the repository

```bash
git clone https://github.com/yourusername/your-repo.git
```

2. Environment Configuration

Copy the .env.example file to .env and adjust the configuration parameters.

3. Build Docker Images

```bash
docker compose build
```

4. Start Docker Containers

```bash
docker compose up -d
```

5. Run FastAPI and Celery

- FastAPI: Access the FastAPI endpoints at http://localhost:5000
- Celery Flower (Task Monitor): Access Celery Flower at http://localhost:5555

6. Test the Endpoints

You can use the `curl` to send a POST request to http://localhost:5000/tasks with the provided data.

```bash
curl -X POST -H "Content-Type: application/json" -d '{"data": "test data"}' http://localhost:5000/tasks
```

7. Monitor Celery Tasks

Visit Celery Flower at http://localhost:5555 to monitor and inspect the tasks running asynchronously.

8. Stop and Remove Containers

```bash
   docker compose down
```

---

### Project Structure

#### Modules

#### `application_logs`

This module contains log files generated by the application. The logs include Celery task execution logs and scheduled task logs, along with the logs from the general program.

#### `broker-data`

This module stores data related to the Celery broker, specifically the Redis database dump file (`dump.rdb`) as a backup for persistent storage.

#### `db`

The `db` module contains functionalities related to database operations. Key files include:
- `database_logger.py`: Implements logging functionality to the database
- `db_connection.py`: Manages the database connection
- `db_helper.py`: Provides helper functions for database operations
- `models.py`: Defines database models

#### `logs`

This module contains configuration files and utility scripts for logging:
- `config.ini`: Configuration file for logging settings
- `get_logger.py`: Utility script to obtain the logger object


#### `middleware`

This module contains middleware functionality for the application. Currently, it includes a logger middleware (`logger.py`) to capture details on each request.

#### `monitor`

The `monitor` module implements a task monitoring process.
- `monitor.py`: Contains the logic for monitoring the log records in the database, and retrying failed tasks

#### `router`

The `router` module handles API routing:
- `api_routes.py`: Defines the API routes used

#### `usecase`

The `usecase` module contains business logic for tasks:
- `task.py`: Implements specific tasks that can be executed asynchronously

#### `worker`

This module contains the Celery initialization script:
- `worker.py`: Defines the Celery worker

#### `celeryconfig.py`

This Python script contains the configuration settings for the Celery.

#### `main.py`

The main entry point of the application, responsible for initiating and running the FastAPI server

#### `requestvars.py`
This module defines request variables used in the application

---