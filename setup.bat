@echo off
REM 干净环境一键复现（Windows）：创建 venv -> 安装核心依赖 -> 安装 pytest
set PY=python
%PY% -m venv .venv
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m pip install pytest
echo Install done. Run: .venv\Scripts\python.exe -m starforge serve
