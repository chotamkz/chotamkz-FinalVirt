FROM python:3.9-slim

ENV FLASK_APP=userDoner.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5003

WORKDIR /app/userDoner

COPY . /app/userDoner

RUN pip install --no-cache-dir -r /app/userDoner/requirements.txt

EXPOSE 5003

CMD ["python", "userDoner.py"]
