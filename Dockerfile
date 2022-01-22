FROM python:3.8-slim

RUN apt-get update -y

COPY ./src /clothing/src
COPY ./Pipfile /clothing/
COPY ./config.ini /clothing/
COPY ./app.py /clothing/

WORKDIR /clothing

RUN pip3 install pipenv --upgrade
RUN pipenv update

EXPOSE 5000

CMD ["pipenv", "run", "uvicorn", "app:app", "--port", "5000", "--host", "0.0.0.0"]