#!/usr/bin/env python
# -*- coding: utf-8 -*-

# # # # #
# Controller Area Network debugger
# # #
# Reads data from files filled with CAN data dump in specific format (see docs)
# and allows manipulation with the data (several types)
# # # # #

import sys
import getopt  # reading command line
import re
import csv
from datetime import datetime
from src.data_structure import CANNode, CANTestCase
from src.data_diff import CANDiff


def get_diff_data_str(src_tc, trg_tc, addr, outputgrp):
    """Also simple
    """
    (src_diff, trg_diff) = CANDiff().get_diff_data(
        src_tc, trg_tc, addr)
    string = ''
    if src_diff is not None:
        string += "\n--- SOURCE: {0} ---\n".format(src_diff.addr)
        for src_data in src_diff.data:
            string += "{0}\n".format(src_data)
    else:
        string += "\n--- SOURCE: NONE ---\n"

    if trg_diff is not None:
        string += "\n--- TARGET: {0} ---\n".format(trg_diff.addr)
        for trg_data in trg_diff.data:
            string += "{0}\n".format(trg_data)
    else:
        string += "\n--- TARGET: NONE ---\n"

    return string


def get_diffs_data_str(src_tc, trg_tc, outputgrp):
    """A simple wrap up for receiving basic diffs
    Args:
        src_tc: source test case
        trg_tc: target test case
    Returns:
        formatted string of diff data
    """
    diff_addrs = CANDiff().get_diff_addrs(src_tc, trg_tc)
    string = ''
    for addr in diff_addrs:
        string += get_diff_data_str(src_tc, trg_tc, addr, outputgrp)

    return string


def get_diff_data_csv(src_tc, trg_tc, outputgrp):
    """A little less simple wrap up for receiving basic diffs for csv
    Args:
        src_tc: source test case
        trg_tc: target test case
    Returns:
        formatted array for csv writer
    """
    data = CANDiff().get_diffs_data(src_tc, trg_tc)
    data_list = [[src_tc.filename, trg_tc.filename, "Address", "Data", "Count", "Time"]]
    for src_diff, trg_diff in data:
        if src_diff is not None:
            last_data = src_diff.data[0].data
            last_data_count = 1
            for src_data in src_diff.data:
                if src_data.data == last_data:
                    last_data_count += 1
                else:
                    data_list.append(["Yes", "No", src_diff.addr,
                                  src_data.data, last_data_count, src_data.time])
                    last_data_count = 1
                    last_data = src_data.data
        else:
            data_list.append(["Yes", "No", "None", "None", "None", "None"])

        if trg_diff is not None:
            last_data = trg_diff.data[0].data
            last_data_count = 1
            for trg_data in trg_diff.data:
                if trg_data.data == last_data:
                    last_data_count += 1
                else:
                    data_list.append(["No", "Yes", trg_diff.addr,
                                  trg_data.data, last_data_count, trg_data.time])
                    last_data_count = 1
                    last_data = trg_data.data
        else:
            # normally should not happen, as trg is compared, not source
            data_list.append(["No", "Yes", "None", "None", "None", "None"])
    return data_list


def save_as_text(f, src_tc, trg_tc, outputgrp):
    f.write("Addresses that differ:\n")
    f.write(str(diff_addrs) + "\n")
    f.write(get_diffs_data_str(src_tc, trg_tc, outputgrp))


def save_as_csv(f, src_tc, trg_tc, outputgrp):
    writer = csv.writer(f)
    writer.writerows(get_diff_data_csv(src_tc, trg_tc, outputgrp))


def console_interactive_mode(src_tc, trg_tc, diff_addrs, outputgrp):
    """Interactive mode via console
    """
    print("Addresses that have different data:")
    print(diff_addrs)
    addr_chosen = raw_input("Which address to display?: ")
    while addr_chosen in diff_addrs or addr_chosen == "all":
        if addr_chosen == "all":
            print(get_diffs_data_str(src_tc, trg_tc, outputgrp))
        else:
            print(get_diff_data_str(src_tc, trg_tc, addr_chosen, outputgrp))

        print(diff_addrs)
        addr_chosen = raw_input("Which address to display?: ")


def print_usage():
    print(
        "{0} [-s <sourcepath>] [-t <targetpath>] \
         [-o <outputpath>] [-f <format>]".format(__file__))
    print("\t-s source (root) file path")
    print("\t-t comparable file path")
    print("\t-o difference output file path")
    print("\t-f format for output file. Formats:")
    print("\t\ttext - textual information format")
    print("\t\tcsv - spreadsheet information format")
    print("\t-h display this help")
    print("\t-g group data")


if __name__ == "__main__":
    sourcefile = ''
    targetfile = ''
    outputfile = ''
    outputfrmt = 'text'
    outputgrp = False
    """
    Option list:
        -s or --source for sourcefile
        -t or --target for targetfile
        -o or --output for outputfile
        -f or --format for output file format
        -h for help
    """
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "s:t:o:f:hg",
                                      ["source=", "target=",
                                       "output=", "format=",
                                       "help", "group"])
    except getopt.GetoptError as err:
        print str(err)
        print_usage()
        sys.exit(2)
    for o, a in optlist:
        if o in ("-s", "--source"):
            sourcefile = a
        elif o in ("-t", "--target"):
            targetfile = a
        elif o in ("-o", "--output"):
            outputfile = a
        elif o in ("-f", "--format"):
            # since there are only two formats currently,
            # set text to default
            if a == "csv":
                outputfrmt = a
        elif o in ("-g", "--group"):
            outputgrp = True
        else:
            print_usage()
            sys.exit(2)

    # mandatory
    while not sourcefile:
        sourcefile = raw_input("Source file:")

    # mandatory
    while not targetfile:
        targetfile = raw_input("Target file:")

    source_tc = CANTestCase(sourcefile)
    target_tc = CANTestCase(targetfile)
    diff_addrs = CANDiff().get_diff_addrs(source_tc, target_tc)
    if outputfile:
        with open(outputfile, "wb") as f:
            if outputfrmt == "text":
                save_as_text(f, source_tc, target_tc, outputgrp)
            else:
                save_as_csv(f, source_tc, target_tc, outputgrp)
        print("Saved as '{1}' type to {0}".format(outputfile, outputfrmt))
    else:
        console_interactive_mode(source_tc, target_tc, diff_addrs, outputgrp)