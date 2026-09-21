from starforge.modules.vectorstore.numpy_store import NumpyVectorStore


def test_numpy_search_top1():
    s = NumpyVectorStore()
    base = [1.0, 0.0, 0.0, 0.0]
    other = [0.0, 1.0, 0.0, 0.0]
    s.add("a", base, {"text": "A"})
    s.add("b", other, {"text": "B"})
    res = s.search(base, top_k=1)
    assert res[0].id == "a"
    assert res[0].score > 0.99


def test_numpy_empty():
    s = NumpyVectorStore()
    assert s.search([1.0, 0.0], top_k=3) == []


def test_numpy_topk_limit():
    s = NumpyVectorStore()
    for i in range(5):
        vec = [0.0] * 5
        vec[i] = 1.0
        s.add(str(i), vec, {})
    res = s.search([1.0, 0.0, 0.0, 0.0, 0.0], top_k=2)
    assert len(res) == 2
    assert res[0].id == "0"
