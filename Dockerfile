# Use the official Python base image 
FROM python:3.10-bullseye as builder
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

RUN python -m venv /app/venv
# Enable venv
ENV PATH="/app/venv/bin:$PATH"

# Copy the requirements file
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.10-slim-buster
WORKDIR /app
COPY --from=builder /app/venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# Copy the rest of the application code
COPY . .

# Specify the command to run your application
CMD ["python", "/app/bot.py"]
