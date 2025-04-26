FROM python:3.13

RUN mkdir -p /usr/src/dating/profiles_service
WORKDIR /usr/src/dating/profiles_service

COPY . /usr/src/dating/profiles_service

RUN pip install --upgrade pip
RUN pip3 install --upgrade poetry==2.1.2

RUN python3 -m poetry config virtualenvs.create false \
    && python3 -m poetry install --no-interaction --no-ansi \
    && echo yes | python3 -m poetry cache clear . --all