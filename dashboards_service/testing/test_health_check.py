import sys
import os

# Proje kök dizinini PYTHONPATH'e ekle
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)  # Kök dizin
sys.path.append(project_root)

from app import app  # FastAPI uygulamasını buradan import et
from fastapi.testclient import TestClient

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Dashboard Service"}