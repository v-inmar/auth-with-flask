# Grab the official python image
FROM python:3.12

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt
COPY requirements.txt requirements.txt

# Install OS dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc build-essential libssl-dev libffi-dev default-mysql-client && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt


# Copy the entire app directory and config files
COPY . .

# Copy and make entrypoint script executable
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expose port 5000
EXPOSE 5000

# Use entrypoint to handle migrations and start Gunicorn
ENTRYPOINT ["/app/entrypoint.sh"]
