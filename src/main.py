import streamlit as st
import os
import urllib
import tarfile
import cv2
import annotations
from config import config
from object_detector import DetectorAPI

THRESHOLD_DEFAULT = 0.7

def download_model(model_url, download_path):
    weights_warning, progress_bar = None, None
    try:
        weights_warning = st.sidebar.warning("Downloading %s..." % os.path.split(download_path)[-1])
        progress_bar = st.sidebar.progress(0)
        with open(download_path, "wb") as output_file:
            with urllib.request.urlopen(model_url) as response:
                length = int(response.info()["Content-Length"])
                counter = 0.0
                MEGABYTES = 2.0 ** 20.0
                while True:
                    data = response.read(8192)
                    if not data:
                        break
                    counter += len(data)
                    output_file.write(data)

                    weights_warning.warning("Downloading %s... (%6.2f/%6.2f MB)" %
                        (os.path.split(download_path)[-1], counter / MEGABYTES, length / MEGABYTES))
                    progress_bar.progress(min(counter / length, 1.0))

    finally:
        if weights_warning is not None:
            weights_warning.empty()
        if progress_bar is not None:
            progress_bar.empty()

        tar = tarfile.open(download_path, "r:gz")
        tar = tar.extractall(os.path.split(download_path)[0])
        os.remove(download_path)


def get_model():
    model_names = [model['name'] for model in config.MODELS]
    selected_model = st.sidebar.selectbox('Select model for inference', model_names)

    parent_dir = os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))
    models_dir = os.path.join(parent_dir, 'models')

    model_url = config.MODELS[model_names.index(selected_model)]['url']
    model_file_name = os.path.split(model_url)[-1]
    model_dir = os.path.join(models_dir, model_file_name.split('.')[0])
    inference_file_path = os.path.join(model_dir, 'frozen_inference_graph.pb')

    if os.path.exists(inference_file_path):
        st.sidebar.text('Model is available')
        return inference_file_path
    else:
        if st.sidebar.button('Download model'):
            download_path = os.path.join(models_dir, model_file_name)
            download_model(model_url, download_path)

            if os.path.exists(inference_file_path):
                st.sidebar.text('Downloaded successfully')
                return inference_file_path
            else:
                st.sidebar.text(f'Download error, \'{os.path.join(model_file_name.split(".")[0], "frozen_inference_graph.pb")}\' not found.')

    return None


def get_threshold():
    threshold = st.sidebar.slider('Select threshold', min_value=0.0, max_value=1.0, value=THRESHOLD_DEFAULT, step=0.05)
    return threshold


def get_label_ids():
    categories = [category for category in config.LABEL_CATEGORIES]
    selected_categories = st.sidebar.multiselect('Select label categories', categories)
    label_ids = [label for category in selected_categories for label in config.LABEL_CATEGORIES[category]['labels']]
    return label_ids


def get_color_for_label_id(label_id):
    for category in config.LABEL_CATEGORIES:
        if label_id in config.LABEL_CATEGORIES[category]['labels']:
            return config.LABEL_CATEGORIES[category]['color']


def get_coco_labels():
    labels_file_path = os.path.join(config.CONFIG_DIR, 'coco_labels.txt')
    file = open(labels_file_path, 'r')
    coco_labels = file.read().splitlines()
    file.close()
    return coco_labels


def run_inference(image, image_gui, model, threshold, selected_label_ids):
    coco_labels = get_coco_labels()

    odapi = DetectorAPI(model)
    pred_boxes, pred_scores, pred_label_ids, _ = odapi.process_frame(image)
    annotation_boxes, annotation_scores, annotation_labels = [], [], []

    for box, score, label_id in zip(pred_boxes, pred_scores, pred_label_ids):
        if label_id in selected_label_ids and score > threshold:
            color = get_color_for_label_id(label_id)
            cv2.rectangle(image, (box[1], box[0]), (box[3], box[2]), color, 2)

            image = cv2.putText(image, coco_labels[label_id - 1], (box[1] + 2, box[0] + 15), cv2.FONT_HERSHEY_SIMPLEX , 0.6, color, 1, cv2.LINE_AA)
            image = cv2.putText(image, f'score: {score:.2f}', (box[1] + 2, box[0] + 30), cv2.FONT_HERSHEY_SIMPLEX , 0.5, color, 1, cv2.LINE_AA)

            annotation_boxes.append(box)
            annotation_scores.append(score)
            annotation_labels.append(coco_labels[label_id - 1])

    image_gui.image(image, use_column_width=True)
    return annotation_boxes, annotation_scores, annotation_labels


def navigate_image_to(position):
    if position == 'init':
        name = 'car and pedestrian.jpg'

    if position == 'next':
        name = 'IMG_20180601_143714.jpg'

    image = cv2.imread(os.path.join(config.IMAGE_DIR, name))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    image_dict = {'image': image}
    image_dict['name'] = name
    return image_dict


def get_image():
    image_dict = None

    # To do: insert next and prev buttons
    # next = st.button('Next')
    # prev = st.button('Prev')

    # if next:
    #     image_dict = navigate_image_to('next')
    #
    # if prev:
    #     image_dict = navigate_image_to('prev')

    if image_dict is None:
        image_dict = navigate_image_to('init')

    image_gui = st.empty()
    image_gui.image(image_dict['image'], use_column_width=True)
    return image_dict, image_gui


def generate_xml(image_dict, boxes, scores, labels, threshold):
    shape = image_dict['image'].shape
    coordinates = [box for box, score in zip(boxes, scores) if score > threshold]
    annotations.generate_xml(labels, coordinates, config.IMAGE_DIR, image_dict['name'], config.ANNOTATIONS_DIR, shape)


def main():
    resolute_logo_path = os.path.join(config.CONFIG_DIR, 'logo_extended.png')
    st.image(resolute_logo_path, use_column_width=True, format='PNG')
    st.markdown("<h1 style='text-align: center;'>Auto Annotation Tool</h1>", unsafe_allow_html=True)

    st.sidebar.title('Settings')

    model = get_model()
    if not model:
        return

    threshold = get_threshold()
    label_ids = get_label_ids()
    image_dict, image_gui = get_image()

    boxes, scores, labels = None, None, None
    detect = st.button('Detect and save XML')

    if detect:
        boxes, scores, labels = run_inference(image_dict['image'], image_gui, model, threshold, label_ids)
        generate_xml(image_dict, boxes, scores, labels, threshold)


if __name__ == '__main__':
    main()
