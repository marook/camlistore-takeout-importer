#!/usr/bin/python2
# -*-Python-*-

import cam
import json
import os
import re
import sys

def main():
    # properties I used: description, title, url, geoInfo.longitude_, geoInfo.latitude_
    for photo in find_photos(sys.argv[1:]):
        photoPath = photo['$photoPath']
        description = photo['description']
        title = photo['title']
        url = photo['url']

        geoInfo = photo['geoInfo']
        lng = None if geoInfo is None else geoInfo['longitude_']
        lat = None if geoInfo is None else geoInfo['latitude_']

        blobRefs = cam.camput('file', '--permanode', photoPath)
        blobRef = blobRefs[0]
        claimRef = blobRefs[1]
        permanodeRef = blobRefs[2]

        if(not description is None):
            cam.camput('attr', permanodeRef, 'description', description)
        if(not title is None):
            cam.camput('attr', permanodeRef, 'title', title)
        cam.camput('attr', permanodeRef, 'srcUrl', url)

        if(not lng is None and not lat is None):
            cam.camput('attr', permanodeRef, 'latitude', '%s' % (lat,))
            cam.camput('attr', permanodeRef, 'longitude', '%s' % (lng,))

        os.remove(photo['$metadataPath'])
        os.remove(photo['$photoPath'])

def find_photos(root_paths):
    for root_path in root_paths:
        for root, dirs, files in os.walk(root_path):
            for file_name in files:
                photo_file_name = build_photo_file_name(root, file_name)
                if(photo_file_name is None):
                    continue

                metadata_path = os.path.join(root, file_name)
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
                    metadata['$metadataPath'] = metadata_path
                    metadata['$photoPath'] = photo_file_name

                    yield metadata

DIR_METADATA_PATTERN = re.compile('^Metadaten(\([0-9]+\))?\.json$')
NUMBER_SUFFIX_PATTERN = re.compile('^(.*)([.](?:jpg|png|jpeg|gif))([(][0-9]+[)])$')

def build_photo_file_name(root, metadata_file_name):
    if(DIR_METADATA_PATTERN.match(metadata_file_name)):
        return None

    metadata_file_suffix = '.json'

    if(not metadata_file_name.endswith(metadata_file_suffix)):
        return None

    base_name = metadata_file_name[:-len(metadata_file_suffix)]
    
    base_path = os.path.join(root, base_name)
    if(os.path.isfile(base_path)):
        return base_path

    for img_suffix in ['jpg', 'jpeg', 'png', 'gif']:
        base_path = os.path.join(root, '%s.%s' % (base_name, img_suffix))
        if(os.path.isfile(base_path)):
            return base_path

    m = NUMBER_SUFFIX_PATTERN.match(base_name)
    if(m):
        photo_path = os.path.join(root, '%s%s%s' % (m.group(1), m.group(3), m.group(2)))
        if(os.path.isfile(photo_path)):
            return photo_path

    print 'WARNING Could not find image for metadata %s' % (os.path.join(root, metadata_file_name), )

    return None

main()
