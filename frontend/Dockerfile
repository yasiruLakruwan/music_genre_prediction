FROM node:18-alpine AS build
WORKDIR /app

# Copy package files and install dependancies.

COPY package*.json ./
RUN npm install

# Copy all frontend files
COPY . .

ARG REACT_APP_API_URL
ENV REACT_APP_API_URL=$REACT_APP_API_URL

# Build the React app
RUN npm run build

# ---------- Stage 2: Serve with NGINX ----------
FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html

#Expose the port
EXPOSE 80

# Start NGINX
CMD ["nginx", "-g", "daemon off;"]