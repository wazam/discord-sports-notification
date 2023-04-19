FROM python:3.11.3-slim

WORKDIR /app

COPY Pipfile .
COPY Pipfile.lock .

# RUN pip install pip --upgrade
RUN python -m pip install pipenv
RUN pipenv install --ignore-pipfile --deploy

COPY . .

CMD pipenv run python src/main.py
