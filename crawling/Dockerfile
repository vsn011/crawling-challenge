FROM python:3.10-alpine

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /assignment

WORKDIR /assignment
ENV PYTHONPATH="/assignment"
ENTRYPOINT ["python", "assignment/scrape.py"]
