# Task Manager API

A comprehensive RESTful API for managing tasks with user authentication, built using Django and Django REST Framework.

## Features

- **User Authentication**: Token-based authentication with registration and login
- **CRUD Operations**: Full Create, Read, Update, Delete operations for tasks
- **Task Management**: Create, view, update, and delete tasks
- **Filtering & Search**: Filter tasks by completion status, search by title/description
- **Pagination**: Built-in pagination for large task lists
- **API Documentation**: Interactive Swagger/OpenAPI documentation
- **Admin Interface**: Django admin for task management
- **Comprehensive Testing**: Unit tests for all endpoints

## Requirements

- Python 3.8+
- Django 5.0+
- Django REST Framework
- Django CORS Headers
- Django Filter
- drf-yasg (Swagger documentation)

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd task-manager-api
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser** (optional):
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authentication

#### Register User
- **URL**: `/api/auth/register/`
- **Method**: `POST`
- **Description**: Register a new user account
- **Request Body**:
  ```json
  {
    "username": "newuser",
    "email": "user@example.com",
    "password": "securepassword123"
  }
  ```
- **Response**:
  ```json
  {
    "token": "your-auth-token",
    "user_id": 1,
    "username": "newuser",
    "email": "user@example.com"
  }
  ```

#### Login User
- **URL**: `/api/auth/login/`
- **Method**: `POST`
- **Description**: Authenticate user and get token
- **Request Body**:
  ```json
  {
    "username": "username",
    "password": "password"
  }
  ```
- **Response**:
  ```json
  {
    "token": "your-auth-token",
    "user_id": 1,
    "username": "username",
    "email": "user@example.com"
  }
  ```

### Tasks

#### Get All Tasks
- **URL**: `/api/tasks/`
- **Method**: `GET`
- **Authentication**: Required
- **Query Parameters**:
  - `completed`: Filter by completion status (true/false)
  - `search`: Search in title and description
  - `ordering`: Order by field (created_at, updated_at, title)
  - `page`: Page number for pagination
- **Response**:
  ```json
  {
    "count": 10,
    "next": "http://localhost:8000/api/tasks/?page=2",
    "previous": null,
    "results": [
      {
        "id": 1,
        "title": "Complete project",
        "description": "Finish the Django API project",
        "completed": false,
        "created_at": "2024-01-15T10:30:00Z"
      }
    ]
  }
  ```

#### Get Single Task
- **URL**: `/api/tasks/{id}/`
- **Method**: `GET`
- **Authentication**: Required
- **Response**:
  ```json
  {
    "id": 1,
    "title": "Complete project",
    "description": "Finish the Django API project",
    "completed": false,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z",
    "user": {
      "id": 1,
      "username": "username",
      "email": "user@example.com"
    }
  }
  ```

#### Create Task
- **URL**: `/api/tasks/`
- **Method**: `POST`
- **Authentication**: Required
- **Request Body**:
  ```json
  {
    "title": "New Task",
    "description": "Task description"
  }
  ```
- **Response**: Same as Get Single Task

#### Update Task
- **URL**: `/api/tasks/{id}/`
- **Method**: `PUT`
- **Authentication**: Required
- **Request Body**:
  ```json
  {
    "title": "Updated Task",
    "description": "Updated description",
    "completed": true
  }
  ```
- **Response**: Same as Get Single Task

#### Delete Task
- **URL**: `/api/tasks/{id}/`
- **Method**: `DELETE`
- **Authentication**: Required
- **Response**: 204 No Content

#### Get Completed Tasks
- **URL**: `/api/tasks/completed/`
- **Method**: `GET`
- **Authentication**: Required
- **Response**: Same as Get All Tasks (filtered)

#### Get Pending Tasks
- **URL**: `/api/tasks/pending/`
- **Method**: `GET`
- **Authentication**: Required
- **Response**: Same as Get All Tasks (filtered)

#### Toggle Task Completion
- **URL**: `/api/tasks/{id}/toggle_complete/`
- **Method**: `PATCH`
- **Authentication**: Required
- **Response**: Same as Get Single Task

## Usage Examples

### Using curl

1. **Register a new user**:
   ```bash
   curl -X POST http://localhost:8000/api/auth/register/ \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "email": "test@example.com", "password": "testpass123"}'
   ```

2. **Login**:
   ```bash
   curl -X POST http://localhost:8000/api/auth/login/ \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "password": "testpass123"}'
   ```

3. **Create a task** (replace `YOUR_TOKEN` with the actual token):
   ```bash
   curl -X POST http://localhost:8000/api/tasks/ \
     -H "Authorization: Token YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"title": "My first task", "description": "This is a test task"}'
   ```

4. **Get all tasks**:
   ```bash
   curl -X GET http://localhost:8000/api/tasks/ \
     -H "Authorization: Token YOUR_TOKEN"
   ```

### Using Python requests

```python
import requests

# Base URL
base_url = "http://localhost:8000/api"

# Register
response = requests.post(f"{base_url}/auth/register/", json={
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123"
})
token = response.json()["token"]

# Set headers for authenticated requests
headers = {"Authorization": f"Token {token}"}

# Create a task
response = requests.post(f"{base_url}/tasks/", json={
    "title": "Python task",
    "description": "Created via Python requests"
}, headers=headers)

# Get all tasks
response = requests.get(f"{base_url}/tasks/", headers=headers)
tasks = response.json()
```

## Testing

Run the test suite:

```bash
python manage.py test
```

Run tests with coverage:

```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

## API Documentation

Interactive API documentation is available at:
- **Swagger UI**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/

## Admin Interface

Access the Django admin interface at http://localhost:8000/admin/ using the superuser credentials.

## Project Structure

```
task_manager/
├── task_manager/          # Main project settings
│   ├── settings.py       # Django settings
│   ├── urls.py          # Main URL configuration
│   └── wsgi.py          # WSGI configuration
├── tasks/               # Tasks app
│   ├── models.py        # Task model
│   ├── serializers.py   # API serializers
│   ├── views.py         # API views
│   ├── urls.py          # App URL configuration
│   ├── admin.py         # Admin interface
│   └── tests.py         # Unit tests
├── manage.py            # Django management script
└── README.md           # This file
```

## Security Features

- Token-based authentication
- User isolation (users can only access their own tasks)
- Input validation and sanitization
- CORS configuration for cross-origin requests

## Performance Features

- Database indexing on frequently queried fields
- Pagination for large datasets
- Efficient filtering and search capabilities
- Optimized database queries

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 