"""可观测性 — 单一职责：结构化日志 + 可选 Prometheus 指标。

默认仅启用结构化日志；开启 PROMETHEUS_ENABLED 后惰性加载 prometheus-client，
调用方对 None 返回值做安全降级，避免强依赖。
Author: 晨星
"""
from __future__ import annotations

import logging

from starforge.core.config import get_settings

_CONFIGURED = False


def get_logger(name: str = "starforge") -> logging.Logger:
    global _CONFIGURED
    if not _CONFIGURED:
        level = getattr(logging, get_settings().log_level.upper(), logging.INFO)
        logging.basicConfig(
            level=level,
            format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        _CONFIGURED = True
    return logging.getLogger(name)


def get_metrics():
    """可选指标；未启用或依赖缺失时返回 None。"""
    if not get_settings().prometheus_enabled:
        return None
    try:
        from prometheus_client import Counter, Histogram  # 惰性导入

        return {
            "requests": Counter("starforge_requests_total", "总请求数"),
            "latency": Histogram("starforge_request_latency_seconds", "请求延迟"),
        }
    except Exception:  # pragma: no cover - 可选依赖
        return None
