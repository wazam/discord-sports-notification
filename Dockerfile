FROM python:3.10.4-slim

WORKDIR /discord

COPY Pipfile .
COPY Pipfile.lock .

RUN pip install pipenv
RUN pipenv install --deploy --ignore-pipfile

COPY . .

CMD pipenv run python src/main.py
