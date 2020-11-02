FROM python:3.6

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /src

RUN apt-get update && apt-get install -y gettext libgettextpo-dev zlib1g libjpeg-dev

RUN pip install --upgrade pip

COPY src/requirements.txt /scripts/
RUN pip install --no-cache-dir -r /scripts/requirements.txt

COPY /src/ /src/