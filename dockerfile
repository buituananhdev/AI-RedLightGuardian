FROM python

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y python3-opencv

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "app.py"]