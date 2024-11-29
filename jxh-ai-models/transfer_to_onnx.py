#!/usr/bin/env python
from ultralytics import YOLO


if __name__ == '__main__':
    # Load the YOLO11 model
    model = YOLO("/Users/eleme/Desktop/ls/qrdet-s.pt")

    # Export the model to ONNX format
    onnx_path=model.export(format="onnx")
    print('export onnx success'+onnx_path)
    print(model.names)
