import json

GLOBAL_TMP_AVERAGES = [
    {  # Balise
        'coord_tmp_average': [0, 0],
        'relative_position_average': 0,
        'elements': 0,
    },
    {  # Distant Signal
        'coord_tmp_average': [0, 0],
        'relative_position_average': 0,
        'elements': 0,
    },
    {  # Main Signal
        'coord_tmp_average': [0, 0],
        'relative_position_average': 0,
        'elements': 0,
    }
]

OBJECT_CLASSES = ['balise', 'distant signal', 'main signal']

result = []

with open('objects.json') as devices_json:

    devices = json.load(devices_json)

    def get_id(relative_position, device_type):
        best_dif = 100
        best_idx = -1
        for idx, device in enumerate(devices):
            device_position = float(device['relativ position'].split()[0])
            if abs(relative_position - device_position) < best_dif \
                    and device_type == device['type']:
                best_dif = relative_position - device_position
                best_idx = idx
        best_id = devices[best_idx]['id']
        return best_id

    with open('image_relative_position.json') as images_json:
        images = json.load(images_json)
        for image in images:  # Should also check for the last item
            print(image)
            coordinates = image['coordinates']
            for idx, is_object_present in enumerate(image['objects']):
                if idx != 3:
                    coord_avg = GLOBAL_TMP_AVERAGES[idx]['coord_tmp_average']
                    rel_avg = \
                        GLOBAL_TMP_AVERAGES[idx]['relative_position_average']
                    if idx != 3 and is_object_present:
                        GLOBAL_TMP_AVERAGES[idx]['elements'] += 1
                        GLOBAL_TMP_AVERAGES[idx]['coord_tmp_average'] = \
                            [coord_avg[0] + coordinates[0], coord_avg[1] +
                                coordinates[1]]
                        GLOBAL_TMP_AVERAGES[idx]['relative_position_average'] \
                            = rel_avg + image['relative_position']
                    elif idx != 3 and (is_object_present == 0 or idx ==
                                       len(image['objects']) - 1) and \
                            coord_avg[0] != 0:
                        latitude = coord_avg[0] / \
                            GLOBAL_TMP_AVERAGES[idx]['elements']
                        longitude = coord_avg[1] / \
                            GLOBAL_TMP_AVERAGES[idx]['elements']
                        relative_position = rel_avg / \
                            GLOBAL_TMP_AVERAGES[idx]['elements']
                        GLOBAL_TMP_AVERAGES[idx] = {
                            'coord_tmp_average': [0, 0],
                            'elements': 0,
                            'relative_position_average': 0
                        }
                        result.append({
                            'id': get_id(relative_position,
                                         OBJECT_CLASSES[idx]),
                            'latitude': latitude,
                            'longitude': longitude,
                            'type': OBJECT_CLASSES[idx],
                            'relative_position': relative_position
                        })
                        with open('feed_results.json', 'w+') as ff:
                            json.dump(result, ff)

