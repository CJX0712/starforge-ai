from starforge.modules.ingestion.loaders import FileIngestor


def test_load_and_chunk(tmp_path):
    f = tmp_path / "s.txt"
    f.write_text("人工智能是计算机科学的一个分支。" * 50, encoding="utf-8")
    ing = FileIngestor()
    docs = ing.load(str(f))
    assert len(docs) == 1
    chunks = ing.chunk(docs[0], size=100, overlap=20)
    assert len(chunks) >= 2
    # 切片含原文档元数据
    assert chunks[0].metadata["doc_id"] == docs[0].id


def test_inline_text():
    ing = FileIngestor()
    docs = ing.load("StarForge 是模块化 AI 平台")
    assert docs[0].metadata["source"] == "inline"
