# Stage 1: Install dependencies
FROM python:3.12-alpine AS builder
RUN apk update && apk upgrade

WORKDIR /app
COPY app/requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Production image
FROM python:3.12-alpine

RUN adduser -D -u 10001 appuser
WORKDIR /app

COPY --from=builder /install /usr/local
COPY app/ .

USER appuser
EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
