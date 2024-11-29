from ultralytics import YOLO


def startPredict():
    # Load a model
    # qrcode detect
    #model = YOLO("/Users/eleme/Desktop/ls/qrdet-l.pt")  # pretrained YOLO11n model
    # product detect
    model = YOLO("/jxh_ai/output/product.pt")

    # product detect
    results = model(["/Users/eleme/code/jxh-server/jingxiaohe-server/jxh-api-server/src/test/resources/1.jpg"])  # return a list of Results objects

    # Process results list
    for i, result in enumerate(results):
        boxes = result.boxes  # Boxes object for bounding box outputs
        masks = result.masks  # Masks object for segmentation masks outputs
        keypoints = result.keypoints  # Keypoints object for pose outputs
        probs = result.probs  # Probs object for classification outputs
        obb = result.obb  # Oriented boxes object for OBB outputs
        result.show()  # display to screen
        result.save(filename="result_%d.jpg" % i)  # save to disk


if __name__ == '__main__':
    startPredict()
