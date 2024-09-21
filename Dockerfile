# Use the official Python image from Docker Hub
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the entire application code into the container
COPY . .

# Expose the port your app runs on (Django's default port)
EXPOSE 8000

# Set environment variables to improve performance
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Run migrations and start the Django development server
CMD ["sh", "-c", "python manage.py makemigrations accounts && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
