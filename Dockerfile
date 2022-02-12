FROM python:3.8-slim-buster

WORKDIR /app

RUN pip3 install --upgrade pip
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

COPY ./entrypoint.sh /
ENTRYPOINT [ "sh", "/entrypoint.sh" ]
#CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
