# This code is public domain.

import json

data = {}
images = {}


def imagename_to_id(name):
    return list(filter(lambda img: img['file_name'] == name, data['images']))[0]['id']


def load(filename='COCO.json'):
    """Load the given JSON file."""
    global data, images
    with open(filename) as input:
        data = json.load(input)
        images = {img['id']: img for img in data['images']}
        return data, images


def get_images():
    """Return all images."""
    return data['images']


def get_annotations(image=None):
    """Return the annotations for the given image or all annotations if no argument or a falsy argument is given."""
    if not image:
        return data['annotations']
    img_id = imagename_to_id(image)
    return list(filter(lambda a: a['image_id'] == img_id, data['annotations']))


def get_with(object_type=None):
    """
    Return the files that are annotated with the given object class ('balise', 'main_signal' oder 'distant_signal').
    If no argument or a falsy argument is given, returns all files that have at least one annotation.
    """
    if not object_type:
        with_annots = set(map(lambda a: a['image_id'], data['annotations']))
        return [images[id]['file_name'] for id in with_annots]
    cat_id = [cat['id'] for cat in filter(lambda cat: cat['name'] == object_type, data['categories'])][0]
    annots = filter(lambda annot: annot['category_id'] == cat_id, data['annotations'])
    return list(map(lambda annot: images[annot['image_id']]['file_name'], annots))


if __name__ == '__main__':
    """Load the input file, invoke get_with() and print the result."""
    load('COCO.json')
    print(get_with())
