FROM python:3
WORKDIR ./meltianov_test_service

COPY ./src ./
COPY ./requirements.txt ./
COPY ./.env ./
# --no-cache-dir
RUN python -m pip install  -r requirements.txt

CMD ["fastapi", "dev", "service_app.py"]
# CMD ["python","./service_app.py"]
