import json
import os
import shutil
import urllib
from glob import glob
from pathlib import Path
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import yaml
from matplotlib.font_manager import fontManager
from ultralytics import YOLO
from ultralytics.utils.downloads import download

# bentchmark https://aiimg.obs.cn-east-3.myhuaweicloud.com/train/dataset/project-4-at-2024-11-13-00-59-ce04fdff.zip
# v2 https://aiimg.obs.cn-east-3.myhuaweicloud.com:443/train%2FAI%E5%95%86%E5%93%81%E5%BC%80%E5%8F%91%E6%B5%8B%E8%AF%95%E4%BC%81%E4%B8%9A%2Fjxh%2F20241128204154_Raw_82387.zip
dataset_url='https://aiimg.obs.cn-east-3.myhuaweicloud.com/labelstudio%2FAI%E5%95%86%E5%93%81%E5%BC%80%E5%8F%91%E6%B5%8B%E8%AF%95%E4%BC%81%E4%B8%9A%2Fexport%2FYOLO%2F20241225144442_Raw_71578.zip'
current = os.path.dirname(os.path.abspath('__file__'))
root = current
datasset_folder=Path(root+'/ls-export')
folder=root+'/dataset-download'
datasset_download_folder =Path(folder)
if  datasset_download_folder.exists():
    shutil.rmtree(datasset_download_folder)
os.makedirs(datasset_download_folder)
download(dataset_url,datasset_download_folder)
subfolders= [f.path for f in os.scandir(folder) if f.is_dir()]
folder=subfolders[0]
datasets = root+'/yolo_datasets'
model_yaml = os.path.abspath(f'{datasets}/data.yaml')
print('\n\n\n==========\n\n')
print('datasset_download_folder=>',folder,end='\n')
txts = glob(folder + '/**/*.txt')
images = glob(folder + '/**/*.jpg')

# Create DataFrame
df = pd.DataFrame({'txt': txts, 'image': images})

if os.path.exists(datasets):
    shutil.rmtree(datasets)
# Shuffle and split data
df = df.sample(frac=1, random_state=42).reset_index(drop=True)
all_train = len(df) < 100
train_size = int(0.8 * len(df))
if all_train:
    train_size = len(df)
train_df = df.iloc[:train_size]
test_df = []
val_df = []
if all_train:
    test_df = train_df
    val_df = train_df
else:
    test_df = df.iloc[train_size:]
    val_df = test_df.sample(frac=0.5)
    test_df = test_df.drop(val_df.index)

print('building data set')
# Create directories
for split in ['train', 'test', 'val']:
    os.makedirs(f'{datasets}/{split}/images', exist_ok=True)
    os.makedirs(f'{datasets}/{split}/labels', exist_ok=True)

# Copy files to respective directories
for split, split_df in [('train', train_df), ('test', test_df), ('val', val_df)]:
    for _, row in split_df.iterrows():
        shutil.copy(row['image'], f'{datasets}/{split}/images')
        shutil.copy(row['txt'], f'{datasets}/{split}/labels')

with open(f'{folder}/notes.json', 'r') as file:
    notes = json.load(file)

labelList = []
for label in notes['categories']:
    name = urllib.parse.unquote(label['name'])
    labelList.append(name)

print("parse yaml success labels =>", labelList)

data = dict(
    train='train/images',
    val='val/images',
    test='test/images',
    nc=len(labelList),
    names=labelList
)
with open(model_yaml, 'w') as outfile:
    yaml.dump(data, outfile, default_flow_style=False)

print('finish model_yaml in=>', model_yaml)





def startTrain():
    mpl_data_path = mpl.get_data_path()
    mpl_fonts_folder = mpl_data_path + '/fonts/ttf'
    print("get_data_path=>", mpl.get_data_path())
    if not os.path.exists(mpl_fonts_folder + '/SimHei.ttf'):
        shutil.copyfile(root + '/SimHei.ttf', mpl_fonts_folder + '/SimHei.ttf')
    fontManager.addfont(mpl_fonts_folder + '/SimHei.ttf')
    plt.rcParams["font.family"] = "SimHei"
    plt.rcParams['font.sans-serif'] = ['SimHei']  #用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  #用来正常显示负号


    init_model=root+'/models/input/yolo11l.pt'
    print('load init_model from =>',init_model)
    print('load model_yaml from =>',model_yaml)
    model = YOLO(init_model)  # build a new model from YAML
    results = model.train(data=model_yaml,batch=1, epochs=100, imgsz=1440)
    pass


if __name__ == '__main__':
    startTrain()
