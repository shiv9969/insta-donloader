# Use an official Python runtime as base
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the bot code into the container
COPY . .

# Command to run the bot
CMD ["python", "bot/main.py"]
