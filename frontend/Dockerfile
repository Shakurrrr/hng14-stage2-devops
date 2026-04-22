FROM node:18-alpine

# Set working directory
WORKDIR /app

# Install dependencies in a single RUN
COPY ./frontend/package*.json ./
RUN npm install --production

# Copy source files
COPY ./frontend /app

# Expose port
EXPOSE 3000

# Start frontend
CMD ["npm", "start"]