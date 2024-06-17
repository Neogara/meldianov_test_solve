FROM python:3
WORKDIR ./meltianov_test_service

COPY ./src ./
COPY ./requirements.txt ./
COPY ./.env ./
# --no-cache-dir
RUN python -m pip install  -r requirements.txt

CMD ["uvicorn", "service_app:app", "--host", "0.0.0.0", "--port", "8000"]
