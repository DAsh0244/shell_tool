#!/usr/bin/env python
# vim:fileencoding=utf-8
# -*- coding: utf-8 -*-
"""
shell_tool
cmd_parser.py
Author: Danyal Ahsanullah
Date: 4/24/2017
License: N/A
Description: parser(s) for CLI 
"""


__version__ = '0.0.2'


import sys
import argparse
from utils import constants as con
try:
    if str(sys.argv[1]).upper() == 'FAKE':
        from utils import fake_daq as daq
        # print('running in fake daq mode')
except IndexError:
    from utils import daq_handler as daq


class ReadParser(argparse.ArgumentParser):
    """
    Overloaded class to disable help flags by default. Modified formatter length as well
    Otherwise identical to argparse.ArguementParser
    """
    def __init__(self, *args, **kwargs):
        super(ReadParser, self).__init__(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                         add_help=False, *args, **kwargs)


class CliParsers:
    """
    DAQ CLI shell command parsers
    """
    save_parser = ReadParser('save', description='Save buffer to file')
    fin_parser = ReadParser('fin_read', description='Finite read')
    con_parser = ReadParser('con_read', description='Continuous read')
    view_parser = ReadParser('view', description='View buffer')
    quit_parser = ReadParser('quit', description='Quit the shell.')

    """ Save data Parser """
    # save_parser.add_argument('--version', action='version', version=__version__)
    save_parser.add_argument('file_name', type=str, action='store',
                             help='file name to save current data as')
    save_parser.set_defaults(func=daq.dq.save)

    """ Finite Read Parser """
    FIN_READ_ARGS = ('--sample_rate', '--min', '--max')
    # fin_parser.add_argument('--version', action='version', version=__version__)
    fin_parser.add_argument('samples', type=int, action='store', default=con.samples_,
                            help='number of samples to read in a given run')
    fin_parser.add_argument('--sample_rate', type=float, action='store', default=con.sample_rate_,
                            help='set sample rate (Hz) for the DAQ')
    fin_parser.add_argument('--min', type=float, action='store', default=con.min_,
                            help='minimum input voltage')
    fin_parser.add_argument('--max', type=float, action='store', default=con.max_,
                            help='maximum input voltage')
    fin_parser.set_defaults(func=daq.fin_read)

    """ Continuous Read Parser """
    CON_READ_ARGS = ('--sample_rate', '--min', '--max')
    # con_parser.add_argument('--version', action='version', version=__version__)
    con_parser.add_argument('file_name', type=str, help='file name for file to be saved as', )
    con_parser.add_argument('--sample_rate', type=float, action='store', default=con.sample_rate_,
                            help='set sample rate (Hz) for the DAQ')
    con_parser.add_argument('--min', type=float, action='store',
                            default=con.min_, help='minimum input voltage')
    con_parser.add_argument('--max', type=float, action='store',
                            default=con.max_, help='maximum input voltage')
    con_parser.set_defaults(func=daq.con_read)

    """ View Parser """
    VIEW_ARGS = ('--tail',)
    # view_parser.add_argument('--version', action='version', version=__version__)
    view_parser.add_argument('entries', type=int, action='store', default=con.buf_size_,
                             help='how many entries in buffer to view')
    view_parser.add_argument('--tail', action="store_true", default=False,
                             help='view the last elements in the buffer')
    view_parser.set_defaults(func=daq.dq.view)

    """" Quit Parser """
    # quit_parser.add_argument('--version', action='version', version=__version__)
    QUIT_ARGS = ('-q', '-f', '--file')
    group = quit_parser.add_mutually_exclusive_group()
    group.add_argument('-q', action='store_true', default=False,
                       help='force quit with no prompt to save (will NOT save current buffer(s) contents')
    group.add_argument('-f', '--file', type=str, action='store',
                       help='confirm save and exit with save filename being the string passed in the FILE '
                            'field')
    quit_parser.add_argument('-s', action='store', type=str, default='default_session',
                             help=argparse.SUPPRESS)
    quit_parser.set_defaults(func=daq.dq.quit_save)

if __name__ == '__main__':
    """ Testing for each parser """
    # todo - automate testing in a separate file?
    # import os
    # sys.argv.remove('FAKE')
    cli = CliParsers

    print('fin parser:')
    args = cli.fin_parser.parse_args(['--sample_rate', '12', '120'])
    print(vars(args), end='\n')
    # args.func(**vars(args))
    print('help:')
    cli.fin_parser.print_help()

    # os.system('pause')
    print('con parser:')
    args = cli.con_parser.parse_args(['--sample_rate', '12', 'test.txt'])
    print(vars(args), end='\n')
    # args.func(**vars(args))
    print('help:')
    cli.con_parser.print_help()

    # os.system('pause')
    print('view parser:')
    args = cli.view_parser.parse_args(['12'])
    # args.func(**vars(args))
    print(vars(args), end='\n')
    print('help:')
    cli.view_parser.print_help()

    # os.system('pause')
    print('quit parser:')
    args = cli.quit_parser.parse_args(['-f', 'test.txt', '-s', 'test'])
    # args.func(**vars(args))
    print(vars(args), end='\n')
    print('help:')
    cli.quit_parser.print_help()

    sys.exit(0)
