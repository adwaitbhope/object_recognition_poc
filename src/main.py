import numpy as np
import cv2
import os, glob
from gui import GUI
from object_detector import DetectorAPI
import annotations

class Handler:

    def load_image(self, frame=None):
        os.chdir(self.img_dir)
        if frame is None:
            self.img_processed = False
            frame = cv2.imread(self.images[self.img_index])
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            resize_width, resize_height = 0, 0
            if frame.shape[1] / frame.shape[0] > self.img_width / self.img_height:
                resize_width = self.img_width
                resize_height = self.img_width * frame.shape[0] / frame.shape[1]
            else:
                resize_height = self.img_height
                resize_width = self.img_height * frame.shape[1] / frame.shape[0]

            frame = cv2.resize(frame, (int(resize_width), int(resize_height)))
            self.un_annotated_frame = frame.copy()

        self.gui.load_image(frame)

    def on_dir_selected(self, path):
        os.chdir(path)
        self.img_dir = path
        self.img_index = 0
        self.images = glob.glob('*.jpg')
        self.images.extend(glob.glob('*.jpeg'))
        self.images.extend(glob.glob('*.png'))
        self.images.extend(glob.glob('*.JPG'))
        self.images.extend(glob.glob('*.JPEG'))
        self.images.extend(glob.glob('*.PNG'))
        self.images.sort()

        if len(self.images) == 0:
            self.gui.show_error('No images in this directory')
            self.img_dir = None
            return

        self.load_image()

    def on_prev_clicked(self):
        self.img_index = (self.img_index - 1) % len(self.images)
        self.load_image()

    def on_next_clicked(self):
        self.img_index = (self.img_index + 1) % len(self.images)
        self.load_image()

    def on_detect_clicked(self, model, threshold, classes, colors):
        if self.img_dir is None:
            self.gui.show_error('Directory not selected')
            return

        os.chdir(self.base_working_dir)
        path = '../models/' + model + '/frozen_inference_graph.pb'
        self.threshold = threshold
        odapi = DetectorAPI(path_to_ckpt=path)
        self.pred_boxes, self.pred_scores, self.pred_classes, self.pred_num = odapi.process_frame(self.un_annotated_frame)

        annotated_frame = self.un_annotated_frame.copy()
        for i, box in enumerate(self.pred_boxes):
            if self.pred_classes[i] in classes and self.pred_scores[i] > threshold:
                color = colors[classes.index(self.pred_classes[i])]
                cv2.rectangle(annotated_frame, (box[1], box[0]), (box[3], box[2]), color, 2)
                annotated_frame = cv2.putText(annotated_frame, self.labels[self.pred_classes[i]], (box[1] + 2, box[0] + 15), cv2.FONT_HERSHEY_SIMPLEX , 0.6, color, 1, cv2.LINE_AA)
                annotated_frame = cv2.putText(annotated_frame, f'score: {self.pred_scores[i]:.2f}', (box[1] + 2, box[0] + 30), cv2.FONT_HERSHEY_SIMPLEX , 0.5, color, 1, cv2.LINE_AA)

        self.img_processed = True
        self.load_image(annotated_frame)

    def on_save_xml_clicked(self, file_path):
        if self.img_processed:
            labels = []
            coordinates = []
            shape = self.un_annotated_frame.shape
            for i, score in enumerate(self.pred_scores):
                box = self.pred_boxes[i]
                if score > self.threshold:
                    labels.append(self.labels[self.pred_classes[i]])
                    coordinates.append(box)

            annotations.generate_xml(labels, coordinates, self.img_dir, self.images[self.img_index], file_path, shape)
        else:
            self.gui.show_error('Click on detect first')

    def set_image_size(self, width, height, gui):
        self.img_width = width
        self.img_height = height
        self.gui = gui

    def __init__(self):
        self.base_working_dir = os.getcwd()
        self.img_dir = None
        self.labels = {}
        self.img_processed = False

        file = open('../coco_labels.txt', 'r')
        content = file.readlines()
        file.close()

        for i, label in enumerate(content):
            self.labels[i + 1] = label[:-1]

        gui = GUI(self)


if __name__ == '__main__':
    handler = Handler()
