FROM python:3.8

WORKDIR /app

RUN apt-get update
RUN apt-get install build-essential

RUN python -m pip install --upgrade pip
COPY ./requirements.txt .
RUN python -m pip install -r requirements.txt

COPY . .

EXPOSE 4500

CMD ["python", "app.py"]