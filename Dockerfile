FROM python:3.11
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
#RUN  cat /app/deploy
#DOCKER_BUILDKIT=0 docker build .
#docker-compose build
#RUN /app/deploy run-model-id --apikey land_sk_w5vxxuoKvJmrFzvwCdPk8qpQwk0Gau6cJD9H6YBnA3vETaPs9D --model afa8e461-b35e-42df-9e63-fd6dd384aa0b
