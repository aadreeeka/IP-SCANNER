FROM python:3.11-slim

# Install nmap
RUN apt-get update && apt-get install -y nmap && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy app files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Start with Gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]
