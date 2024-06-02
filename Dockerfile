FROM ubuntu:20.04

WORKDIR /app
ADD . /app

RUN apt-get update && apt-get install -y python3 python3-pip

RUN apt-get update && apt-get install -y curl git make

RUN pip install poetry

RUN poetry install

EXPOSE 5443

CMD ["poetry", "run", "sh", "main.sh"]

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD curl --fail http://localhost:5443/health || exit 1