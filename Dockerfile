# Use an official Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy our ETL script into the container
COPY etl_script.py .

# Command to run when the container starts
CMD ["python", "etl_script.py"]