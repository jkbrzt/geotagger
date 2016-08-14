import mimetypes
import os

import arrow
import dateutil.parser


def parse_date(s):
    return arrow.get(dateutil.parser.parse(s))


def get_image_file_paths(photo_directory_path):
    image_file_paths = set()
    for root, subdirs, files in os.walk(photo_directory_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            mime, encoding = mimetypes.guess_type(file_path)
            if ((mime and 'image' in mime)
                    or file_path.lower().endswith('.dng')):
                    image_file_paths.add(file_path)
    return image_file_paths
