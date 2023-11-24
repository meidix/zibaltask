# Quick Start

This project is a distributed application. To run it you need to have `docker` and `docker compose` installed on your system. After installing the prerequisites in the root directory run the following command:

```bash
docker compose up --build
```

This will spawn all the neccessary servers and the API endpoints will be availabe at `localhost:8000` and `localhost:8080`.

# Introduction

zibaltask consists of two `django` apps, a `rabbitmq` instance, `mongodb` and 2 `celery workers` and a `celery beat` server. the `django` apps are referred to as the `notification-service` and the `reports-service`. The `celery workers` use `mongodb` as the result backedn and the `rabbitmq` instance as the broker. each worker is responsible for receiving and processing the tasks of one of the services mentioned earlier.

# Reports Service

This `django` app provides API endpoints for generating a summary of transactions of users which are referred to as merchants. Transactions are stored in the `mongodb`. Since these operations have high computational complexity, a django command is also provided in this app which allows for caching an intermediate level of the operations to enable faster response times by reducing the computational overhead of the operation.To use this functionality you need to run the following command in the terminal after, deploying the app:

```bash
docker compose exec -it reports_service python manage.py summarizetransaction
```

This service also uses the `celery beat` container to generate daily reports of each merchant's transaction, and sending it to the merchant using the second `django` app which we will discuss later. The API documentation is available at :

- [https://documenter.getpostman.com/view/25449104/2s9YeD7YB6](Report Service API Documentation)

# Notification Service
