from ultralytics import YOLO
import pathlib

product_detector = YOLO("./jxh-ai-service/jxh_ai/product.pt")
qr_detector = YOLO("./jxh-ai-service/jxh_ai/qrdet-s.pt")
