# Build stage
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies (including g++ for fasttext compilation)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pybind11 setuptools wheel && \
    pip install --no-cache-dir --user -r requirements.txt


# Runtime stage
FROM python:3.11-slim

WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY . .

# Set PATH to include user site-packages
ENV PATH=/root/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    NLTK_DATA=/usr/local/share/nltk_data

# Download NLTK data at build time
RUN python -c "import nltk; nltk.download('wordnet', download_dir='/usr/local/share/nltk_data')" && \
    python -m nltk.downloader -d /usr/local/share/nltk_data cmudict || true

# Expose API port
EXPOSE 8000

# Health check: verify app can import modules
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from infrastructure.language_detector import detectLanguage; print('healthy')" || exit 1

# Default command - runs main.py
CMD ["python", "main.py"]
