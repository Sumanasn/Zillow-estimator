FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir streamlit requests

COPY . .

# Streamlit looks for the backend at the docker service name "backend"
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]