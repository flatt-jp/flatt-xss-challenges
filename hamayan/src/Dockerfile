FROM node:20-slim

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

COPY index.js index.ejs design.css ./

CMD ["node", "index.js"]
