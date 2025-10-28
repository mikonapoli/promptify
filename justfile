# Promptify - Just Commands

# List available commands
default:
    @just --list

# Install dependencies with uv
install:
    uv pip install -e ".[dev]"

# Run tests
test:
    uv run pytest tests/ -v

# Run tests with coverage
test-cov:
    uv run pytest tests/ -v --cov=. --cov-report=term-missing

# Run the app in development mode
dev:
    uv run uvicorn app:app --reload --port 8000

# Run the app in production mode
run:
    uv run uvicorn app:app --host 0.0.0.0 --port 8000

# Stop the app (finds and kills uvicorn process)
stop:
    @pkill -f "uvicorn app:app" || echo "No app running"

# Format code (if you add ruff later)
fmt:
    @echo "No formatter configured yet"

# Lint code (if you add ruff later)
lint:
    @echo "No linter configured yet"

# Clean pycache and build artifacts
clean:
    find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
    find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
    find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
    rm -rf dist/ build/ .coverage 2>/dev/null || true

# Create .env file from template if it doesn't exist
setup-env:
    @if [ ! -f .env ]; then \
        echo "GEMINI_API_KEY=your_api_key_here" > .env; \
        echo "# GEMINI_MODEL_NAME=gemini-2.0-flash-exp" >> .env; \
        echo "Created .env file - please add your GEMINI_API_KEY"; \
    else \
        echo ".env file already exists"; \
    fi

# Full setup: create venv, install deps, setup env
setup:
    uv venv
    @just install
    @just setup-env
    @echo ""
    @echo "Setup complete! Next steps:"
    @echo "1. Activate venv: source .venv/bin/activate"
    @echo "2. Edit .env and add your GEMINI_API_KEY"
    @echo "3. Run the app: just dev"

# Check if dependencies are installed
check:
    uv pip list

# Docker commands
# Build Docker image
docker-build:
    docker build -t promptify .

# Run with Docker Compose
docker-up:
    docker-compose up

# Run with Docker Compose (detached)
docker-up-d:
    docker-compose up -d

# Stop Docker Compose
docker-down:
    docker-compose down

# Rebuild and run with Docker Compose
docker-rebuild:
    docker-compose up --build

# View Docker logs
docker-logs:
    docker-compose logs -f
