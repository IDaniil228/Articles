FROM python:3.12-alpine
WORKDIR /python_app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "manage.py", "runserver"]