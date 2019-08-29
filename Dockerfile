FROM python:3.7-slim-stretch AS builder
COPY . /app
WORKDIR /app
RUN apt-get update && apt-get install -y git python3-dev gcc \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade -r requirements.txt

FROM python:3.7-slim-stretch AS release
WORKDIR /app
COPY --from=builder /app /app
COPY --from=builder /root/.cache /root/.cache
RUN pip install --upgrade -r requirements.txt && rm -rf /root/.cache

ENV PORT 8080
CMD [ "python", "app.py" ]
