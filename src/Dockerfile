FROM python:3.11-slim
 
WORKDIR /app

ARG ENVIRONMENT
ENV ENVIRONMENT=${ENVIRONMENT}

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ${ENVIRONMENT}-variables.py ./variables.py

COPY main.py .
 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]