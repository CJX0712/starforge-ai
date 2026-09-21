from fastapi.testclient import TestClient

from starforge.api.app import app


def test_health():
    with TestClient(app) as client:
        r = client.get("/health")
        assert r.status_code == 200
        body = r.json()
        assert body["status"] == "ok"
        assert body["author"] == "晨星"
        assert body["components"]["vectorstore"] == "NumpyVectorStore"


def test_ingest_then_query():
    with TestClient(app) as client:
        r = client.post(
            "/ingest",
            json={"text": "StarForge 是模块化 AI 平台。它支持 RAG 与 Agent 编排。"},
        )
        assert r.status_code == 200
        assert r.json()["chunks"] > 0
        q = client.post("/query", json={"question": "StarForge 支持什么"})
        assert q.status_code == 200
        assert q.json()["answer"]
        assert len(q.json()["sources"]) >= 1


def test_chat():
    with TestClient(app) as client:
        r = client.post(
            "/chat",
            json={"messages": [{"role": "user", "content": "你好"}]},
        )
        assert r.status_code == 200
        assert r.json()["reply"]
