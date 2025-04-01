# Use an official Python runtime as a base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy application files
COPY . /app

# Start the consumer first, then the API
CMD ["sh", "-c", "python queue.py & uvicorn api:app --host 0.0.0.0 --port 5007"]
