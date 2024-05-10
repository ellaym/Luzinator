# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN pip install --upgrade pip

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Reinstall openai to fix the issue with the latest version
RUN pip uninstall -y openai
RUN pip install openai

# Make port 5500 available to the world outside this container
EXPOSE 5500

# Run the GPT service python script when the container launches
CMD ["python", "src/gpt_service.py"]
