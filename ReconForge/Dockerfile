FROM python:3.11-slim

WORKDIR /app

COPY . .
RUN pip install --no-cache-dir .

ENTRYPOINT ["reconforge"]
CMD ["discover", "https://example.com"]
