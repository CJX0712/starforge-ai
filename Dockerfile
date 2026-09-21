# 容器化部署：默认 mock 后端，无网络/密钥即可运行
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt pytest
COPY . .
EXPOSE 8000
CMD ["python", "-m", "starforge", "serve", "--host", "0.0.0.0", "--port", "8000"]
