# Use an official Ubuntu base image
FROM ubuntu:latest

# Set the working directory in the container
WORKDIR /usr/src/app

# Install Python and pip
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container at /usr/src/app
COPY requirements.txt ./

# Install the Python libraries from the requirements file
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of your application's code
COPY . .

# Command to run the application
CMD ["python3", "your-application.py"]
