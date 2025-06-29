# Use official Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy everything
COPY . /app
 
# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --index-url https://download.pytorch.org/whl/cpu

# Expose port
EXPOSE 8000

# Start the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]