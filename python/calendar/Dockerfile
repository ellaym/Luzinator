# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5544 available to the world outside this container
EXPOSE 5544

# Run the calendar service python script when the container launches
CMD ["python", "src/calendar_service.py"]
