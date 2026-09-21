# 使用指南 — StarForge-AI

**Author: 晨星**

> 以下示例默认已安装依赖（见 DEPLOYMENT.md）。命令中的 `python` 指虚拟环境解释器
> （Windows: `.venv/Scripts/python`，Linux/macOS: `.venv/bin/python`）。

---

## 1. 命令行（CLI）

### 启动 REST 服务
```bash
python -m starforge serve
# 自定义端口
python -m starforge serve --port 8080
```

### 摄入知识
```bash
# 从文件
python -m starforge ingest --path samples/sample.txt
# 从纯文本
python -m starforge ingest --text "StarForge 是模块化 AI 平台，支持 RAG 与 Agent。"
# 输出: 摄入完成: 文档 1 个, 切片 N 个
```

### 知识库问答
```bash
python -m starforge query "StarForge 的核心能力有哪些"
# 输出: 回答: ...  来源1 (score=0.xxx): ...
```

### 对话
```bash
python -m starforge chat "用一句话介绍 StarForge"
```

## 2. REST API

服务启动后（默认 `http://localhost:8000`）：

### 健康检查
```bash
GET /health
```
```json
{ "status": "ok", "version": "1.0.0", "author": "晨星",
  "components": { "llm": "mock", "embedding": "mock", "vectorstore": "NumpyVectorStore" } }
```

### 摄入文档
```bash
POST /ingest
Content-Type: application/json
{ "text": "StarForge 是模块化 AI 平台。" }
# 或 { "path": "samples/sample.txt" }
```

### 知识库问答
```bash
POST /query
Content-Type: application/json
{ "question": "StarForge 支持什么", "top_k": 3 }
```
```json
{ "answer": "...", "sources": [ { "id": "...", "score": 0.91, "text": "..." } ] }
```

### 对话
```bash
POST /chat
Content-Type: application/json
{ "messages": [ { "role": "user", "content": "你好" } ] }
```

### Python 客户端示例
```python
import httpx
base = "http://localhost:8000"
httpx.post(f"{base}/ingest", json={"text": "StarForge 是模块化 AI 平台。"})
r = httpx.post(f"{base}/query", json={"question": "StarForge 是什么"})
print(r.json()["answer"])
```

## 3. 作为库调用（接口驱动）

```python
from starforge.core.config import Settings
from starforge.core.container import Container

container = Container(Settings(llm_provider="mock", embedding_provider="mock"))
container.rag.ingest("samples/sample.txt")
out = container.rag.answer("StarForge 的核心能力有哪些")
print(out["answer"], out["sources"])
```

## 4. 从 Mock 切到真实后端

无需改代码，仅改环境变量（详见 DEPLOYMENT.md 第 5 节）：

```bash
export LLM_PROVIDER=openai
export OPENAI_API_KEY=sk-xxx
export EMBEDDING_PROVIDER=sentence-transformers
export VECTORSTORE_BACKEND=faiss
pip install -r requirements-optional.txt
python -m starforge serve
```

调用方式与返回结构完全一致 —— 这正是「接口驱动 + 依赖注入」带来的可替换性。
