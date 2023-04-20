FROM python:3.11.3-slim

WORKDIR /app

COPY Pipfile .
COPY Pipfile.lock .

RUN python -m pip install pipenv
RUN pipenv install --ignore-pipfile --deploy

#  dont import .env ?, just copy /src . breaks manual install method in favor of docker compose portability
COPY . .

CMD pipenv run python src/main.py
