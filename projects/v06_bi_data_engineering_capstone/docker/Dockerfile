FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY data ./data
COPY python ./python
COPY docs ./docs
COPY sql ./sql
COPY reports ./reports
CMD ["python", "python/build_marts.py"]
