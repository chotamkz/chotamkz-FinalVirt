
FROM python:3.9-slim

ENV FLASK_APP=productDoner.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5002

WORKDIR /app/productDoner

COPY . /app/productDoner

RUN pip install --no-cache-dir -r /app/productDoner/requirements.txt

EXPOSE 5002

CMD ["python", "productDoner.py"]
