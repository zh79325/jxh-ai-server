import cv2
import os

dir = os.path.dirname(os.path.abspath(__file__))
wechat_qr = cv2.wechat_qrcode_WeChatQRCode(dir + "/jxh_ai/detect.prototxt", dir + "/jxh_ai/detect.caffemodel",
                                           dir + "/jxh_ai/sr.prototxt", dir + "/jxh_ai/sr.caffemodel")
