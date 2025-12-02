# Use Python 3.12
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install locales for Spanish support
RUN apt-get update && \
    apt-get install -y locales && \
    sed -i -e 's/# es_ES.UTF-8 UTF-8/es_ES.UTF-8 UTF-8/' /etc/locale.gen && \
    sed -i -e 's/# es_MX.UTF-8 UTF-8/es_MX.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# Set environment variables
ENV PYTHONPATH=/app:/app/webapp:/app/calculadoras-python
ENV PORT=8080

# Expose port
EXPOSE 8080

# Start gunicorn with the main entry point (root level)
CMD ["gunicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "1"]