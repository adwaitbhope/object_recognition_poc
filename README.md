# Object Recognition POC  

A python application developed to demonstrate object recognition using pre-trained models from [TensorFlow Model Zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md).  

![screenshot](https://github.com/adwaitbhope/object_recognition_poc/blob/master/screenshot.jpg)  


## Running  
1. Clone the repo and create a virtual environment using something like [virtualenv](https://pypi.org/project/virtualenv/).

2. Install all dependencies using `pip install -r requirements.txt`

3. Download these models and extract them  
      [SSD Inception V2](http://download.tensorflow.org/models/object_detection/ssd_inception_v2_coco_2018_01_28.tar.gz)  
      [SSD MobileNet V2](http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v2_coco_2018_03_29.tar.gz)  
      [Faster RCNN Inception V2](http://download.tensorflow.org/models/object_detection/faster_rcnn_inception_v2_coco_2018_01_28.tar.gz)  

4. The directory structure should look like
```bash
      object_recognition_poc/  
      ├── coco_labels.txt  
      ├── requirements.txt  
      ├── images  
      │   ├── car and pedestrian.jpg  
      │   ├── desk (1).jpeg  
      │   ├── desk.jpg  
      │   ├── furniture.jpg  
      │   ├── puppy.jpg  
      │   └── vehicles.jpg  
      ├── models  
      │   ├── faster_rcnn_inception_v2_coco_2018_01_28  
      │   │   └── frozen_inference_graph.pb  
      │   ├── ssd_inception_v2_coco_2018_01_28  
      │   │   └── frozen_inference_graph.pb  
      │   └── ssd_mobilenet_v2_coco_2018_03_29  
      │       └── frozen_inference_graph.pb  
      └── src  
          ├── annotations.py  
          ├── gui.py  
          ├── main.py  
          └── object_detector.py  
```
5. Run `src/main.py`

> Tested only on Ubuntu 18.04, might not work on Windows.
