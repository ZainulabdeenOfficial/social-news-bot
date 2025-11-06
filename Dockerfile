# syntax=docker/dockerfile:1
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Default command runs the Streamlit dashboard
EXPOSE 8501
CMD ["streamlit", "run", "web_dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]


