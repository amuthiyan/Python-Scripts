# Use an official Python runtime as a parent image
FROM python:3.6.2-slim

# Set the working directory to /webapi
WORKDIR /pipeline

# Copy the current directory contents into the container at /webapi
ADD . /pipeline

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run run.py when the container launches
CMD ["python", "run.py"]