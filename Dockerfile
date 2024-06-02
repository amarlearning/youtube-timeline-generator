FROM python:3.8-slim-buster

WORKDIR /app
ADD . /app

RUN apt-get update && apt-get install -y curl git make

RUN pip install poetry

RUN poetry install

EXPOSE 8000

CMD ["poetry", "run", "sh", "main.sh"]
