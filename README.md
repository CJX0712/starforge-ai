# StarForge-AI

> 模块化、单一职责的端到端 AI 应用平台 —— 复用业界领先开源成果，干净环境一键复现，离线即可跑通完整链路。
> **Author: 晨星**

---

## 一句话定位

StarForge-AI 不是从零自研的模型，而是一套**把领先开源 AI 能力编排成可运行系统**的工程骨架：文档摄入 → 向量化 → 向量检索 → RAG 生成 → 可选工具编排 Agent，统一通过 REST / CLI 暴露。每个模块只暴露一个抽象接口（ABC），经依赖注入容器解耦，可独立替换、独立验证、组合成完整链路。

## 核心特性

- **单一职责 + 接口驱动**：`LLMProvider` / `EmbeddingProvider` / `VectorStore` 等抽象接口，上层只依赖接口，不依赖具体实现。
- **默认离线可验**：内置确定性 Mock 后端（LLM + 向量化），**零网络、零密钥**即可跑通端到端，保证干净环境复现与 CI 全绿。
- **三后端可切**：LLM 支持 `mock` / `OpenAI 兼容` / `Ollama`；向量化支持 `mock` / `sentence-transformers`；向量库支持 `numpy` / `faiss`。全部通过环境变量切换，不改代码。
- **版本锁定可复现**：`requirements.lock`（pip freeze 全量）+ `requirements.txt` + `pyproject.toml` + `setup.sh`/`Makefile`，一键安装。
- **完整文档**：架构、部署、使用三份指南齐备。

## 模块划分

| 模块 | 职责 | 核心接口 |
|------|------|----------|
| `core.config` | 配置加载 | `Settings` |
| `core.observability` | 日志 + 可选指标 | `get_logger` / `get_metrics` |
| `core.container` | 依赖注入装配 | `Container` |
| `modules.llm` | 文本生成 | `LLMProvider.complete/chat` |
| `modules.embeddings` | 向量化 | `EmbeddingProvider.embed` |
| `modules.vectorstore` | 向量存取检索 | `VectorStore.add/search` |
| `modules.ingestion` | 文档加载切分 | `Ingestor.load/chunk` |
| `modules.retrieval` | 检索召回 | `Retriever.retrieve` |
| `modules.rag` | RAG 生成管线 | `RAGPipeline.ingest/answer` |
| `modules.agent` | 工具编排 | `Agent.run` |
| `api` | REST 网关 | `/health /ingest /query /chat` |
| `cli` | 命令行 | `serve / ingest / query / chat` |

## 快速开始

```bash
# 1. 一键安装（创建 venv + 安装核心依赖）
bash setup.sh            # Windows: setup.bat

# 2. 跑测试（离线 mock，全绿）
.venv/Scripts/python -m pytest -q     # Linux/macOS: .venv/bin/python

# 3. 启动服务（默认 mock 后端）
.venv/Scripts/python -m starforge serve

# 4. 摄入 + 问答
.venv/Scripts/python -m starforge ingest --path samples/sample.txt
.venv/Scripts/python -m starforge query "StarForge 的核心能力有哪些"
```

打开 `http://localhost:8000/health` 查看健康状态与组件信息。

## 切换真实后端

```bash
# 使用 OpenAI 兼容接口（vLLM / 第三方均可）
export LLM_PROVIDER=openai
export OPENAI_API_KEY=sk-xxx
export OPENAI_BASE_URL=https://api.openai.com/v1
export OPENAI_MODEL=gpt-4o-mini

# 使用本地 Ollama
export LLM_PROVIDER=ollama
export OLLAMA_BASE_URL=http://localhost:11434
export OLLAMA_MODEL=llama3

# 使用真实向量模型 + 高性能向量库
export EMBEDDING_PROVIDER=sentence-transformers
export VECTORSTORE_BACKEND=faiss
pip install -r requirements-optional.txt
```

## 文档导航

- [ARCHITECTURE.md](./ARCHITECTURE.md) — 系统架构、接口契约、数据流
- [DEPLOYMENT.md](./DEPLOYMENT.md) — 干净环境 / 容器 / 环境变量
- [USAGE.md](./USAGE.md) — CLI 与 API 使用示例

## 许可

本项目由「晨星」构建并署名，用于学习与生产集成。
