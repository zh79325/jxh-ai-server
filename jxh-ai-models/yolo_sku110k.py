#!/usr/bin/env python
import os.path

from ultralytics import YOLO


def startTrain():
    pt = os.path.abspath('models/input/yolo11n.pt')
    print('pt file', pt)
    model = YOLO(pt)  # build a new model from YAML
    sku110k = os.path.abspath('models/input/sku110k.yaml')
    print('sku110k file', sku110k)
    results = model.train(data=sku110k, epochs=100, imgsz=640)


if __name__ == '__main__':
    startTrain()
