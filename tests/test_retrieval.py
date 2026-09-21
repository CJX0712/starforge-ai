from starforge.modules.ingestion.loaders import FileIngestor

from tests.conftest import SAMPLE


def test_retrieve_returns_results(container):
    ing = FileIngestor()
    docs = ing.load(SAMPLE)
    chunks = ing.chunk(docs[0], size=120, overlap=20)
    container.retriever.index_chunks(chunks)
    res = container.retriever.retrieve("StarForge 是什么", top_k=2)
    assert len(res) >= 1
    assert "StarForge" in res[0].payload.get("text", "")
