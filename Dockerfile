FROM python:3-slim

COPY . .

ENV DISCORD_TOKEN= \
    DISCORD_CHANNEL= \
    NBA_THRESHOLD_PT_DIFFERENTIAL=5 \
    NBA_THRESHOLD_MINS_LEFT=4 \
    NBA_THRESHOLD_PERIOD=4 \
    MLB_THRESHOLD_SCORE_DIFFERENTIAL=1 \
    MLB_THRESHOLD_MEN_ON_BASE="RISP" \
    MLB_THRESHOLD_INNING=9 \
    TZ=America/New_York

RUN pip install pipenv \
    pipenv install \
    mkdir /data

CMD pipenv run python src/main.py

VOLUME /data

ENTRYPOINT [ "/sportsnow" ]