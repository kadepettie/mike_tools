#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Rename mp3s as '[track] [name].mp3'.

============================================================================

        AUTHOR: Michael D Dacre, mike.dacre@gmail.com
       CREATED: 2016-37-17 16:02
 Last modified: 2016-08-19 15:39

============================================================================
"""
import os
import sys
import argparse
import mutagen.mp3
import re


def rename_files(files, directory='', folders=False):
    """Rename files using mp3 tags.

    :files:     List of files to run on
    :directory: Put music into this directory
    :folders:   Arrange music into Artist/Album folders (does not overwrite)
    :returns:   0 on success

    """
    if directory:
        directory = os.path.abspath(os.path.expandvars(directory))
        if os.path.exists(directory) and not os.path.isdir(directory):
            raise Exception("{} is not a directory".format(directory))
        if not os.path.isdir(directory):
            os.makedirs(directory)
    else:
        directory = os.path.abspath(os.path.expandvars('.'))
    for fl in files:
        metadata = mutagen.mp3.Open(fl)
        try:
            artist = metadata['TPE1']
        except KeyError:
            artist = metadata['TPE2']
        album = metadata['TALB']
        if folders:
            root_path = os.path.join(directory,
                                str(artist),
                                str(album))
            if not os.path.isdir(root_path):
                os.makedirs(root_path)
        else:
            root_path = directory
        new_name = os.path.join(
            root_path, '{0:0>2} {1}.mp3'.format(
                str(metadata['TRCK']).split('/')[0],
                re.sub(r'/', r'_', str(metadata['TIT2']))
            )
        )
        os.rename(fl, new_name)


def main(argv=None):
    """Run as a script."""
    if not argv:
        argv = sys.argv[1:]

    parser  = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('files', nargs='+',
                        help="Input files")

    parser.add_argument('-f', '--folders', action="store_true",
                        help="Create Artist/Album folders")
    parser.add_argument('-d', '--directory',
                        help="Put music into this root directory.")

    args = parser.parse_args(argv)

    rename_files(args.files, args.directory, args.folders)

if __name__ == '__main__' and '__file__' in globals():
    sys.exit(main())
