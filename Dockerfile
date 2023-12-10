FROM python:3.10

LABEL authors="Amir and Mansur"

WORKDIR /

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
RUN apt-get update && \
    apt-get install -y postgresql-server-dev-all gcc python3-dev musl-dev

# Upgrade pip
RUN pip install --upgrade pip

# Copy project
COPY . .
