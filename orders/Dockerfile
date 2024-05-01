
FROM python:3.9-slim

ENV FLASK_APP=orderDoner.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5001

WORKDIR /app/orderDoner

COPY . /app/orderDoner

RUN pip install --no-cache-dir -r /app/orderDoner/requirements.txt

EXPOSE 5001

CMD ["python", "orderDoner.py"]
