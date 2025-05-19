# Dockerfile

# Use the official Python 3.11 image as base
FROM python:3.11


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# Set working directory inside the container
WORKDIR /app

# Copy requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entrypoint script and make it executable
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Copy all other application code into the container
COPY . .

# Define the default command to run when the container starts
CMD ["./entrypoint.sh"]
