#!/usr/bin/env python3
"""
Test script for the Task Manager API
This script demonstrates how to use the API endpoints
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8000/api"
HEADERS = {"Content-Type": "application/json"}

def print_response(response, title):
    """Print formatted response"""
    print(f"\n{'='*50}")
    print(f"{title}")
    print(f"{'='*50}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_api():
    """Test the Task Manager API"""
    
    print("🚀 Testing Task Manager API")
    print("Make sure the server is running on http://localhost:8000")
    
    # Test 1: Register a new user
    print("\n1. Registering a new user...")
    register_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register/", 
                               json=register_data, 
                               headers=HEADERS)
        print_response(response, "User Registration")
        
        if response.status_code == 201:
            token = response.json()["token"]
            auth_headers = {**HEADERS, "Authorization": f"Token {token}"}
            print(f"✅ Registration successful! Token: {token[:20]}...")
        else:
            print("❌ Registration failed, trying login...")
            # Try to login if user already exists
            login_data = {
                "username": "testuser",
                "password": "testpass123"
            }
            response = requests.post(f"{BASE_URL}/auth/login/", 
                                   json=login_data, 
                                   headers=HEADERS)
            print_response(response, "User Login")
            token = response.json()["token"]
            auth_headers = {**HEADERS, "Authorization": f"Token {token}"}
            print(f"✅ Login successful! Token: {token[:20]}...")
    
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed! Make sure the server is running.")
        return
    
    # Test 2: Create tasks
    print("\n2. Creating tasks...")
    tasks_data = [
        {
            "title": "Complete Django API Project",
            "description": "Finish building the Task Manager API with all features"
        },
        {
            "title": "Write Documentation",
            "description": "Create comprehensive API documentation and README"
        },
        {
            "title": "Run Tests",
            "description": "Execute all unit tests and ensure coverage"
        }
    ]
    
    created_tasks = []
    for i, task_data in enumerate(tasks_data, 1):
        response = requests.post(f"{BASE_URL}/tasks/", 
                               json=task_data, 
                               headers=auth_headers)
        print_response(response, f"Create Task {i}")
        if response.status_code == 201:
            created_tasks.append(response.json())
            print(f"✅ Task {i} created successfully!")
    
    # Test 3: Get all tasks
    print("\n3. Getting all tasks...")
    response = requests.get(f"{BASE_URL}/tasks/", headers=auth_headers)
    print_response(response, "Get All Tasks")
    
    # Test 4: Get a specific task
    if created_tasks:
        task_id = created_tasks[0]["id"]
        print(f"\n4. Getting task {task_id}...")
        response = requests.get(f"{BASE_URL}/tasks/{task_id}/", headers=auth_headers)
        print_response(response, f"Get Task {task_id}")
    
    # Test 5: Update a task
    if created_tasks:
        task_id = created_tasks[0]["id"]
        print(f"\n5. Updating task {task_id}...")
        update_data = {
            "title": "Updated: Complete Django API Project",
            "description": "Updated description with more details",
            "completed": True
        }
        response = requests.put(f"{BASE_URL}/tasks/{task_id}/", 
                              json=update_data, 
                              headers=auth_headers)
        print_response(response, f"Update Task {task_id}")
    
    # Test 6: Toggle task completion
    if len(created_tasks) > 1:
        task_id = created_tasks[1]["id"]
        print(f"\n6. Toggling completion for task {task_id}...")
        response = requests.patch(f"{BASE_URL}/tasks/{task_id}/toggle_complete/", 
                                headers=auth_headers)
        print_response(response, f"Toggle Task {task_id} Completion")
    
    # Test 7: Filter completed tasks
    print("\n7. Getting completed tasks...")
    response = requests.get(f"{BASE_URL}/tasks/completed/", headers=auth_headers)
    print_response(response, "Get Completed Tasks")
    
    # Test 8: Filter pending tasks
    print("\n8. Getting pending tasks...")
    response = requests.get(f"{BASE_URL}/tasks/pending/", headers=auth_headers)
    print_response(response, "Get Pending Tasks")
    
    # Test 9: Search tasks
    print("\n9. Searching tasks...")
    response = requests.get(f"{BASE_URL}/tasks/?search=Django", headers=auth_headers)
    print_response(response, "Search Tasks (Django)")
    
    # Test 10: Order tasks
    print("\n10. Ordering tasks by title...")
    response = requests.get(f"{BASE_URL}/tasks/?ordering=title", headers=auth_headers)
    print_response(response, "Order Tasks by Title")
    
    # Test 11: Delete a task
    if created_tasks:
        task_id = created_tasks[-1]["id"]
        print(f"\n11. Deleting task {task_id}...")
        response = requests.delete(f"{BASE_URL}/tasks/{task_id}/", headers=auth_headers)
        print(f"\n{'='*50}")
        print(f"Delete Task {task_id}")
        print(f"{'='*50}")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 204:
            print("✅ Task deleted successfully!")
        else:
            print(f"❌ Failed to delete task: {response.text}")
    
    print("\n🎉 API testing completed!")
    print("\n📚 API Documentation available at:")
    print("   - Swagger UI: http://localhost:8000/swagger/")
    print("   - ReDoc: http://localhost:8000/redoc/")
    print("\n🔧 Admin Interface: http://localhost:8000/admin/")

if __name__ == "__main__":
    test_api() 