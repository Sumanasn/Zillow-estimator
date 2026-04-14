FROM python:3.11-slim

# Install curl for the Docker Healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend files
COPY . .

# Run tests, then start the server
# Using 'sh -c' allows us to chain the test execution and the server startup
CMD sh -c "python tests.py && uvicorn main:app --host 0.0.0.0 --port 8000"