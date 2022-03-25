FROM python:latest

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

ENV REDIS_HOST=redis-cache
ENV MONGO_HOST=db

RUN rm -rf /app/agro
COPY ./agro /app/agro

CMD ["uvicorn", "agro.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]