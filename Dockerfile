FROM python:3.8-alpine

USER root

WORKDIR /app

# Install Git and tools
RUN apk --no-cache add git zip

RUN git config --global --add safe.directory /app

# Clone the Git repository
RUN git clone https://github.com/eliasedwin7/comicviewer.git /app

# Install Python requirements
RUN pip install --requirement /app/requirements.txt

# Set execute permissions on start script
RUN chmod +x /app/start.sh

CMD ["/app/start.sh"]
