#!/usr/bin/python2
# -*-Python-*-

# import cam
import json
import os
import sys

def main():
    for photo in find_photos(sys.argv[1:]):
        print photo

def find_photos(root_paths):
    for root_path in root_paths:
        for root, dirs, files in os.walk(root_path):
            for file_name in files:
                photo_file_name = build_photo_file_name(root, file_name)
                if(photo_file_name is None):
                    continue

                with open(os.path.join(root, file_name), 'r') as f:
                    metadata = json.load(f)
                    metadata['$fileName'] = photo_file_name

                    yield metadata

def build_photo_file_name(root, metadata_file_name):
    if(metadata_file_name == 'Metadaten.json'):
        return None

    metadata_file_suffix = '.json'

    if(not metadata_file_name.endswith(metadata_file_suffix)):
        return None

    base_name = metadata_file_name[:-len(metadata_file_suffix)]
    
    base_path = os.path.join(root, base_name)
    if(os.path.isfile(base_path)):
        return base_path

    for img_suffix in ['jpg', 'jpeg', 'png']:
        base_path = os.path.join(root, '%s.%s' % (base_name, img_suffix))
        if(os.path.isfile(base_path)):
            return base_path

    print 'WARNING Could not find image for metadata %s' % (os.path.join(root, metadata_file_name), )

    return None

main()
