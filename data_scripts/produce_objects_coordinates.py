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

TRACK_SEGMENT_PDFS = {
    'LQ': '49600_LQ_Landquart_situation_plan.pdf',
    'MALA': '49202_MALA_Malans_situation_plan.pdf',
    'SAGE': '49203_SAGE_Malans_Alte_Saege_situation_plan.pdf',
    'GRUS': '49208_GRUS_Gruesch_situation_plan.pdf',
    'SCRS': '49211_SCRS_Schiers_situation_plan.pdf',
    'FUWI': '49214_FUWI_Fuchswinkel_situation_plan.pdf',
    'JAZ': '49217_JAZ_Jenaz_situation_plan.pdf',
    'FID': '49218_FID_Fideris_situation_plan.pdf',
    'KUEB': '49221_KUEB_Kueblis_situation_plan.pdf',
    'CAPA': '49223_CAPA_Capaels_situation_plan.pdf',
    'SAAS': '49225_SAAS_Saas_situation_plan.pdf',
    'SERN': '49228_SERN_Serneus_situation_plan.pdf',
    'KLOD': '49231_KLOD_Klosters_Dorf_situation_plan.pdf',
    'KLO': '49232_KLO_Klosters_situation_plan.pdf',
}

result = []

with open('objects.json') as devices_json:

    devices = json.load(devices_json)

    def get_id_and_location(relative_position, device_type):
        best_dif = 100
        best_idx = -1
        for idx, device in enumerate(devices):
            device_position = float(device['relativ position'].split()[0])
            if abs(relative_position - device_position) < best_dif \
                    and device_type == device['type']:
                best_dif = relative_position - device_position
                best_idx = idx
        best_id = devices[best_idx]['id']
        return best_id, devices[best_idx]['location abreviation']

    with open('image_relative_position.json') as images_json:
        images = json.load(images_json)
        for image in images:  # Should also check for the last item
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
                        object_id, location_abreviation = get_id_and_location(
                                relative_position, OBJECT_CLASSES[idx])
                        result.append({
                            'id': object_id,
                            'latitude': latitude,
                            'longitude': longitude,
                            'type': OBJECT_CLASSES[idx],
                            'relative_position': relative_position,
                            'pdf_file':
                                TRACK_SEGMENT_PDFS[location_abreviation],
                            'image': image['image'].split('Res/')[1]
                        })
                        with open('feed_results.json', 'w+') as ff:
                            json.dump(result, ff)

