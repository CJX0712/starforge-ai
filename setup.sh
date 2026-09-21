#!/usr/bin/env bash
# 干净环境一键复现：创建 venv -> 安装核心依赖 -> 安装 pytest
# 用法: bash setup.sh
set -euo pipefail
PY="${PYTHON:-python3}"
ROOT="$(cd "$(dirname "$0")" && pwd)"
"$PY" -m venv "$ROOT/.venv"
if [ -f "$ROOT/.venv/Scripts/python.exe" ]; then
  PY="$ROOT/.venv/Scripts/python.exe"
else
  PY="$ROOT/.venv/bin/python"
fi
"$PY" -m pip install --upgrade pip
"$PY" -m pip install -r "$ROOT/requirements.txt"
"$PY" -m pip install pytest
echo "✅ 安装完成。运行示例: $PY -m starforge serve"
