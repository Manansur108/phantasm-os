"""
Integration tests for FastAPI endpoints using TestClient.
"""

import pytest
from fastapi.testclient import TestClient
from phantasm_os.app import create_app


@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)


def test_system_info(client):
    res = client.get("/api/system/info")
    assert res.status_code == 200
    data = res.json()
    assert "Phantasm-OS" in data["os_name"]
    assert data["status"] == "ONLINE"


def test_vfs_endpoints(client):
    # List root
    res = client.get("/api/vfs/list?path=C:\\")
    assert res.status_code == 200
    items = res.json()
    assert len(items) > 0

    # Get node
    res = client.get("/api/vfs/node?path=C:\\AUTOEXEC.BAT")
    assert res.status_code == 200
    assert "CIPHER_SEED" in res.json()["content"]

    # Write node
    write_payload = {
        "path": "C:\\MYDOCS\\API_TEST.TXT",
        "content": "Created via API endpoint",
        "corrupt": False,
        "corrupt_level": 0.0
    }
    res = client.post("/api/vfs/write", json=write_payload)
    assert res.status_code == 200
    assert res.json()["name"] == "API_TEST.TXT"

    # Search
    res = client.get("/api/vfs/search?query=API_TEST")
    assert res.status_code == 200
    assert len(res.json()) >= 1

    # Glitch
    res = client.post("/api/vfs/glitch?path=C:\\MYDOCS\\API_TEST.TXT&intensity=0.5")
    assert res.status_code == 200
    assert res.json()["corrupted"] is True

    # Delete
    res = client.delete("/api/vfs/node?path=C:\\MYDOCS\\API_TEST.TXT")
    assert res.status_code == 200
    assert res.json()["status"] == "DELETED"


def test_vfs_hallucinate(client):
    res = client.post("/api/vfs/hallucinate", json={"path": "C:\\MYDOCS\\DREAM.TXT", "theme": "cyber"})
    assert res.status_code == 200
    assert "DREAM.TXT" in res.json()["name"]


def test_navigator_browse(client):
    res = client.post("/api/navigator/browse", json={"url": "http://www.geocities.com/area51"})
    assert res.status_code == 200
    page = res.json()
    assert "GEOCITIES.COM" in page["title"]
    assert page["hit_counter"] > 0

    hist = client.get("/api/navigator/history")
    assert hist.status_code == 200
    assert "http://www.geocities.com/area51" in hist.json()


def test_clippy_api(client):
    res = client.get("/api/clippy/greeting")
    assert res.status_code == 200
    assert "Cliptron" in res.json()["text"]

    interact_res = client.post("/api/clippy/interact", json={"query": "Who made you?"})
    assert interact_res.status_code == 200
    assert "Cliptron" in interact_res.json()["text"]


def test_mail_api(client):
    res = client.get("/api/mail/inbox")
    assert res.status_code == 200
    inbox = res.json()
    assert len(inbox) >= 3

    send_res = client.post("/api/mail/send", json={
        "to": "test@cyberspace.net",
        "subject": "Testing Mail 95",
        "body": "Does the simulated mail exchange work?"
    })
    assert send_res.status_code == 200
    assert "RE: Testing Mail 95" in send_res.json()["subject"]


def test_arg_api(client):
    status_res = client.get("/api/arg/status")
    assert status_res.status_code == 200
    assert status_res.json()["current_stage"] == 1

    # Cipher helper
    caesar_res = client.post("/api/arg/cipher/caesar?text=HELLO&shift=7")
    assert caesar_res.status_code == 200
    assert caesar_res.json()["output"] == "OLSSV"

    # Submit solution
    sub_res = client.post("/api/arg/submit", json={"solution": "http://www.phantasm.net/sector7/chimera"})
    assert sub_res.status_code == 200
    assert sub_res.json()["success"] is True


def test_dos_execution(client):
    # VER
    res = client.post("/api/dos/execute", json={"command": "ver", "current_dir": "C:\\"})
    assert res.status_code == 200
    assert "6.22" in res.json()["output"]

    # DIR
    res = client.post("/api/dos/execute", json={"command": "dir", "current_dir": "C:\\"})
    assert res.status_code == 200
    assert "AUTOEXEC.BAT" in res.json()["output"]

    # CD
    res = client.post("/api/dos/execute", json={"command": "cd WINDOWS", "current_dir": "C:\\"})
    assert res.status_code == 200
    assert res.json()["new_dir"] == "C:\\WINDOWS"

    # TYPE
    res = client.post("/api/dos/execute", json={"command": "type README.TXT", "current_dir": "C:\\"})
    assert res.status_code == 200
    assert "WELCOME TO PHANTASM-OS" in res.json()["output"]

    # MATRIX
    res = client.post("/api/dos/execute", json={"command": "matrix", "current_dir": "C:\\"})
    assert res.status_code == 200
    assert res.json()["trigger_glitch"] is True


def test_static_index(client):
    res = client.get("/")
    assert res.status_code == 200
    assert "Phantasm-OS" in res.text
