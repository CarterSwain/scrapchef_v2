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

# Load environment variables from a .env file
COPY .env /app/.env

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port 8080 for Cloud Run
EXPOSE 8080

# Start the Django application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "config.wsgi:application"]
