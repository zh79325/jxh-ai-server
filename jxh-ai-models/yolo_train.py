#!/usr/bin/env python
from ultralytics import YOLO
from build_model import datasets, model_yaml

def startTrain():
    print('load model_yaml from =>',model_yaml)
    model = YOLO('models/input/yolo11n.pt')  # build a new model from YAML
    results = model.train(data=model_yaml, epochs=100, imgsz=640)

if __name__ == '__main__':
    startTrain()

