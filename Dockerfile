FROM python:latest

LABEL authors="Zeneto"

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /app
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ,"--reload"]