# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /crm
RUN pip install --upgrade pip
COPY requirements.txt /crm/
RUN pip install -r requirements.txt
COPY . /crm/


EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
