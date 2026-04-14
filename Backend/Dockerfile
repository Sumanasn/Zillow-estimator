FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend files
COPY . .

# Run tests, then start the server
CMD python tests.py && uvicorn main:app --host 0.0.0.0 --port 8000