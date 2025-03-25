# Use official Python image
FROM python:3.11

# Set environment variables (to prevent interactive prompts)
ENV PYTHONUNBUFFERED 1

# Set working directory in container
WORKDIR /app

# Copy project files into container
COPY . /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080 for Cloud Run
EXPOSE 8080

# Collect static files and run migrations on container startup
# Cloud Run expects the app to start quickly, so we use gunicorn as entrypoint

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "config.wsgi:application"]

