FROM python:3.10-slim

RUN mkdir /app
EXPOSE 8000

RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "main:app"]
