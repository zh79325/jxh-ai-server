#!/usr/bin/env python
from ultralytics import YOLO
from ultralytics.utils.checks import check_font

from build_model import datasets, model_yaml

def startTrain():
    print('load model_yaml from =>',model_yaml)
    model = YOLO('models/input/yolo11s.pt')  # build a new model from YAML
    results = model.train(data=model_yaml, epochs=100, imgsz=1440)

if __name__ == '__main__':
    startTrain()

