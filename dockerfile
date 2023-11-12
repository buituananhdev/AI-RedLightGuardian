FROM python

WORKDIR /app

ENV PORT 3012

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "app.py"]