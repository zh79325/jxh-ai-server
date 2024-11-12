FROM registry.cn-hangzhou.aliyuncs.com/ali-build/jxh-ai-server:runtime
ENV BUILDKIT_PROGRESS=plain
WORKDIR /app
#COPY requirements.txt .
COPY jxhaiserver/ /app/
RUN ls -l
EXPOSE 8010
CMD ["python", "manage.py", "runserver", "0.0.0.0:8010"]
#ADD docker-entrypoint.sh /docker-entrypoint.sh
#RUN chmod a+x /docker-entrypoint.sh
#ENTRYPOINT ["/docker-entrypoint.sh"]
#RUN  cat /app/deploy
#DOCKER_BUILDKIT=0 docker build .
#docker-compose build
#RUN /app/deploy run-model-id --apikey land_sk_w5vxxuoKvJmrFzvwCdPk8qpQwk0Gau6cJD9H6YBnA3vETaPs9D --model afa8e461-b35e-42df-9e63-fd6dd384aa0b
