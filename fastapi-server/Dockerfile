FROM python:latest

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./agro /app/agro

CMD ["uvicorn", "agro.main:app", "--host", "0.0.0.0", "--port", "80"]