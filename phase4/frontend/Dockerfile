# Frontend Dockerfile - Next.js Application
# Use Node.js to run Next.js production server (simple and reliable approach)
FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install --production=false

# Copy source code
COPY . .

# Build the Next.js application
RUN npm run build

# Remove dev dependencies to reduce image size
RUN npm prune --production

# Expose port 3000
EXPOSE 3000

# Set environment variables
ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV=production

# Create a wrapper script that accepts connections on all interfaces
RUN echo '#!/bin/sh\nnode server.js' > /app/start.sh && chmod +x /app/start.sh

# Start the application with proper hostname binding
CMD ["node", "/app/node_modules/.bin/next", "start", "-H", "0.0.0.0", "-p", "3000"]
