ARG VERSION=20-bookworm-slim
FROM node:$VERSION AS builder

WORKDIR /server
COPY package*.json ./

RUN npm install
# RUN npm ci --omit=dev

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "$UID" \
    code

# ------------------------------ #

FROM oven/bun:1.0 AS testing

WORKDIR /server
COPY package*.json ./

RUN bun install

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "$UID" \
    code

# ------------------------------ #

FROM builder AS production
ENV NODE_ENV=production
USER code

COPY . .

CMD ["npm", "start"]
