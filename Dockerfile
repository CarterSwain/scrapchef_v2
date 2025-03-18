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

# Run migrations & collect static at container startup
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn --bind 0.0.0.0:8080 config.wsgi:application"]
