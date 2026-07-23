# Use the official Python runtime
FROM python:3.13-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Expose the FastAPI port
EXPOSE 5005

# Start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5005"]
