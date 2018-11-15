#! /usr/bin/env python2

import sys
import os.path
import json
import re
import time
import serial
from serial.tools.miniterm import ask_for_port
from optparse import OptionGroup, OptionParser

__version__ = "0.02"
__copyright__ = 'Vladimir Kushnir aka Kvantum i(c)2018'


def get_param(arguments=None):
    """Parse Command-Line parameters"""
    parser = OptionParser(usage="%prog [options] <data> [<connection>] ", version="%prog " + __version__)
    opt_con = OptionGroup(parser, 'Connection Settings')
    opt_con.add_option("-p", "--port", dest="port", help="serial port name ('-' to show port list)")
    opt_con.add_option("-b", "--baudrate", dest="baudrate", help="set baud rate")
    parser.add_option_group(opt_con)
    parser.add_option("-s", "--sleep", dest="sleep", help="wait before read")
    parser.add_option('-f', '--file', dest='file', help="settings file (json)",
                      default=__file__.split('.')[0] + '.json')

    (opt, args) = parser.parse_args(arguments)

    if not os.path.isfile(opt.file):
        parser.error('Can\'t find data file \"{}\"!'.format(opt.file))

    with open(opt.file) as f:
        json_data = json.load(f)

    if len(args) < 1:
        sec_data = 'default'
    else:
        sec_data = args[0]

    if sec_data in json_data["data"]:
        data = json_data["data"][sec_data]
    else:
        parser.error('Can\'t find \"{}\" data section in data file \"{}\"!'.format(sec_data, opt.file))

    if len(args) > 1:
        sec_settings = args[1]
    else:
        sec_settings = 'default'

    if sec_settings in json_data["settings"]:
        settings = json_data["settings"][sec_settings]
    else:
        parser.error('Can\'t found \"{}\" settings section in data file \"{}\"!'.format(sec_settings, opt.file))

    if opt.port is not None:
        if opt.port == '-':
            settings['port'] = ask_for_port()
        else:
            settings['port'] = opt.port

    if opt.baudrate is not None:
        settings['baudrate'] = opt.baudrate

    if opt.sleep is not None:
        settings['sleep'] = opt.baudrate

    return settings, data


def get_serial(settings):
    """Connect to serial interface and return connection"""
    ser = serial.Serial(
        port=settings['port'],
        baudrate=settings['baudrate'],
        parity=serial.PARITY_ODD,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.SEVENBITS
    )

    if not ser.isOpen():
        try:
            ser.open()
        except Exception, e:
            print "Error open serial port: " + str(e)
            sys.exit(1)

    return ser


def get_input(out, data):
    """Check if output string matches keys in data and if true return values"""
    value = None
    for key in data.keys():
        if out.startswith(key):
            value = data[key].encode('ascii', 'ignore')
    return value


def main():
    # Get parameters and connection
    cfg, data = get_param()
    ser = get_serial(cfg)

    print 'Enter your commands below.\r\nInsert "exit" to leave the application.'
    user_input = ""
    sleep = cfg['sleep']
    while 1:
        if user_input == 'exit':
            ser.close()
            exit()
        else:
            ser.write(user_input + '\r\n')
            out = ''
            # let wait some time before reading output (let give device time to answer)
            time.sleep(sleep)
            while ser.inWaiting() > 0:
                out += ser.read(1)

            if out != '':
                #:TODO make splitlines universal (some devices return \r\n instead \n\r)
                # lines = out.splitlines()
                lines = re.split(r"[~\r\n]+", out)
                if lines[0].startswith(user_input):
                    del lines[0]
                user_input = get_input(lines[-1], data)
                if user_input is not None:
                    lines[-1] += ' <<-- ' + user_input
                print '\n'.join(lines)
                if user_input is None:
                    user_input = raw_input(">> ")


if __name__ == "__main__":
    main()
