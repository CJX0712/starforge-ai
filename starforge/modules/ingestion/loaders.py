"""文档加载与切分 — 复用 pypdf(可选) 加载 PDF，其余按纯文本处理。

支持单文件 / 目录批量 / 纯文本直传；按字符定长重叠切分，利于后续检索粒度控制。
Author: 晨星
"""
from __future__ import annotations

import hashlib
import os
from typing import List

from starforge.core.observability import get_logger
from starforge.modules.ingestion.base import Chunk, Document, Ingestor

_LOG = get_logger("starforge.ingestion")


class FileIngestor(Ingestor):
    def load(self, source: str) -> List[Document]:
        if os.path.isfile(source):
            ext = os.path.splitext(source)[1].lower()
            if ext == ".pdf":
                text = self._load_pdf(source)
            else:
                with open(source, "r", encoding="utf-8", errors="ignore") as f:
                    text = f.read()
            doc_id = hashlib.md5(source.encode("utf-8")).hexdigest()[:12]
            return [
                Document(
                    id=doc_id, text=text, metadata={"source": source, "type": ext or "text"}
                )
            ]
        if os.path.isdir(source):
            docs: List[Document] = []
            for name in sorted(os.listdir(source)):
                docs.extend(self.load(os.path.join(source, name)))
            return docs
        # 视为纯文本
        doc_id = hashlib.md5(source.encode("utf-8")).hexdigest()[:12]
        return [Document(id=doc_id, text=source, metadata={"source": "inline", "type": "text"})]

    def _load_pdf(self, path: str) -> str:
        try:
            from pypdf import PdfReader  # 惰性导入
        except ImportError as e:  # pragma: no cover - 可选依赖
            raise RuntimeError(
                "未安装 pypdf，请执行: pip install -r requirements-optional.txt"
            ) from e
        reader = PdfReader(path)
        return "\n".join((p.extract_text() or "") for p in reader.pages)

    def chunk(self, doc: Document, size: int = 500, overlap: int = 50) -> List[Chunk]:
        text = doc.text
        if not text.strip():
            return []
        step = max(1, size - overlap)
        chunks: List[Chunk] = []
        start = 0
        idx = 0
        while start < len(text):
            piece = text[start : start + size]
            if piece.strip():
                cid = f"{doc.id}-{idx}"
                chunks.append(
                    Chunk(
                        id=cid,
                        text=piece,
                        metadata={**doc.metadata, "doc_id": doc.id, "index": idx},
                    )
                )
                idx += 1
            start += step
        _LOG.info("文档 %s 切分为 %d 个切片", doc.id, len(chunks))
        return chunks
