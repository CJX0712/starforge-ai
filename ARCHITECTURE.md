# 系统架构 — StarForge-AI

**Author: 晨星**

---

## 1. 设计原则

1. **单一职责**：每个模块只做一件事，仅暴露一个抽象接口（ABC）。
2. **接口驱动 / 依赖倒置**：上层（RAG / Agent / API / CLI）只依赖接口，不 import 具体实现。
3. **依赖注入**：`Container` 是唯一装配点，按 `Settings` 决定具体实现，便于替换与测试。
4. **离线可验**：默认 Mock 后端确定性输出，保证无网络、无密钥也能跑通全链路、CI 全绿。

## 2. 模块依赖关系

```
                 ┌─────────────┐
   CLI / 调用 ──►│  core.container │◄── Settings(.env)
                 └──────┬──────┘
            ┌──────────┼──────────────────────┐
            ▼          ▼                       ▼
      modules.rag   modules.agent          api (FastAPI)
            │          │                       │
            └────┬─────┘                       │
                 ▼                             │
          modules.retrieval                   │
           ┌────────────┐                      │
           ▼            ▼                      │
   modules.embeddings  modules.vectorstore     │
                 └────────────┘                │
                                               │
        modules.llm  ◄─────────────────────────┘
        modules.ingestion ──► retrieval
```

## 3. 接口契约（关键 ABC）

### LLMProvider
```python
class LLMProvider(ABC):
    name: str
    def complete(self, prompt: str, **kwargs) -> str: ...
    def chat(self, messages: List[Message], **kwargs) -> str: ...
```
实现：`MockLLMProvider`（离线）/ `OpenAIProvider`（OpenAI 兼容）/ `OllamaProvider`（本地）。

### EmbeddingProvider
```python
class EmbeddingProvider(ABC):
    name: str
    dimension: int
    def embed(self, texts: List[str]) -> List[List[float]]: ...
```
实现：`MockEmbeddingProvider`（TF-hash，确定性）/ `SentenceTransformerProvider`（真实模型）。

### VectorStore
```python
@dataclass
class SearchResult:
    id: str; score: float; payload: Dict[str, Any]

class VectorStore(ABC):
    def add(self, id, vector, payload) -> None: ...
    def search(self, vector, top_k=3) -> List[SearchResult]: ...
```
实现：`NumpyVectorStore`（默认，零依赖）/ `FAISSVectorStore`（高性能，可选）。

### 数据流（摄入 → 问答）

```
摄入:  File/path ─► Ingestor.load ─► Document
                              ─► Ingestor.chunk ─► Chunk[]
                              ─► Embedding.embed ─► vector[]
                              ─► VectorStore.add (payload=text+metadata)

问答:  Question ─► Embedding.embed ─► vector
                    ─► VectorStore.search(top_k) ─► SearchResult[]
                    ─► 拼装提示(PROMPT) ─► LLM.complete ─► answer + sources

Agent: Question ─► LLM.chat(system+user)
       若 Action: 调用 tools(knowledge_search/calculator) ─► Observation ─► 再推理
       若 Final Answer: 返回答案
```

## 4. 可替换性验证

上层对具体实现零耦合：把 `VECTORSTORE_BACKEND` 从 `numpy` 改为 `faiss`，或把 `LLM_PROVIDER` 从 `mock` 改为 `openai`，调用方代码与接口不变，仅 `Container` 装配结果变化。测试 `test_integration.py::test_swap_backend_is_interface_driven` 即验证此点。

## 5. 测试分层

- **逐模块单测**：config / llm / embeddings / vectorstore / ingestion / retrieval / rag / agent / api
- **集成测试**：`tests/test_integration.py` 覆盖摄入→检索→生成→Agent 完整链路（mock 后端）
- 运行：`pytest -q`，默认全 mock，零外部依赖。
