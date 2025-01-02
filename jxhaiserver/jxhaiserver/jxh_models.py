import os
from collections import namedtuple
from enum import Enum

from ultralytics import YOLO

JxhProductModel = namedtuple('JxhProductModel', ['modelName', 'modelCode', 'modelPath','obb'])


class JxhProductModels(Enum):
    @property
    def model_path(self):
        return self.value.modelPath

    @property
    def abs_model_path(self):
        dir = os.path.dirname(os.path.abspath(__file__))
        return dir + '/' + self.model_path

    @property
    def model_name(self):
        return self.value.modelName

    @property
    def obb(self):
        return self.value.obb

    @property
    def model_code(self):
        return self.value.modelCode

    qr_code = JxhProductModel('二维码模型', 'qr_code', 'jxh_ai/qrdet-s.pt',False)
    normal_product = JxhProductModel('通用模型', 'normal_product', 'jxh_ai/product-obb-best.pt',True)
    #normal_product = JxhProductModel('通用模型', 'normal_product', 'jxh_ai/product.pt',False)
    benchmark_product = JxhProductModel('版本1-普通', 'benchmark_product', 'jxh_ai/jxh-product-nobb-latest.pt',False)
    latest_product = JxhProductModel('版本3-带旋转', 'latest_product', 'jxh_ai/jxh-product-obb-best.pt',True)

    def buildDetector(self):
        model_file = self.abs_model_path
        print("%s model exists %s => %s" % (self.model_name, os.path.exists(model_file), model_file))
        return YOLO(model_file)


class YoloDetector:
    def __init__(self, model: JxhProductModels):
        self.model = model
        self.detector = model.buildDetector()


productModels = []
for name, model in JxhProductModels.__members__.items():
    if model == JxhProductModels.qr_code:
        continue
    productModels.append(YoloDetector(model))

qr_detector = YoloDetector(JxhProductModels.qr_code)
