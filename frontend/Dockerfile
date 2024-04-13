FROM python:3.10

# Set the working directory in the container
WORKDIR /app/frontend

# Copy the current directory contents into the container at /app
# COPY . /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install  -r requirements.txt

COPY . .
# Make port 8000 available to the world outside this container
EXPOSE 8000

# # Define environment variable for Flask
# ENV FLASK_APP=app.py
# ENV FLASK_RUN_HOST=0.0.0.0
# ENV FLASK_RUN_PORT=8000

# Run app.py when the container launches
# CMD ["flask", "run"]
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "wsgi:app"]
