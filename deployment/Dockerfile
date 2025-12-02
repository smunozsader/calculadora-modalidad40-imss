# Use Python 3.12
FROM python:3.12-slim

# Set working directory
WORKDIR /app

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

# Start gunicorn with the main entry point
CMD ["gunicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "1"]