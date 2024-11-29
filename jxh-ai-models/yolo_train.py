#!/usr/bin/env python
import os
import shutil
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.font_manager import fontManager

from ultralytics import YOLO
from build_model import model_yaml


mpl_data_path = mpl.get_data_path()
mpl_fonts_folder = mpl_data_path + '/fonts/ttf'
print("get_data_path=>", mpl.get_data_path())
if not os.path.exists(mpl_fonts_folder + '/SimHei.ttf'):
    shutil.copyfile(os.path.dirname(os.path.abspath('__file__')) + '/SimHei.ttf', mpl_fonts_folder + '/SimHei.ttf')
fontManager.addfont(mpl_fonts_folder + '/SimHei.ttf')
plt.rcParams["font.family"] = "SimHei"
plt.rcParams['font.sans-serif'] = ['SimHei']  #用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  #用来正常显示负号


def startTrain():
    print('load model_yaml from =>', model_yaml)
    model = YOLO('models/input/yolo11s.pt')  # build a new model from YAML
    results = model.train(data=model_yaml, epochs=100, imgsz=1440)


if __name__ == '__main__':
    startTrain()
