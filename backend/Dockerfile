# Use the official Python image as the base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app/backend

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install any dependencies
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install  -r requirements.txt


# Copy the contents of the local backend folder to the container at /app/backend
COPY . .

# Expose the port that your Flask app will run on
EXPOSE 5000

# Command to run the application
# CMD ["python", "app.py"]
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "wsgib:app"]
