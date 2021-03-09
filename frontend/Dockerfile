FROM node:12

RUN mkdir /frontend
WORKDIR /frontend

COPY . .

RUN npm ci
RUN npm run build

EXPOSE 3000
CMD [ "npm", "start" ]
