FROM node:22.23.4-slim

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

COPY index.js index.ejs design.css ./

CMD ["node", "index.js"]
