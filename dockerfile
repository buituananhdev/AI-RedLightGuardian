FROM python

WORKDIR /app

ENV PORT 3012

COPY . .

RUN python -m venv venv
RUN /bin/bash -c "source venv/bin/activate"

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "app.py"]
