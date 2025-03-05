#!/usr/bin/env python
import os.path
import shutil
from pathlib import Path

import numpy as np
import pandas as pd
from tqdm import tqdm
from ultralytics import YOLO
from ultralytics.utils.downloads import download
from ultralytics.utils.ops import xyxy2xywh
import yaml

current = os.path.dirname(os.path.abspath('__file__'))
dir = Path(current+'/sku110k')  # dataset root dir
parent = Path(dir.parent)  # download dir
model_yaml = os.path.abspath(f'{current}/sku110k.yaml')
def download2():
    urls = ['http://trax-geometry.s3.amazonaws.com/cvpr_challenge/SKU110K_fixed.tar.gz']
    download(urls, dir=parent)
    # Rename directories
    if dir.exists():
        shutil.rmtree(dir)
    (parent / 'SKU110K_fixed').rename(dir)  # rename dir
    (dir / 'labels').mkdir(parents=True, exist_ok=True)  # create labels dir

    # Convert labels
    names = 'image', 'x1', 'y1', 'x2', 'y2', 'class', 'image_width', 'image_height'  # column names
    for d in 'annotations_train.csv', 'annotations_val.csv', 'annotations_test.csv':
        x = pd.read_csv(dir / 'annotations' / d, names=names).values  # annotations
        images, unique_images = x[:, 0], np.unique(x[:, 0])
        with open((dir / d).with_suffix('.txt').__str__().replace('annotations_', ''), 'w') as f:
            f.writelines(f'./images/{s}\n' for s in unique_images)
        for im in tqdm(unique_images, desc=f'Converting {dir / d}'):
            cls = 0  # single-class dataset
            with open((dir / 'labels' / im).with_suffix('.txt'), 'a') as f:
                for r in x[images == im]:
                    w, h = r[6], r[7]  # image width, height
                    xywh = xyxy2xywh(np.array([[r[1] / w, r[2] / h, r[3] / w, r[4] / h]]))[0]  # instance
                    f.write(f"{cls} {xywh[0]:.5f} {xywh[1]:.5f} {xywh[0]+xywh[2]:.5f} {xywh[1]:.5f} {xywh[0]+xywh[2]:.5f} {xywh[1]+xywh[3]:.5f} {xywh[0]:.5f} {xywh[1]+xywh[3]:.5f}\n")  # write label

def startTrain():
    labelList = ['object']
    data = dict(
        path=dir,
        train='train/images',
        val='val/images',
        test='test/images',
        nc=len(labelList),
        names=labelList
    )
    with open(model_yaml, 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)
    pt = os.path.abspath('models/input/yolo11l-obb.pt')
    print('pt file', pt)
    model = YOLO(pt)  # build a new model from YAML
    print('sku110k file', model_yaml)
    results = model.train(data=model_yaml, epochs=100, imgsz=640)


if __name__ == '__main__':
    startTrain()
