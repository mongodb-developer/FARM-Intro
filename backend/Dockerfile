FROM python:3.8-slim

ADD requirements.txt /src/
WORKDIR /src

RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "main.py" ]
