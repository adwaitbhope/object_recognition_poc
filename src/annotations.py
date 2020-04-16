import xml.etree.cElementTree as ET
import xml.dom.minidom
import os

def generate_xml(labels, coordinates, img_dir, img_name, annotations_dir, shape):
    width, height, depth = shape[1], shape[0], shape[2]

    annotation = ET.Element('annotation')
    ET.SubElement(annotation, 'folder').text = img_dir
    ET.SubElement(annotation, 'filename').text = img_name
    ET.SubElement(annotation, 'path').text = img_dir + img_name

    source = ET.SubElement(annotation, 'source')
    ET.SubElement(source, 'database').text = 'Unknown'

    size = ET.SubElement(annotation, 'size')
    ET.SubElement(size, 'width').text = str(width)
    ET.SubElement(size, 'height').text = str(height)
    ET.SubElement(size, 'depth').text = str(depth)

    ET.SubElement(annotation, 'segmented').text = '0'

    for i, box in enumerate(coordinates):
        object = ET.SubElement(annotation, 'object')
        ET.SubElement(object, 'name').text = labels[i]
        ET.SubElement(object, 'pose').text = 'Unspecified'
        ET.SubElement(object, 'truncated').text = '0'
        ET.SubElement(object, 'difficult').text = '0'

        bndbox = ET.SubElement(object, 'bndbox')
        ET.SubElement(bndbox, 'xmin').text = str(box[0])
        ET.SubElement(bndbox, 'ymin').text = str(box[1])
        ET.SubElement(bndbox, 'xmax').text = str(box[2])
        ET.SubElement(bndbox, 'ymax').text = str(box[3])

    img_name_without_ext = os.path.splitext(img_name)[0]
    annotations_file_path = os.path.join(annotations_dir, img_name_without_ext + '.xml')

    tree = ET.ElementTree(annotation)
    tree.write(annotations_file_path)

    dom = xml.dom.minidom.parse(annotations_file_path)
    pretty_xml_as_string = dom.toprettyxml()

    file = open(annotations_file_path, 'w')
    file.write(pretty_xml_as_string)
    file.close()
