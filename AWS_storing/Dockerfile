# ---- Backend Dockerfile ----

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependency list and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all backend code
COPY . .

# Expose backend port
EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "applicaiton:app", "--host", "0.0.0.0", "--port", "8000"]
