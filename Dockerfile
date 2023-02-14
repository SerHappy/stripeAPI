FROM python:3.10

RUN apt-get upgrade && apt-get update

RUN mkdir /app
COPY . /app/
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "manage.py" ]
CMD [ "runserver", "0.0.0.0:8000" ]
