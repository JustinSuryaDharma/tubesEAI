FROM node:14
WORKDIR /attraction
COPY package*.json /attracion
RUN npm install
COPY app.js /attraction
EXPOSE 3000
CMD ["node", "index.js"]