#!/usr/bin/env python
# vim:fileencoding=utf-8
# -*- coding: utf-8 -*-
"""
shell_tool
shell.py
Author: Danyal Ahsanullah
Date: 4/20/2017
License: N/A
Description: main shell file for the tool
"""

import os
import sys
from cmd import Cmd
from contextlib import suppress
from datetime import datetime as dt

from utils import cmd_parser


class Shell(Cmd):
    __version__ = "0.0.2 - 'Silly Name Here'"
    prompt = '(FAKE) DAQ-CLI > '
    try:
        if cmd_parser.daq.FAKE:
            prompt = '(FAKE) DAQ-CLI > '
    except AttributeError:  # if FAKE doesnt exist
        pass
    intro = 'DAQ-CLI v {}\nStarting Capture Tool.' \
            ' Type "help" or "?" to get a list of help commands \n'.format(__version__)
    # doc_header = "Documented commands (type help <topic>):"
    # misc_header = "Miscellaneous help topics:"
    # undoc_header = "Undocumented commands:"

    def __init__(self, *args, **kwargs):
        super(Shell, self).__init__(*args, **kwargs)
        self.session = str(dt.now().strftime('%d-%b-%Y--%H-%M-%f'))
        self.cli = cmd_parser.CliParsers()

    def help_fin_read(self):
        self.cli.fin_parser.print_help()

    def help_con_read(self):
        self.cli.con_parser.print_help()

    def help_view_data(self):
        self.cli.view_parser.print_help()

    def help_save(self):
        self.cli.save_parser.print_help()

    def help_quit(self):
        self.cli.quit_parser.print_help()

    def do_fin_read(self, *args):
        """reads finite amounts of data"""
        with suppress(SystemExit):
            command = self.cli.fin_parser.parse_args(str(*args).split(' '))
            command.func(**vars(command))

    def do_con_read(self, *args):
        """reads continuously until canceled, output saved to file parameter"""
        with suppress(SystemExit):
            params = list(filter(None, str(*args).split(' ')))
            if not params:
                params.insert(0, self.session+'.txt')
            command = self.cli.con_parser.parse_args(params)
            command.func(**vars(command))

    def do_view_data(self, *args):
        """lets you view the contents of the current buffer"""
        with suppress(SystemExit):
            if str(*args).split(' ')[0] == '':
                command = self.cli.view_parser.parse_args(*args)
            else:
                command = self.cli.view_parser.parse_args(str(*args).split(' '))
            command.func(**vars(command))

    def do_save(self, *args):
        with suppress(SystemExit):
            params = list(filter(None, str(*args).split(' ')))
            if not params:
                params.insert(0, self.session+'.txt')
            command = self.cli.save_parser.parse_args(params)
            command.func(**vars(command))

    def do_quit(self, *args):
        """
        Quit the program.

        Usage:
        quit [-q] [-f  [FILENAME]]

        Options:
        -q     force quit with no prompt to save (will NOT save current buffer(s) contents
        -f     confirm save and exit with save filename being the string passed in the FILENAME field
        """
        """"
        Example call:
        quit                    before exit ask user if wanting to save contents of buffer(s) to file
        quit -q                 force quit
        quit -f test_run.txt    before exit save contents of buffer(s) to file(s) named 'test_run.txt'
        """
        with suppress(SystemExit):
            params = list(filter(None, str(*args).split(' ')))
            params.extend(['-s', self.session])
            command = self.cli.quit_parser.parse_args(params)
            command.func(**vars(command))
        return True

    def do_session(self, name):
        """if no arguments provided, echos current session name"""
        if name != "":
            self.session = name
        else:
            print('\n'+self.session+'\n')

    @staticmethod
    def do_version(*args, **kwargs):
        """print version of shell"""
        print(Shell.__version__)

    @staticmethod
    def do_buffer_size(num: int, *args, **kwargs):
        """
        Check buffer size - if argument [num] passed, resize buffer to size num

        Usage:
        buffer_size [num]

        Options:
        [num] -- size to make the buffer
        """
        if num == '':
            print(len(cmd_parser.daq.dq.data))
        else:
            try:
                # TODO support rest of args to buffer resize
                cmd_parser.daq.dq.buffer_resize(int(num))
            except ValueError:
                print('invalid input, [num] must be of type <int>')

    def do_EOF(self, line):
        return True

    @staticmethod
    def do_shell(line):
        """Run a shell command"""
        output = os.popen(line).read()
        print(output)


class ScriptShell(Shell):
    prompt = ''
    use_rawinput = False


def create_shell(func):
    return func

if __name__ == '__main__':
    """ run shell """
    passed = len(sys.argv)
    shell = create_shell(Shell().cmdloop)
    if passed > 1:
        if sys.argv[1] == 'FAKE':
            sys.argv.remove('FAKE')
            passed -= 1
        if os.path.isfile(sys.argv[1]):
            input_stream = open(sys.argv[1], 'rt')
            shell = create_shell(ScriptShell(stdin=input_stream).cmdloop)
        elif not passed == 2:  # if sys argv is NOT "python shell.py FAKE"
            shell = create_shell(lambda: Shell().onecmd(' '.join(sys.argv[1:])))
    shell()
    try:
        input_stream.close()
    except NameError:
        pass
    finally:
        sys.exit(0)
