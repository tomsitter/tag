from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def geocode(filename):
    image = Image.open(filename)
    info = get_exif_data(image)
    lat, lon = get_lat_lon(info)
    return make_point(lat, lon)

def get_exif_data(image):
    """Returns a dictionary from the exif data of an PIL Image item. Also converts the GPS Tags"""
    exif_data = {}
    info = image._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_data[sub_decoded] = value[t]
                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value
    return exif_data

def _get_if_exist(data, key):
    if key in data:
        return data[key]
    return None

get_float = lambda x: float(x[0]) / float(x[1])
def convert_to_degrees(value):
    d = get_float(value[0])
    m = get_float(value[1])
    s = get_float(value[2])
    return d + (m / 60.0) + (s / 3600.0)

def get_lat_lon(info):
    gps_info = info['GPSInfo']
    gps_latitude = gps_info['GPSLatitude']
    gps_latitude_ref = gps_info['GPSLatitudeRef']
    gps_longitude = gps_info['GPSLongitude']
    gps_longitude_ref = gps_info['GPSLongitudeRef']
    lat = convert_to_degrees(gps_latitude)
    if gps_latitude_ref != "N":
        lat *= -1
    lon = convert_to_degrees(gps_longitude)
    if gps_longitude_ref != "E":
        lon *= -1
    return lat, lon

def make_point(lat, lon):
    return 'POINT ({lat}, {lon})'.format(lat=lat, lon=lon)