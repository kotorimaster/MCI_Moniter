#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" \example read_recording.py
This is as example of how to set up the DataReader to read back a previously
recorded session.
"""

from __future__ import print_function
from pymoduleconnector import DataReader
from pymoduleconnector import DataRecord
from pymoduleconnector import DataType

from optparse import OptionParser
from datetime import datetime

import sys

def process(record):
    if record.is_user_header:
        print("read custom user header of type: {}, size: {}".format(record.data_type, record.data.size()))
        return

    print("read data of type: {}, size: {}".format(record.data_type, record.data.size()))
    if record.data_type == DataType.BasebandApDataType:
        print("process baseband ap data")
    elif record.data_type == DataType.SleepDataType:
        print("process sleep data")
    elif record.data_type == DataType.RespirationDataType:
        print("process respiration data")


def read_recording(meta_filename, depth):
##! [Typical usage]
    print("read recording: {}, depth: {}".format(meta_filename, depth))
    reader = DataReader()

    if reader.open(meta_filename, depth) != 0:
        print("ERROR: failed to open meta file: {}".format(meta_filename))
        sys.exit(1)

    while not reader.at_end():
        record = reader.read_record()
        if not record.is_valid:
            print("ERROR: failed to read data record")
            sys.exit(1)
        process(record)
##! [Typical usage]

    print("-----------------------------------------------------")
    start_epoch = reader.get_start_epoch() / 1000.0 # convert from ms to seconds
    print("start time: {}".format(datetime.fromtimestamp(start_epoch).strftime('%Y-%m-%d %H:%M:%S.%f')))
    print("duration:   {} ms".format(reader.get_duration()))
    print("size:       {} bytes".format(reader.get_size()))
    print("session id: {}".format(reader.get_session_id()))
    print("-----------------------------------------------------")


def main():
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="meta_filename", metavar="FILE",\
                      help="meta file from recording")
    parser.add_option("--depth", dest="depth", metavar="NUMBER", type="int", default=-1,\
                      help="number of meta files to read in chained mode")

    (options, args) = parser.parse_args()
    if not options.meta_filename:
        print("Please specify a meta file to read (use -f <file> or --file <file>)")
        sys.exit(1)

    read_recording(options.meta_filename, options.depth)

if __name__ == "__main__":
    main()
