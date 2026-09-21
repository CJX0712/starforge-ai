# StarForge-AI 常用命令
# Windows(Git Bash) 下自动使用 .venv/Scripts/python；其余平台使用 .venv/bin/python
PY := python
VENV := .venv
ifeq ($(OS),Windows_NT)
  PY := $(VENV)/Scripts/python
endif

install:
	$(PY) -m pip install -r requirements.txt
	$(PY) -m pip install pytest

test:
	$(PY) -m pytest -q

serve:
	$(PY) -m starforge serve

cli:
	$(PY) -m starforge --help

.PHONY: install test serve cli
