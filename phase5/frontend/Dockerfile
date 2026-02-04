# Use Node 20
FROM node:20

WORKDIR /app

# Copy only package files first (cache dependencies)
COPY package*.json ./

# Install dependencies
RUN npm install --production=false

# Copy rest of the code
COPY . .

# Build the Next.js app
RUN npm run build

# Remove dev dependencies to reduce image size
RUN npm prune --production

# Expose port 3000
EXPOSE 3000

# Disable telemetry & set production
ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV=production

# Start the app
CMD ["node", "node_modules/.bin/next", "start", "-H", "0.0.0.0", "-p", "3000"]
