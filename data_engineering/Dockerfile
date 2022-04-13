FROM python:3.9-alpine
RUN apk --no-cache add musl-dev g++

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /data_engineering

WORKDIR /data_engineering
ENV PYTHONPATH="/data_engineering"
ENTRYPOINT ["python", "assignment/data_engine.py"]
