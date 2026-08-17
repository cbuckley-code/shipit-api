FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Container binds all interfaces; Container Apps ingress terminates TLS.
ENV FRANK_HOST=0.0.0.0 \
    FRANK_PORT=8720

EXPOSE 8720
CMD ["python", "server.py"]
