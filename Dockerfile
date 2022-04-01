FROM python:3-slim

COPY . .

ENV DISCORD_SECRET_TOKEN= \
    DISCORD_CHANNEL_ID= \
    NBA_PT_DIFFERENTIAL=5 \
    NBA_MINS_LEFT=4 \
    NBA_PERIOD=4 \
    MLB_MINIMUM_INNING=9 \
    MLB_MAXIMUM_SCORE_DIFFERENTIAL=1 \
    MLB_THRESHOLD_MEN_ON_BASE="RISP" \
    TZ=America/New_York

RUN pip install pipenv \
    pipenv install

CMD pipenv run python src/main.py