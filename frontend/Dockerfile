FROM node:18-alpine
RUN mkdir /frontend
WORKDIR /frontend
COPY package.json /frontend/package.json
ENV PATH /app/node_modules/.bin:$PATH
RUN npm install