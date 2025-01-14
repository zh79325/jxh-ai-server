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


def index(request):
    return HttpResponse("Hello, world.")


class TaskAPI(generics.RetrieveUpdateDestroyAPIView):
    parser_classes = (JSONParser, FormParser, MultiPartParser)


def getDetectResult(detector: jxh_models.YoloDetector, img):
    results = detector.detector(img)
    return {
        'code':  detector.model.model_code,
        'name': detector.model.model_name,
        'type': detector.model.type,
        'results': json.loads(results[0].to_json())
    }


def detect_all(request):
    image_url = request.GET.get('img')
    img_data = requests.get(image_url).content
    with tempfile.NamedTemporaryFile(suffix=".jpg") as fp:
        fp.write(img_data)
        img = fp.name
        qr_result = getDetectResult(jxh_models.qr_detector, img)
        shelve_result = getDetectResult(jxh_models.shelve_detector, img)
        productList = []
        for productModel in jxh_models.productModels:
            results = getDetectResult(productModel, img)
            productList.append(results)
        image = cv2.imread(img)
        fp.close()
        resp = {
            'qrResult': qr_result,
            'shelveResult': shelve_result,
            'modelResults': productList,
        }
        height, width, channels = image.shape
        if len(qr_result['results']) > 0:
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
