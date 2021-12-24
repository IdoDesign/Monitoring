FROM python:3.8-slim-buster
#install required tools
RUN apt-get update && apt-get install -y iputils-ping && apt-get install -y netcat

RUN mkdir /app
ADD . /app
WORKDIR /app
#install python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# run entrypoint.sh to validate psql availability
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]

CMD ["python", "app.py"]