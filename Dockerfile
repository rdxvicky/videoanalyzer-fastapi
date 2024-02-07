# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable to run the server on 0.0.0.0
ENV UVICORN_HOST=0.0.0.0

# Run the application
ENTRYPOINT ["uvicorn", "main:app", "--host", "${UVICORN_HOST}", "--port", "8000", "--reload"]
