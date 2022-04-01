if [ ! -f .env ]
then
  export $(cat .env | xargs)
fi

pipenv run python src/main.py