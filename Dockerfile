# Dockerfile for Promptify
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install uv for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files
COPY pyproject.toml ./
COPY requirements.txt ./

# Install dependencies using uv
RUN uv pip install --system -r requirements.txt

# Copy application code
COPY app.py ./
COPY assets ./assets

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
