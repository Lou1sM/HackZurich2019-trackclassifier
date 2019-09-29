import json
import os

OBJECT_CLASSES = ['balise', 'distant_signal', 'main_signal']


def clean_name(x):
    x['name'] = './' + x['name']
    return x


with open('COCO.json') as f:
    base_data = json.load(f)
    images = base_data['images']
    annotations = base_data['annotations']
    print(images[0].keys())
    print(annotations[0].keys())
    result = []
    annoted_files = []
    for image in images:
        for annotation in annotations:
            if image['id'] == annotation['image_id']:
                arr = [0, 0, 0, 0]
                arr[annotation['category_id']] = 1
                obj = {
                    'name': './Trackpictures_LoRes/' + image['file_name'],
                    'objects': arr,
                }
                annoted_files.append(obj['name'])
                result.append(obj)

    path = './'
    all_files = []
    for r, d, f in os.walk(path):
        for file in f:
            file_name = os.path.join(r, file)
            if file_name not in annoted_files:
                obj = {
                    'name': file_name,
                    'objects': [0, 0, 0, 0]
                }
                result.append(obj)

    final_result = result
    ANNOTED_FILES = ['annotated_005.json', 'annotated_006.json',
                     'annotated_007.json', 'annotated_008.json',
                     'annotated_009.json', 'annotated_010.json']
    for json_file in ANNOTED_FILES:
        with open(json_file) as jso_file:
            arr = json.load(jso_file)
            arr = list(map(clean_name, arr))
            print(arr)
            final_result = final_result + arr

    final_result = sorted(final_result, key=lambda k: k['name'])
    with open('best_data.json', 'w+') as ff:
        json.dump(final_result, ff)
