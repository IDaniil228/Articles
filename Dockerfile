FROM python:3.12-alpine
WORKDIR /python_app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "manage.py", "runserver"]