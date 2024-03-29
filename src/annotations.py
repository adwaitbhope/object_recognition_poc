import xml.etree.cElementTree as ET
import xml.dom.minidom
import os

def generate_xml(labels, coordinates, img_dir, img_name, file_path, shape):
    file_dir = os.path.split(file_path)[0]
    file_name = os.path.split(file_path)[1]
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
        ET.SubElement(bndbox, 'xmin').text = str(box[1])
        ET.SubElement(bndbox, 'ymin').text = str(box[0])
        ET.SubElement(bndbox, 'xmax').text = str(box[3])
        ET.SubElement(bndbox, 'ymax').text = str(box[2])

    os.chdir(file_dir)
    tree = ET.ElementTree(annotation)
    tree.write(file_name + '.xml')

    dom = xml.dom.minidom.parse(file_name + '.xml')
    pretty_xml_as_string = dom.toprettyxml()

    file = open(file_name + '.xml', 'w')
    file.write(pretty_xml_as_string)
    file.close()
