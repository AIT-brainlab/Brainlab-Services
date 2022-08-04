FROM node:16-buster
WORKDIR /home/app


EXPOSE 80

COPY ./app/package*.json .
RUN npm install

COPY ./app .

CMD npm run dev
