FROM python:3.11-slim

LABEL quay.expires-after=12w

RUN apt-get update && \
    apt-get install -y --no-install-recommends g++ gcc libpq-dev && \ 
    apt-get autoremove -yqq --purge && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    python -m pip install --upgrade pip

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host=0.0.0.0", "--port=8000"]
