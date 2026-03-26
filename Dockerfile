FROM python:3.9-slim

# Create working folder and install dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the service package into the working directory 
COPY service/ ./service/

# Create a non-root user called theia, change the ownership of the /app folder recursively to theia, and switch to the theia user.
RUN useradd --uid 1000 theia && chown -R theia /app
USER theia

# Expose the port 8080 and run the service
EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--log-level", "info", "service:app"]