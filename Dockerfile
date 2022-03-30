FROM python:3-slim-bullseye

COPY . .

RUN pip install pipenv
RUN pipenv install

CMD pipenv run python src/main.py
