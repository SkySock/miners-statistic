FROM python:3.9.6

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /miners

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y gcc python3-dev musl-dev
RUN apt-get install netcat -y
COPY ./req.txt .
RUN pip install --upgrade pip
RUN pip install -r req.txt

COPY . .

ENTRYPOINT ["./entrypoint.sh"]

#EXPOSE 8000
