FROM python:3-slim

COPY . .

ENV DISCORD_TOKEN= \
    DISCORD_CHANNEL= \
    NBA_THRESHOLD_PT_DIFFERENTIAL= \
    NBA_THRESHOLD_MINS_LEFT= \
    NBA_THRESHOLD_PERIOD= \
    MLB_THRESHOLD_SCORE_DIFFERENTIAL= \
    MLB_THRESHOLD_MEN_ON_BASE= \
    MLB_THRESHOLD_INNING= \
    TZ= \
    PUID= \
    PGID=

RUN pip install pipenv \
    pipenv install

CMD pipenv run python src/main.py

VOLUME /config

ENTRYPOINT [ "/sportsnow" ]