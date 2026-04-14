Zillow price estimate
# Zillow price estimator

A professional-grade, containerized AI agent built with **Python**, **FastAPI**, and **Streamlit**. This agent autonomously navigates Zillow to extract real-time property values (Sales & Rentals) while bypassing modern anti-bot security.

## 🌟 Key Features

* **Autonomous Decision Making**: The agent identifies property types (Apartment vs. House) and selects the correct valuation metric (Monthly Rent vs. Listing Price).
* **Stateful Memory (Caching)**: Uses a local TTL (Time-To-Live) cache to store results, reducing API costs and providing instant responses for previously searched addresses.
* **Anti-Bot Bypass**: Integrated with **ZenRows** (JS Rendering & Premium Proxies) to bypass modern detection systems like DataDome.
* **Production-Ready Architecture**: 
    * **Backend**: FastAPI with asynchronous endpoints.
    * **Frontend**: Streamlit dashboard for real-time interaction.
    * **DevOps**: Fully containerized using Docker Compose with built-in health checks.
    * **Validation**: Automated unit tests run on every container build.

## 🏗️ Architecture

The system follows a **Client-Server** model distributed across an internal Docker network:

1.  **Frontend (Streamlit)**: Dispatches address queries to the backend.
2.  **Backend (FastAPI)**: Coordinates the Agent's "Brain."
3.  **Agent (The Brain)**: Checks `memory.json` before deploying network resources.
4.  **Utilities (The Tools)**: Handles regex extraction and data normalization.

## 🚀 Getting Started

### Prerequisites
* [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* A [ZenRows API Key](https://www.zenrows.com/)

### Setup & Installation

1.  **Clone the Repository**:
    ```bash
    git clone [https://github.com/your-username/Zillow_es.git](https://github.com/your-username/Zillow_es.git)
    cd Zillow_es
    ```

2.  **Configure Environment Variables**:
    Create a `.env` file in the root directory:
    ```text
    ZENROWS_API_KEY=your_api_key_here
    ```

3.  **Launch the Agent**:
    ```bash
    docker-compose up --build
    ```

4.  **Access the Dashboard**:
    Open your browser to [http://localhost:8501](http://localhost:8501)

## 🧪 Testing

Unit tests are automatically executed during the Docker build process. To run them manually:
```bash
cd backend
python -m unittest tests.py

## 📚 Sources & Acknowledgments
* [Gemini](https://gemini.google.com) - Architectural guidance and code optimization.
* [Medium Article](https://medium.com/@sohail_saifii/web-scraping-in-2025-bypassing-modern-bot-detection-fcab286b117d) - Insights on modern bot detection.
