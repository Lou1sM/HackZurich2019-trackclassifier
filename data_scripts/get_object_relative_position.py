import json

OBJECT_CLASSES = ['balise', 'distant_signal', 'main_signal', '']

with open('images.json') as json_file:
    image_data = json.load(json_file)
    with open('track_km.json') as json_file_2:
        track_data = json.load(json_file_2)
        result = []
        for track in track_data:
            for image_item in image_data.items():
                if track['image'] == image_item[0]:
                    result.append({
                        'image': image_item[0],
                        'objects': image_item[1],
                        'relative_position': track['relative_position'],
                        'coordinates': track['coordinates']
                        })
        with open('image_relative_position.json', 'w+') as fn:
            json.dump(result, fn)
