FROM python:3.11
LABEL authors="CherrySuryp"

RUN mkdir "/booking"
WORKDIR /booking
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]

