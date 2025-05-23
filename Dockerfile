FROM python:3.12

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app

CMD ["uvicorn", "main:root_app", "--host", "0.0.0.0", "--port", "8000"]
