FROM python:3.10.5-slim

# Add build dependencies
RUN apt-get update && \
    apt-get -y install gcc musl-dev

# Add pre-requisites for python packaging
RUN pip install --upgrade pip
RUN pip install poetry==1.1.13

# Configuring poetry
RUN poetry config virtualenvs.create false

# Copying requirements of a project
COPY pyproject.toml poetry.lock /app/src/
WORKDIR /app/src

# Installing requirements
RUN poetry install

# Copying actuall application
COPY . /app/src/
RUN poetry install

CMD ["/usr/local/bin/python", "-m", "car_rental_service"]
