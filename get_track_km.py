import os
import glob
import json
import PIL.ExifTags
import PIL.Image as pil
import geopy.distance

root_dir = '/siemens/data/Trackpictures/Trackpictures_HiRes/'
count = 1

for _, dirs, _, in os.walk(root_dir):
    for sub_dir in dirs:
        directory_string = '/siemens/data/Trackpictures/Trackpictures_HiRes/' + \
                            sub_dir
        past_coordinates = (-1, -1)

        print(directory_string)
        total_distance = 0
        results = {}

        filelist = glob.glob(os.path.join(directory_string, '*'))
        for infile in sorted(filelist):
            image_name = str(infile)
            if image_name.endswith(".JPG"):
                img = pil.open(image_name)
                exif = {
                  PIL.ExifTags.TAGS[k]: v
                  for k, v in img._getexif().items()
                  if k in PIL.ExifTags.TAGS
                }
                gps_info = exif['GPSInfo']
                string_latitude = gps_info[2]
                string_longitude = gps_info[4]
                latitude = string_latitude[0][0] / string_latitude[0][1] + \
                    (string_latitude[1][0] / string_latitude[1][1] +
                        (string_latitude[2][0] / string_latitude[2][1]) / 60) / 60
                longitude = string_longitude[0][0] / string_longitude[0][1] + \
                    (string_longitude[1][0] / string_longitude[1][1] +
                        (string_longitude[2][0] / string_longitude[2][1]) / 60) / 60

                if past_coordinates[0] >= 0:
                    distance = geopy.distance.distance((latitude, longitude),
                                                       past_coordinates).km
                    results[image_name] = distance + total_distance
                    total_distance += distance
                else:
                    results[image_name] = 0
                past_coordinates = (latitude, longitude)

        with open('track_km +' + str(count) + '.json', 'w+') as fp:
            json.dump(results, fp)
        count = count + 1
