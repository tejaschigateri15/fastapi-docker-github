# FastAPI Robot Framework Testing Project

This project demonstrates a FastAPI application with automated testing using Robot Framework. It includes Docker containerization for consistent deployment and testing.

## 🚀 Features

- FastAPI REST API endpoints
- Robot Framework automated testing
- Docker containerization
- Continuous Integration ready

## 📋 Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Git

## 🛠️ Installation

### Local Development Setup

1. Clone the repository:
```bash
git clone [your-repository-url]
cd [repository-name]
```

2. Create and activate virtual environment:
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install fastapi uvicorn robotframework robotframework-requests requests
```

### Docker Setup

1. Build and run using Docker:
```bash
docker build -t fastapi-robot .
docker run -p 8000:8000 fastapi-robot
```

2. Using Docker Compose:
```bash
docker-compose up -d
```

## 🏃‍♂️ Running the Application

### Local Development
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Docker
The application will automatically start when running the Docker container.

## 🧪 Running Tests

### Local Tests
```bash
robot test_api.robot
```

## 🔑 API Endpoints

- `GET /`: Returns a hello message
  - Response: `{"Hello": "test123"}`


## 🐳 Docker Commands

- Build image: `docker build -t fastapi-robot .`
- Run container: `docker run -p 8000:8000 fastapi-robot`
- Run tests: `docker exec -it [container-name] robot test_api.robot`
- Stop container: `docker stop [container-name]`
