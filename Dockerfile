FROM python:3.11.4-slim

WORKDIR /app

COPY Pipfile .
COPY Pipfile.lock .

RUN python -m pip install pipenv
RUN pipenv install --ignore-pipfile --deploy

COPY . .

CMD pipenv run python src/main.py
