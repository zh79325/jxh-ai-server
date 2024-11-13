#!/usr/bin/env python
from ultralytics import YOLO
from ultralytics.utils.checks import check_font

from build_model import datasets, model_yaml

def startTrain():
    print('load model_yaml from =>',model_yaml)
    f = check_font(font='Arial.ttf')
    f = check_font(font='DejaVu Sans.ttf')
    model = YOLO('models/input/yolo11n.pt')  # build a new model from YAML
    results = model.train(data=model_yaml, epochs=100, imgsz=640)

if __name__ == '__main__':
    startTrain()

