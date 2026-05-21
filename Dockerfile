# Dockerfile for Django News App
# Uses Python 3.13 slim image for a smaller, faster build

FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for Pillow and other packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the default Django development port
EXPOSE 8000

# Run database migrations and start the development server
# NOTE: Replace the placeholder values in settings.py before running:
#   SECRET_KEY, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
CMD ["sh", "-c", "\
    python manage.py migrate && \
    echo 'Starting Django development server on port 8000...' && \
    python manage.py runserver 0.0.0.0:8000 \
"]
