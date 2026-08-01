from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
def test_health(): assert client.get('/health').status_code==200
def test_release_lifecycle():
    rows=client.get('/api/releases').json();assert rows
    created=client.post('/api/releases',json={"service":"billing","version":"1.0.0","environment":"staging","strategy":"canary","commit_sha":"abcdef1"})
    assert created.status_code==201
    promoted=client.post(f"/api/releases/{created.json()['id']}/promote")
    assert promoted.status_code==201 and promoted.json()['environment']=='production'
