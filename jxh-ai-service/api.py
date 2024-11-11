from django.http import HttpResponse
from rest_framework import generics
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from django.http import JsonResponse
from . import jxh_models
import requests
import tempfile


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

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
