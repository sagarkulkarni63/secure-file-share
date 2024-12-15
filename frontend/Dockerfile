FROM node:18-alpine as build
WORKDIR /app
COPY package.json yarn.lock ./
RUN yarn install
COPY . .
RUN yarn build

FROM node:18-alpine
WORKDIR /app
COPY --from=build /app/build /app/build
RUN yarn global add serve
EXPOSE 3000
CMD ["serve", "-s", "build"]
