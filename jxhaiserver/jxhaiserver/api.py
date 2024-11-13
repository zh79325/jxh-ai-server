from django.http import HttpResponse
from rest_framework import generics
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from django.http import JsonResponse
from . import jxh_models,jxh_cv
import requests
import tempfile
import json
import cv2


def index(request):
    return HttpResponse("Hello, world.")


class TaskAPI(generics.RetrieveUpdateDestroyAPIView):
    parser_classes = (JSONParser, FormParser, MultiPartParser)


def qr_detect(request):
    image_url = request.GET.get('img')
    return detecetImageItems(jxh_models.qr_detector, image_url)


def detecetImageItems(detector, image_url):
    img_data = requests.get(image_url).content
    with tempfile.NamedTemporaryFile(suffix=".jpg") as fp:
        fp.write(img_data)
        img = fp.name
        results = detector(img)
        fp.close()
        items = []
        for i, result in enumerate(results):
            items.append(result.tojson())
        return JsonResponse(items, safe=False)


def product_detect(request):
    image_url = request.GET.get('img')
    return detecetImageItems(jxh_models.product_detector, image_url)


def detect_all(request):
    image_url = request.GET.get('img')
    img_data = requests.get(image_url).content
    with tempfile.NamedTemporaryFile(suffix=".jpg") as fp:
        fp.write(img_data)
        img = fp.name
        qr_results = jxh_models.qr_detector(img)
        product_results = jxh_models.product_detector(img)
        jxh_product_results = jxh_models.jxh_product_detector(img)
        image = cv2.imread(img)
        fp.close()
        resp = {
            'qrList': json.loads(qr_results[0].to_json()),
            'productList': json.loads(product_results[0].to_json()),
            'jxhProductList': json.loads(jxh_product_results[0].to_json()),
        }
        if len(resp['qr']) > 0:
            for qr in resp['qr']:
                box = qr['box']
                qr_crop = image[int(box['y1']):int(box['y2']), int(box['x1']):int(box['x2'])]
                res, points = jxh_cv.wechat_qr.detectAndDecode(qr_crop)
                if len(res) > 0:
                    qr['name'] = res[0]
        return JsonResponse(resp, safe=False)


def info(request):
    return JsonResponse(jxh_models.jxh_model_info, safe=False)
