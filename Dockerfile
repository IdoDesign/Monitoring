FROM python:3.8-slim-buster
RUN apt-get update && apt-get install -y iputils-ping
RUN mkdir /app
ADD . /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python", "app.py"]