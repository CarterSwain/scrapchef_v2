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

# Set environment variables inside Docker
ARG SECRET_KEY
ARG DATABASE_URL
ARG DEBUG
ARG OPENAI_API_KEY
ARG GOOGLE_CLIENT_ID
ARG GOOGLE_CLIENT_SECRET

ENV SECRET_KEY=$SECRET_KEY
ENV DATABASE_URL=$DATABASE_URL
ENV DEBUG=$DEBUG
ENV OPENAI_API_KEY=$OPENAI_API_KEY
ENV GOOGLE_CLIENT_ID=$GOOGLE_CLIENT_ID
ENV GOOGLE_CLIENT_SECRET=$GOOGLE_CLIENT_SECRET

# Now `SECRET_KEY` is available when running collectstatic
RUN python manage.py collectstatic --noinput

# Expose port 8080 for Cloud Run
EXPOSE 8080

# Start the Django application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "config.wsgi:application"]
