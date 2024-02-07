# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/src/app

COPY ./main.py /usr/src/app
COPY requirements.txt /usr/src/app

# Install any needed packages specified in requirements.txt
RUN apt update && apt upgrade -y
RUN apt install -y gcc python3-dev

RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
# ENV NAME World

# Run app.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
