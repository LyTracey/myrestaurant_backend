# syntax=docker/dockerfile:1

FROM python:3.11


RUN mkdir -p /usr/src/app
RUN mkdir -p /usr/src/app/backend

WORKDIR /usr/src/app/backend

ENV PYTHONDONTWRITEBYTECODE 1
# A non-null PYTHONUNBUFFERED ensures that python 
# output is sent straight to the terminal without being 
# buffered. It helps in debugging.
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
COPY setup.py .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
