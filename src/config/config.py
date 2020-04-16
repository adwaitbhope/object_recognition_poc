import os

# Directories to store data
BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
CONFIG_DIR = os.path.join(os.getcwd(), 'config')
IMAGE_DIR = os.path.join(BASE_DIR, 'images')
ANNOTATIONS_DIR = os.path.join(IMAGE_DIR, 'annotations')

# List of models
# Add a new entry if you want to use a custom built model
# @param name: Name that is displayed in the GUI
# @param url: URL of the tar.gz file OR name of the folder in the 'models' dir
# Note: the folder should contain 'frozen_inference_graph.pb'
MODELS = [{
        'name': 'SSD Inception V2',
        'url': 'http://download.tensorflow.org/models/object_detection/ssd_inception_v2_coco_2018_01_28.tar.gz'
    }, {
        'name': 'SSD MobileNet V2',
        'url': 'http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v2_coco_2018_03_29.tar.gz'
    }, {
        'name': 'Faster RCNN Inception V2',
        'url': 'http://download.tensorflow.org/models/object_detection/faster_rcnn_inception_v2_coco_2018_01_28.tar.gz',
    }, {
        'name': 'Sample test file',
        'url': 'https://dev-files.blender.org/file/download/bwdp5reejwpkuh5i2oak/PHID-FILE-nui3bpuan4wdvd7yzjrs/sample.tar.gz'
    }
]

# Colors used in annotation
COLORS = {
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'brown': (255, 255, 0),
}

# Categories based on the labels in COCO dataset
LABEL_CATEGORIES = {
    'Person': {
        'labels': [1],
        'color': COLORS['white'],
    },
    'Vehicles': {
        'labels': [2, 3, 4, 6, 7, 8],
        'color': COLORS['black'],
    },
    'Animals': {
        'labels': [i for i in range(16, 26)],
        'color': COLORS['red'],
    },
    'Fruits': {
        'labels': [i for i in range(52, 62)],
        'color': COLORS['green'],
    },
    'Electronics': {
        'labels': [i for i in range(72, 78)],
        'color': COLORS['blue'],
    },
    'Furniture': {
        'labels': [i for i in range(62, 72)],
        'color': COLORS['brown'],
    },
}
