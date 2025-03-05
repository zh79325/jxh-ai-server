import os.path

from django.http import HttpResponse
from rest_framework import generics
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from django.http import JsonResponse
from . import jxh_models, jxh_cv
import requests
import tempfile
import json
import cv2

from .jxh_models import JxhProductModels, YoloDetector


def index(request):
    return HttpResponse("Hello, world.")


class TaskAPI(generics.RetrieveUpdateDestroyAPIView):
    parser_classes = (JSONParser, FormParser, MultiPartParser)


def getDetectResult(detector: jxh_models.YoloDetector, img):
    results = detector.detector(img)
    return {
        'code': detector.model.model_code,
        'name': detector.model.model_name,
        'type': detector.model.type,
        'results': json.loads(results[0].to_json())
    }


def detect_all(request):
    image_url = request.GET.get('img')
    models_param = request.GET.get('models')
    models = []
    if models_param:
        models.extend(models_param.split(','))
    product_models = []
    for model in jxh_models.productModels:
        if len(models) == 0 or model.model.model_code in models:
            product_models.append(model)

    need_qr = False
    if len(models) == 0 or jxh_models.qr_detector.model.model_code in models:
        need_qr = True
    need_shelve = False
    if len(models) == 0 or jxh_models.shelve_detector.model.model_code in models:
        need_shelve = True
    img_data = requests.get(image_url).content
    with tempfile.NamedTemporaryFile(suffix=".jpg") as fp:
        fp.write(img_data)
        img = fp.name
        qr_result = None
        if need_qr:
            qr_result = getDetectResult(jxh_models.qr_detector, img)
        shelve_result = None
        if need_shelve:
            shelve_result = getDetectResult(jxh_models.shelve_detector, img)
        product_list = []
        for productModel in product_models:
            results = getDetectResult(productModel, img)
            product_list.append(results)
        image = cv2.imread(img)
        fp.close()
        resp = {
            'qrResult': qr_result,
            'shelveResult': shelve_result,
            'modelResults': product_list,
        }
        height, width, channels = image.shape
        if qr_result != None and len(qr_result['results']) > 0:
            for qr in qr_result['results']:
                box = qr['box']
                y1 = int(box['y1'])
                y2 = int(box['y2'])
                box_height = y2 - y1
                y1 -= int(box_height / 2)
                if y1 < 0:
                    y1 = 0
                y2 += int(box_height / 2)
                if y2 > height:
                    y2 = height
                x1 = int(box['x1'])
                x2 = int(box['x2'])
                box_width = x2 - x1
                x1 -= int(box_width / 2)
                if x1 < 0:
                    x1 = 0
                x2 += int(box_width / 2)
                if x2 > width:
                    x2 = width
                qr_crop = image[y1:y2, x1:x2]
                res, points = jxh_cv.wechat_qr.detectAndDecode(qr_crop)
                if len(res) > 0:
                    qr['content'] = res[0]
        return JsonResponse(resp, safe=False)


def info(request):
    results = []
    for productModel in jxh_models.productModels:
        r = {
            'name': productModel.model.model_name,
            'path': productModel.model.abs_model_path,
            'exists': os.path.exists(productModel.model.abs_model_path)
        }
        results.append(r)
    return JsonResponse(results, safe=False)
