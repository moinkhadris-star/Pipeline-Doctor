import pytest
from app.github_client import GitHubClient

def test_github_connection():
    """Test GitHub API connects successfully"""
    client = GitHubClient()
    result = client.test_connection()
    assert "Connected as:" in result

def test_health_endpoint():
    """Test the health endpoint returns ok"""
    from fastapi.testclient import TestClient
    from app.main import app
    
    client = TestClient(app)
    response = client.get("/health")
    
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_invalid_repo():
    """Test handling of invalid repo name"""
    from fastapi.testclient import TestClient
    from app.main import app
    
    client = TestClient(app)
    response = client.post("/diagnose", json={
        "repo_name": "invalid-repo-no-slash"
    })
    
    assert response.status_code == 500