FROM python:3.8-slim-buster

WORKDIR /app
ADD . /app
RUN pip install poetry

RUN poetry install

EXPOSE 8000
CMD ["sh", "main.sh"]