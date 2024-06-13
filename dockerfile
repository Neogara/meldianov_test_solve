FROM pyton:3.9
WORKDIR ./src

COPY ./src ./
COPY ./requirements.txt ./
COPY ./.env ./

RUN pip install -r requirements.txt

CMD ["python", "-m","fastapi", " dev", "service_app.py"]
