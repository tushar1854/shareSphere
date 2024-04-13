# Use the official Nginx image as the base image
FROM nginx:latest

# Copy your custom configuration file to the Nginx configuration directory
COPY ./nginx.conf /etc/nginx/nginx.conf:ro

# Expose the port that Nginx will run on
EXPOSE 80

# Command to start Nginx
CMD ["nginx", "-g", "daemon off;"]
