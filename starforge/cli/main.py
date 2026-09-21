"""命令行入口 — serve / ingest / query / chat。

通过 Container 装配各模块，CLI 仅做参数解析与结果展示，不承载业务逻辑。
Author: 晨星
"""
from __future__ import annotations

import uvicorn
import typer
from starforge.core.config import get_settings
from starforge.core.container import Container
from starforge.core.observability import get_logger
from starforge.modules.llm.base import Message

_LOG = get_logger("starforge.cli")
app = typer.Typer(help="StarForge-AI 命令行")


def _container() -> Container:
    return Container.from_settings(get_settings())


@app.command()
def serve(host: str = None, port: int = None):
    """启动 REST 服务（python -m starforge serve）。"""
    s = get_settings()
    uvicorn.run(
        "starforge.api.app:app",
        host=host or s.api_host,
        port=port or s.api_port,
        log_level="info",
    )


@app.command()
def ingest(path: str = typer.Option(None, "--path", "-p"), text: str = typer.Option(None, "--text", "-t")):
    """摄入文档或文本到知识库。"""
    c = _container()
    source = path or text
    if not source:
        typer.echo("请提供 --path 文件路径或 --text 文本")
        raise typer.Exit(code=1)
    res = c.rag.ingest(source)
    typer.echo(f"摄入完成: 文档 {res['documents']} 个, 切片 {res['chunks']} 个")


@app.command()
def query(question: str, top_k: int = None):
    """基于知识库问答。"""
    c = _container()
    res = c.rag.answer(question, top_k=top_k)
    typer.echo("回答: " + res["answer"])
    for i, s in enumerate(res["sources"], 1):
        typer.echo(f"  来源{i} (score={s['score']:.3f}): {s['text'][:120]}")


@app.command()
def chat(message: str):
    """与 LLM 单次对话。"""
    c = _container()
    reply = c.llm.chat([Message(role="user", content=message)])
    typer.echo(reply)


def main():
    app()


if __name__ == "__main__":
    main()
