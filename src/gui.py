from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QButtonGroup, QAbstractButton, QMessageBox
from PyQt5.QtWidgets import  QRadioButton, QCheckBox, QDoubleSpinBox, QFrame, QPushButton, QInputDialog, QLineEdit, QFileDialog, QErrorMessage
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap, QImage
import os

class GUI:

    def show_error(self, error):
        QMessageBox.warning(self.main_widget, 'Error', error, QMessageBox.Close)

    def load_image(self, frame=None):
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        self.image.setPixmap(QPixmap(QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)))

    def set_model(self, model_code):
        self.model = self.models[model_code]

    def on_button_clicked(self, id):
        if id == 0:
            self.handler.on_prev_clicked()
        elif id == 1:
            self.handler.on_next_clicked()
        elif id == 2:
            classes = []
            colors = []
            for button in self.check_boxes:
                if button.isChecked():
                    classes.extend(self.labels[button.text()][0])
                    for i in self.labels[button.text()][0]:
                        colors.append(self.labels[button.text()][1])

            if self.model is None:
                self.show_error('Model not selected')
                return

            if len(classes) == 0:
                self.show_error('No classes selected')
                return

            self.handler.on_detect_clicked(self.model, self.threshold.value(), classes, colors)
        elif id == 3:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            file_path, _ = QFileDialog.getSaveFileName(self.main_widget, 'Select location to save', '', 'XML (*.xml)', options=options)
            self.handler.on_save_xml_clicked(file_path)

    def init_select_model_window(self):
        heading = QLabel()
        heading.setText('Model')
        heading.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        ssd_inception = QRadioButton('SSD Inception V2')
        ssd_inception.clicked.connect(lambda: self.set_model(0))
        ssd_mobile_net = QRadioButton('SSD MobileNet V2')
        ssd_mobile_net.clicked.connect(lambda: self.set_model(1))
        faster_rcnn = QRadioButton('Faster RCNN Inception V2')
        faster_rcnn.clicked.connect(lambda: self.set_model(2))

        ssd_inception.setChecked(True)
        self.set_model(0)

        button_group = QButtonGroup()
        button_group.addButton(ssd_inception)
        button_group.addButton(ssd_mobile_net)
        button_group.addButton(faster_rcnn)

        vbox = QVBoxLayout()
        vbox.addWidget(heading)
        vbox.addWidget(ssd_inception)
        vbox.addWidget(ssd_mobile_net)
        vbox.addWidget(faster_rcnn)

        main_widget = QWidget()
        main_widget.setLayout(vbox)
        return main_widget

    def init_threshold_window(self):
        heading = QLabel()
        heading.setText('Theshold: ')

        self.threshold = QDoubleSpinBox()
        self.threshold.setMaximum(1.0)
        self.threshold.setSingleStep(0.05)
        self.threshold.setProperty("value", 0.7)

        hbox = QHBoxLayout()
        hbox.addWidget(heading)
        hbox.addWidget(self.threshold)

        main_widget = QWidget()
        main_widget.setLayout(hbox)
        return main_widget

    def init_label_filters(self):
        heading = QLabel()
        heading.setText('Label Filter')
        heading.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        vbox = QVBoxLayout()
        vbox.addWidget(heading)

        self.labels = {}
        self.labels['Person'] = ([1], (0, 0, 0))
        self.labels['Vehicles'] = ([2, 3, 4, 6, 7, 8], (255, 255, 255))
        self.labels['Animals'] = ([i for i in range(16, 26)], (255, 0, 0))
        self.labels['Fruits'] = ([i for i in range(52, 62)], (0, 255, 0))
        self.labels['Electronics'] = ([i for i in range(72, 78)], (0, 0, 255))
        self.labels['Furniture'] = ([i for i in range(62, 72)], (255, 255, 0))
        self.labels['Shoe'] = ([29], (0, 255, 255))
        self.labels['Eye Glasses'] = ([30], (255, 0, 255))
        self.labels['Handbag'] = ([31], (192, 192, 192))
        self.labels['Bottle'] = ([44], (128, 128, 128))
        self.labels['Plate'] = ([45], (128,0, 0))
        self.labels['Cup'] = ([47], (0, 128, 0))
        self.labels['Bowl'] = ([51], (127, 255, 212))

        self.check_boxes = []
        for i, label in enumerate(self.labels):
            check_box = QCheckBox(label)
            vbox.addWidget(check_box)
            self.check_boxes.append(check_box)

        main_widget = QWidget()
        main_widget.setLayout(vbox)
        return main_widget

    def init_side_panel(self):
        line_1 = QFrame()
        line_1.setFrameShape(QFrame.HLine)
        line_1.setFrameShadow(QFrame.Sunken)

        line_2 = QFrame()
        line_2.setFrameShape(QFrame.HLine)
        line_2.setFrameShadow(QFrame.Sunken)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.init_select_model_window())
        vbox.addStretch(1)
        vbox.addWidget(line_1)
        vbox.addWidget(self.init_threshold_window())
        vbox.addWidget(line_2)
        vbox.addStretch(1)
        vbox.addWidget(self.init_label_filters())
        vbox.addStretch(1)

        main_widget = QWidget()
        main_widget.setLayout(vbox)
        main_widget.resize(QSize(0.35 * self.scale_factor * self.screen_width, main_widget.height()))
        return main_widget

    def init_top_bar(self):
        dir_path = QLabel('')

        def pick_dir_window():
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog

            dir = QFileDialog.getExistingDirectory(self.main_widget, 'Select a folder:', '', options)
            if dir:
                dir_path.setText(os.path.join(dir, ''))
                self.handler.on_dir_selected(os.path.join(dir, ''))

        pick_dir = QPushButton('Select folder')
        pick_dir.clicked.connect(pick_dir_window)

        hbox = QHBoxLayout()
        hbox.addWidget(pick_dir)
        hbox.addStretch(1)
        hbox.addWidget(dir_path)

        main_widget = QWidget()
        main_widget.setLayout(hbox)
        return main_widget

    def init_image_window(self):
        self.image = QLabel()
        self.image.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        hbox = QHBoxLayout()
        hbox.addWidget(self.image)

        main_widget = QWidget()
        main_widget.setLayout(hbox)
        return main_widget

    def init_bottom_bar(self):
        prev_button = QPushButton('Previous')
        prev_button.clicked.connect(lambda: self.on_button_clicked(0))

        next_button = QPushButton('Next')
        next_button.clicked.connect(lambda: self.on_button_clicked(1))

        detect_button = QPushButton('Detect')
        detect_button.clicked.connect(lambda: self.on_button_clicked(2))

        save_xml_button = QPushButton('Save annotations as XML')
        save_xml_button.clicked.connect(lambda: self.on_button_clicked(3))

        hbox = QHBoxLayout()
        hbox.addWidget(prev_button)
        hbox.addWidget(next_button)
        hbox.addStretch(1)
        hbox.addWidget(detect_button)
        hbox.addStretch(1)
        hbox.addWidget(save_xml_button)

        main_widget = QWidget()
        main_widget.setLayout(hbox)
        return main_widget

    def init_main_panel(self):
        line_1 = QFrame()
        line_1.setFrameShape(QFrame.HLine)
        line_1.setFrameShadow(QFrame.Sunken)

        line_2 = QFrame()
        line_2.setFrameShape(QFrame.HLine)
        line_2.setFrameShadow(QFrame.Sunken)

        vbox = QGridLayout()
        vbox.addWidget(self.init_top_bar(), 0, 0)
        vbox.addWidget(line_1, 1, 0)
        vbox.addWidget(self.init_image_window(), 2, 0, 9, 1)
        vbox.addWidget(line_2, 10, 0)
        vbox.addWidget(self.init_bottom_bar(), 11, 0)

        main_widget = QWidget()
        main_widget.setLayout(vbox)
        return main_widget

    def __init__(self, handler):
        self.model = None
        self.classes = []
        self.models = ['ssd_inception_v2_coco_2018_01_28', 'ssd_mobilenet_v2_coco_2018_03_29', 'faster_rcnn_inception_v2_coco_2018_01_28']

        self.handler = handler
        app = QApplication([])

        screen_resolution = app.desktop().screenGeometry()
        self.screen_width, self.screen_height = screen_resolution.width(), screen_resolution.height()
        self.scale_factor = 0.5
        img_width, img_height = self.scale_factor * self.screen_width, self.scale_factor * self.screen_height
        self.handler.set_image_size(img_width, img_height, self)

        self.main_widget = QWidget()
        self.main_widget.setGeometry(0.2 * self.screen_width, 0.2 * self.screen_height, img_width, img_height)
        self.main_widget.setWindowTitle('Image Detector\t')

        hbox = QGridLayout()
        hbox.addWidget(self.init_side_panel(), 0, 0, 1, 1)
        hbox.addWidget(self.init_main_panel(), 0, 1, 1, 5)

        self.main_widget.setLayout(hbox)
        self.main_widget.show()
        app.exec_()
