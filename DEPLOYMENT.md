# 部署指南 — StarForge-AI

**Author: 晨星**

---

## 1. 干净环境一键复现（推荐）

本仓库提供两种等价的一键脚本，**在全新机器上无需任何预装即可跑通离线链路**：

```bash
# Linux / macOS
bash setup.sh

# Windows (PowerShell / CMD)
setup.bat
```

脚本动作：创建 `.venv` → 升级 pip → 安装 `requirements.txt` 核心依赖 → 安装 `pytest`。

> 复现保证：默认 `LLM_PROVIDER=mock` + `EMBEDDING_PROVIDER=mock` + `VECTORSTORE_BACKEND=numpy`，**不下载任何模型权重、不访问任何网络**。

## 2. 手动安装

```bash
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt   # Windows
.venv/bin/python -m pip install -r requirements.txt       # Linux/macOS
.venv/Scripts/python -m pip install pytest
```

## 3. 版本锁定

| 文件 | 作用 |
|------|------|
| `requirements.txt` | 核心依赖（宽松版本区间，便于解析） |
| `requirements.lock` | `pip freeze` 全量精确版本，生产锁定首选 |
| `pyproject.toml` | 项目元数据 + 可选依赖分组（optional/dev） |
| `requirements-optional.txt` | 真实模型 / FAISS / PDF / 指标等可选依赖 |

生产部署建议基于 `requirements.lock` 安装以获得完全可复现环境。

## 4. 容器化部署

```bash
docker build -t starforge-ai .
docker run -p 8000:8000 starforge-ai
# 健康检查
curl http://localhost:8000/health
```

默认镜像即 mock 后端，可直接对外提供离线 RAG 服务。启用真实后端时在 `docker run -e` 注入对应环境变量（见第 5 节），并先 `pip install -r requirements-optional.txt`。

## 5. 环境变量（全部可选，默认值即离线可跑）

| 变量 | 默认 | 说明 |
|------|------|------|
| `LLM_PROVIDER` | `mock` | `mock` / `openai` / `ollama` |
| `OPENAI_API_KEY` | 空 | OpenAI 兼容后端密钥 |
| `OPENAI_BASE_URL` | `https://api.openai.com/v1` | 兼容端点（vLLM / 第三方） |
| `OPENAI_MODEL` | `gpt-4o-mini` | 模型名 |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama 地址 |
| `OLLAMA_MODEL` | `llama3` | Ollama 模型 |
| `EMBEDDING_PROVIDER` | `mock` | `mock` / `sentence-transformers` |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | 真实向量模型名 |
| `EMBEDDING_DIM` | `384` | mock 向量维度 |
| `VECTORSTORE_BACKEND` | `numpy` | `numpy` / `faiss` |
| `CHUNK_SIZE` / `CHUNK_OVERLAP` | `500` / `50` | 切分参数 |
| `TOP_K` | `3` | 检索条数 |
| `API_HOST` / `API_PORT` | `0.0.0.0` / `8000` | 服务监听 |
| `LOG_LEVEL` | `INFO` | 日志级别 |
| `PROMETHEUS_ENABLED` | `false` | 开启 Prometheus 指标 |

> 将 `.env.example` 复制为 `.env` 并填写即可：`cp .env.example .env`。

## 6. 启用真实能力的依赖

```bash
pip install -r requirements-optional.txt
```

- `sentence-transformers`：真实向量模型（首次运行自动下载权重）
- `faiss-cpu`：高性能向量检索（CPU 即可）
- `pypdf`：PDF 文档摄入
- `prometheus-client`：开启 `PROMETHEUS_ENABLED=true` 时暴露指标

## 7. 健康检查与冒烟

```bash
curl http://localhost:8000/health
# => {"status":"ok","version":"1.0.0","author":"晨星","components":{...}}

curl -X POST http://localhost:8000/ingest -H "Content-Type: application/json" \
  -d "{\"text\":\"StarForge 是模块化 AI 平台。\"}"
curl -X POST http://localhost:8000/query -H "Content-Type: application/json" \
  -d "{\"question\":\"StarForge 是什么\"}"
```
