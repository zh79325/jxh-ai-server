# jxh-ai-server

# 本地构建调试
```angular2html
DOCKER_BUILDKIT=0 docker build .  --tag jxh_local:latest
docker run   -p 8010:8010 jxh_local:latest
```


# 启动
```angular2html
docker pull registry.cn-hangzhou.aliyuncs.com/ali-build/jxh-ai-server:latest
docker run -p 8010:8010 registry.cn-hangzhou.aliyuncs.com/ali-build/jxh-ai-server:latest
```

# 部署命令
```angular2html
rm -rf /root/aliyun/jxh-ai-model/server
mkdir /root/aliyun/jxh-ai-model/server

tar zxvf /root/aliyun/jxh-ai-model/package.tgz -C /root/aliyun/jxh-ai-model/server

cd /root/aliyun/jxh-ai-model/server
sh deploy.sh start
```



# 训练步骤
## 把导出的文件解压复制到 ls-export 目录
## 运行 build_model.py
## 运行 yolo_train.py
## obb需要运行300次

### 模型性能对比
| Model   | size(pixels) | mAPval50-95 | SpeedCPU ONNX(ms) | SpeedT4 TensorRT10(ms) | params(M) | FLOPs(B) |
|---------|--------------|-------------|-------------------|------------------------|-----------|----------|
| YOLO11n | 640          | 39.5        | 56.1 ± 0.8        | 1.5 ± 0.0              | 2.6       | 6.5      |
| YOLO11s | 640          | 47.0        | 90.0 ± 1.2        | 2.5 ± 0.0              | 9.4       | 21.5     |
| YOLO11m | 640          | 51.5        | 183.2 ± 2.0       | 4.7 ± 0.1              | 20.1      | 68.0     |
| YOLO11l | 640          | 53.4        | 238.6 ± 1.4       | 6.2 ± 0.1              | 25.3      | 86.9     |
| YOLO11x | 640          | 54.7        | 462.8 ± 6.7       | 11.3 ± 0.2             | 56.9      | 194.9    |


