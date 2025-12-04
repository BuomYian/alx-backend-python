# Use official Python base image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Prevent Python from writing .pyc files and buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies (include MySQL client headers for mysqlclient)
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files to container
COPY . /app/

# Copy and make entrypoint executable
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expose the Django port
EXPOSE 8000

# Start Django development server with entrypoint (handles migrations)
ENTRYPOINT ["/app/entrypoint.sh"]
