FROM python:3-slim-bullseye

COPY . .

RUN pip install --upgrade pip -r requirements.txt

CMD python src/main.py
