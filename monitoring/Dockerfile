FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY consumer.py .

# Create non-root user for security
RUN useradd -m -u 1000 consumer && \
    chown -R consumer:consumer /app

# Switch to non-root user
USER consumer

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the consumer
CMD ["python", "consumer.py"]
