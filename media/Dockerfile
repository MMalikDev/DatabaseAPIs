ARG VERSION=stable-alpine
FROM nginx:$VERSION as builder

WORKDIR /server

# Setup Configuration
COPY ./nginx.conf /etc/nginx/nginx.conf

# Create a non-privileged user 
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "$UID" \
    server

# ------------------------------------------------------------ #

FROM builder AS testing
# USER server
COPY . .
