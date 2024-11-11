# jxh-ai-server

# 本地构建调试
```angular2html
DOCKER_BUILDKIT=0 docker build .
```

# 启动
```angular2html
docker pull registry.cn-hangzhou.aliyuncs.com/ali-build/jxh-ai-server:latest
docker run -p 8010:8000 registry.cn-hangzhou.aliyuncs.com/ali-build/jxh-ai-server:latest
```


