#!/usr/bin/env python
import os
import pandas as pd
from glob import glob
import shutil
import yaml
import json
import urllib

folder = 'ls-export'
datasets = 'yolo_datasets'
model_yaml = os.path.abspath(f'{datasets}/data.yaml')


def buildDataset():
    # Load exported data
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


if __name__ == '__main__':
    buildDataset()
