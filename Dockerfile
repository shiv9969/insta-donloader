# Use official Python image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy all files
COPY . .

# Set Python path to include the bot directory
ENV PYTHONPATH="${PYTHONPATH}:/app"

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the bot
CMD ["python", "bot/main.py"]
