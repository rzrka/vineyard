from node:alpine
RUN apk update && apk add bash
WORKDIR '/app'
COPY package.json .
run npm install
copy . .