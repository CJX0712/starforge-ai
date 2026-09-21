from tests.conftest import SAMPLE


def test_rag_ingest_and_answer(container):
    res = container.rag.ingest(SAMPLE)
    assert res["documents"] == 1
    assert res["chunks"] > 0
    out = container.rag.answer("StarForge 的核心能力有哪些")
    assert out["answer"]
    assert "sources" in out
    assert len(out["sources"]) >= 1
    assert out["sources"][0]["score"] > 0
