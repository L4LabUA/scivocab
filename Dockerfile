FROM python:3.8-slim


workdir scivocab
copy docker-requirements.txt .
run pip install -r docker-requirements.txt
copy . .
RUN pip install .
cmd gunicorn --bind 0.0.0.0:5000 "app:create_app()"
