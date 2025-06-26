#FROM python:latest
#
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONNUNBUFFERED 1
#
#WORKDIR /app
#
#COPY ./requirements.txt /app
#
#COPY . /app
#
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


FROM python:3.8-slim-buster as builder

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y gcc netcat nano libmagic1 build-essential gdal-bin libgdal-dev gettext gettext-base \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install watchdog
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt
RUN pip install watchdog

#########
# FINAL #
#########

FROM python:3.8-slim-buster

RUN mkdir -p /home/app

RUN apt-get update \
    && apt-get install -y netcat nano libmagic1 \
    && apt-get clean

RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev

ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/media
WORKDIR $APP_HOME

COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .

RUN pip install --upgrade pip
RUN python -m venv venv
ENV PATH="$HOME/venv/bin:$PATH"

RUN pip install --no-cache /wheels/*

COPY ./core $APP_HOME
COPY .env $APP_HOME/

RUN chmod +x /home/app/web/manage.py
