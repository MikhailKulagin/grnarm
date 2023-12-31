FROM python:3.8

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY .. .

CMD ["python3", "./app/service.py"]