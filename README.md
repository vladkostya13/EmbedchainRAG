# Embedchain RAG Project

This project is designed to implement and run an Embedchain RAG (Retrieval-Augmented Generation) application, focusing on integrating Ollama and Neural-Chat models for advanced query handling and response generation. It leverages FastAPI for creating a responsive and efficient API service.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3.12
- Docker and Docker Compose

You'll also need to install specific models and dependencies:

- Ollama
- Neural-Chat model

Dependencies should be installed using the `requirements.txt` file included in the project:

`pip install -r requirements.txt`


Ensure Docker is running on your machine, then build and start the services using Docker Compose:

`docker-compose up --build`

This will start the application in a Docker container, installing all necessary dependencies as outlined in the Dockerfile and `requirements.txt`.

## Running the Application

After starting the application with Docker Compose, you can access the application at:

- Application: `http://localhost:8080`
- API Documentation (Swagger UI): `http://localhost:8080/docs`

## Built With

* [FastAPI](https://fastapi.tiangolo.com/) - The web framework used
* [Uvicorn](https://www.uvicorn.org/) - ASGI server for FastAPI
* [Docker](https://www.docker.com/) - Containerization
