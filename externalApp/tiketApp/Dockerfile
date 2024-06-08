# Dockerfile for the Tiket API

# Use the official Node.js image as base
FROM node:14

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package*.json /app

# Install dependencies
RUN npm install

# Copy the application code to the working directory
COPY app.js /app

# Expose the port the app runs on
EXPOSE 3000

# Command to run the app
CMD ["node", "app.js"]