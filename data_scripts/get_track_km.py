import os
import glob
import json
import PIL.ExifTags
import PIL.Image as pil
import geopy.distance

root_dir = '/siemens/data/Trackpictures/Trackpictures_HiRes/'
sub_dirs = ['001_-_Landquart_-_Klosters_Platz/',
            '002_-_Klosters_Platz_-_Landquart/']

total_distance = 0
results = {}

for sub_dir in sub_dirs:
    directory_string = root_dir + \
                        sub_dir
    filelist = glob.glob(os.path.join(directory_string, '*'))
    past_coordinates = (-1, -1)

    filelist.sort()
    filelist.pop()

    for infile in filelist:
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
                    (string_longitude[2][0] / string_longitude[2][1]) /
                    60) / 60
            if past_coordinates[0] >= 0:
                distance = geopy.distance.distance((latitude, longitude),
                                                   past_coordinates).km
                if sub_dir == '001_-_Landquart_-_Klosters_Platz/':
                    results[image_name] = distance + total_distance
                    total_distance += distance
                    print(total_distance)
                else:
                    results[image_name] = total_distance - distance
                    total_distance -= distance
            else:
                if sub_dir == '001_-_Landquart_-_Klosters_Platz/':
                    results[image_name] = 0
                else:
                    results[image_name] = total_distance
            past_coordinates = (latitude, longitude)

with open('track_km.json', 'w+') as fp:
    json.dump(results, fp)
