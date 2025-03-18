# Use official Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy required files
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
COPY documentation_loader.py .

# Expose a port (if running as an API later)
EXPOSE 8080

# Run the script
CMD ["python", "app.py"]

