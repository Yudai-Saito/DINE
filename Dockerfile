FROM python:3.8

WORKDIR /usr/src/app

COPY Pipfile Pipfile.lock ./

RUN apt update && \
apt install -y pipenv && \
pipenv install --system

CMD ["python", "/usr/src/app/dine"]