import json

OBJECT_CLASSES = ['balise', 'distant_signal', 'main_signal', '']

with open('images.json') as json_file:
    image_data = json.load(json_file)
    with open('track_km.json') as json_file_2:
        track_data = json.load(json_file_2)
        separate_objects = {}
        result = []
        for item in image_data.items():
            for idx, object_class in enumerate(item[1]):
                if object_class == 1:
                    separate_objects[item[0]] = OBJECT_CLASSES[idx]
        for object_item in separate_objects.items():
            for image_item in track_data.items():
                if object_item[0] == image_item[0]:
                    result.append({
                        'image': object_item[0],
                        'object_type': object_item[1],
                        'relative_position': image_item[1],
                        })
        with open('object_relative_position.json', 'w+') as fn:
            json.dump(result, fn)
