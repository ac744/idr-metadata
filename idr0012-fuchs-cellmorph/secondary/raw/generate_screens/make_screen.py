#!/usr/bin/env python

import sys
import os
from argparse import ArgumentParser

from pyidr.screenio import ScreenWriter

ROWS = 16
COLUMNS = 24
FIELDS = 1
EXTRA_KV = {"Dimensions": "ZCT"}


def parse_cl(argv):
    parser = ArgumentParser()
    parser.add_argument("dir", metavar="DIR", help="dir")
    parser.add_argument("-o", "--output", metavar="FILE", help="output file")
    parser.add_argument("-p", "--plate", metavar="PLATE", help="plate name")
    return parser.parse_args(argv[1:])


def write_screen(data_dir, plate, outf):
    writer = ScreenWriter(plate, ROWS, COLUMNS, FIELDS)
    for idx in xrange(ROWS * COLUMNS):
        r, c = writer.coordinates(idx)
        well_tag = "Well %s%03d" % (r, c)
        subdir = os.path.join(data_dir, well_tag)
        field_values = []
        if not os.path.isdir(subdir):
            sys.stderr.write("missing: %s\n" % subdir)
        else:
            pattern = "<FITC,Hoechst,Tritc>_Flo - n000000.tif"
            field_values.append(os.path.join(subdir, pattern))
        writer.add_well(field_values, extra_kv=EXTRA_KV)
    writer.write(outf)


def main(argv):
    args = parse_cl(argv)
    if args.output:
        outf = open(args.output, "w")
    else:
        outf = sys.stdout
    write_screen(args.dir, args.plate, outf)
    if outf is not sys.stdout:
        outf.close()


if __name__ == "__main__":
    main(sys.argv)
