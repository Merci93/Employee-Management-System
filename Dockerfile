FROM python3.11-slim

LABEL quay.expires-after=12w

WORKDIR /app

COPY . .

RUN apt-get-update && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python3", "src/main.py"]
