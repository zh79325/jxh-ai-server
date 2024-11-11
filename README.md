# jxh-ai-server

# 本地构建调试
```angular2html
DOCKER_BUILDKIT=0 docker build .  --tag jxh_local:latest
docker run --name jxh_local -p 8010:8010 jxh_local:latest
```

# 启动
```angular2html
docker pull registry.cn-hangzhou.aliyuncs.com/ali-build/jxh-ai-server:latest
docker run -p 8010:8010 registry.cn-hangzhou.aliyuncs.com/ali-build/jxh-ai-server:latest
```


