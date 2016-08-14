from pprint import pprint

from geotagger import settings
from geotagger.utils import parse_date
from geotagger.packages import exiftool


def parse_metadata(metadata):
    location = None
    if 'EXIF:GPSLatitude' in metadata:
        location = {
            'latitude': metadata['EXIF:GPSLatitude'],
            'longitude': metadata['EXIF:GPSLongitude'],
        }

    return {
        'created': parse_exif_date(metadata['EXIF:CreateDate']),
        'path': metadata['SourceFile'],
        'location': location,
        'orig': metadata,
    }


def get_exif_metadata(paths):
    with exiftool.ExifTool(executable_=settings.EXIFTOOL_EXECUTABLE) as et:
        for path in paths:
            metadata = et.get_metadata(path)
            parsed = parse_metadata(metadata)
            pprint(parsed)
            yield parsed


def parse_exif_date(s):
    """
    "2016:08:05 20:29:26"

    """
    date, time = s.split()
    return parse_date('{}T{}'.format(date.replace(':', '-'), time))


def exiftool_geotag(logfile_path, photos_directory_path):
    """
    http://www.sno.phy.queensu.ca/~phil/exiftool/geotag.html

    """
    args = ['-geotag', logfile_path, photos_directory_path]
    args = [arg.encode('utf8') for arg in args]
    with exiftool.ExifTool(executable_=settings.EXIFTOOL_EXECUTABLE) as et:
        et.execute(*args)
