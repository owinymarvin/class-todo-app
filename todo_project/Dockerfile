# Base image for Python environment
FROM python:3.9

# Create a working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy your Django project code
COPY . .

# Expose the Django application port (usually 8000)
EXPOSE 8000

# Run the Django development server (modify as needed for production)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
