from ultralytics import YOLO
import pathlib
import os

dir = os.path.dirname(os.path.abspath(__file__))
print("model dir======>" + dir)
product_model_file = dir + "/jxh_ai/product.pt"
print("product_model_file  exists %s => %s" % (os.path.exists(product_model_file), product_model_file))
product_detector = YOLO(product_model_file)
qr_model_file = dir + "/jxh_ai/qrdet-s.pt"
print("qr_model_file  exists %s => %s" % (os.path.exists(qr_model_file), qr_model_file))
qr_detector = YOLO(qr_model_file)
