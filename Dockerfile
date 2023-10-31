FROM python:3.8-alpine

USER root

WORKDIR /app

# Install Git, tools, and build dependencies
RUN apk --no-cache add git zip \
    && apk --no-cache add --virtual build-deps build-base libffi-dev openssl-dev

RUN git config --global --add safe.directory /app

# Clone the Git repository
RUN git clone https://github.com/eliasedwin7/comicviewer.git /app

# Install Python requirements
RUN pip install --requirement /app/requirements.txt

# Remove build dependencies to reduce image size
RUN apk del build-deps

# Set execute permissions on start script
RUN chmod +x /app/start.sh

CMD ["/app/start.sh"]
