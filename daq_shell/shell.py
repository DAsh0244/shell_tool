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


__version__ = "0.0.3 - 'Basically Working'"


import os
import sys
from cmd import Cmd
from contextlib import suppress
from utils import cmd_parser as cp
from datetime import datetime as dt
# import signal
#
#
# def handler(signum, frame):
#     pass
#
# signal.signal(signal.SIGINT, handler)


class ShellBase(Cmd):
    """
    Base class for DAQ shell. Should only be used as a parent class for a subclass.
    """
    # identchars = Cmd.identchars
    intro = 'ShellBase v{}\n'.format(__version__)
    prompt = 'Base > '
    ruler = '-'
    cli = cp.CliParsers
    # doc_header = "Documented commands (type help <topic>):"
    # misc_header = "Miscellaneous help topics:"
    # undoc_header = "Undocumented commands:"
    try:
        if cp.daq.FAKE:
            prompt = '(FAKE) Base > '
            intro = 'Running in fake daq mode\n' + intro
    except AttributeError:  # if FAKE doesnt exist
        pass

    def __init__(self, *args, **kwargs):
        super(ShellBase, self).__init__(*args, **kwargs)
        self.session = str(dt.now().strftime('%d-%b-%Y--%H-%M-%f'))
        # self.cli = cp.CliParsers

    # def cmdloop(self, intro=None):
    #     try:
    #         super(Shell, self).cmdloop(intro)
    #     except KeyboardInterrupt:
    #         sys.stdout.write('\n')
    #         self.do_quit('-q')

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
            self.session = name.replace(' ', '_')
        else:
            print('\n'+self.session+'\n')

    # noinspection PyUnusedLocal
    @staticmethod
    def do_version(*args, **kwargs):
        """print version of shell"""
        print(__version__)

    # noinspection PyUnusedLocal
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
            print(len(cp.daq.dq.data))
        else:
            try:
                # TODO support rest of args to buffer resize
                cp.daq.dq.buffer_resize(int(num))
            except ValueError:
                print('invalid input, [num] must be of type <int>')

    # noinspection PyUnusedLocal,PyPep8Naming
    @staticmethod
    def do_EOF(line):
        return True

    @staticmethod
    def do_shell(line):
        """Run a shell command"""
        output = os.popen(line).read()
        print(output)

    # noinspection PyUnusedLocal


class Shell(ShellBase):
    prompt = 'DAQ-CLI > '
    intro = 'DAQ-CLI v {}\n' \
            'Starting Capture Tool.\n' \
            'Type "help" or "?" to get a list of help commands.\n'.format(__version__)
    try:
        if cp.daq.FAKE:
            prompt = '(FAKE) DAQ-CLI > '
            intro = 'Running in fake daq mode\n' + intro
    except AttributeError:  # if FAKE doesnt exist
        pass

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

    def complete_fin_read(self, text, line, begidx, endidx):
        return [i for i in self.cli.FIN_READ_ARGS if i.startswith(text)]

    # noinspection PyUnusedLocal
    def complete_con_read(self, text, line, begidx, endidx):
        return [i for i in self.cli.CON_READ_ARGS if i.startswith(text)]

    # noinspection PyUnusedLocal
    def complete_view(self, text, line, begidx, endidx):
        return [i for i in self.cli.VIEW_ARGS if i.startswith(text)]

    # noinspection PyUnusedLocal
    def complete_quit(self, text, line, begidx, endidx):
        return [i for i in self.cli.QUIT_ARGS if i.startswith(text)]


class ScriptShell(ShellBase):
    prompt = ''
    use_rawinput = False

    def do_rem(self, *args):
        pass

    # noinspection PyPep8Naming
    def do_REM(self, *args):
        pass

    # noinspection PyPep8Naming
    def do_Rem(self, *args):
        pass

    def postloop(self):
        print('finished script execution.')

if __name__ == '__main__':
    """ run shell """
    passed = len(sys.argv)
    if passed > 1:
        if sys.argv[1] == 'FAKE':
            sys.argv.remove('FAKE')
            passed -= 1
            Shell().cmdloop()
        if (passed > 1) and os.path.isfile(sys.argv[1]):
            input_stream = open(sys.argv[1], 'rt')
            ScriptShell(stdin=input_stream).cmdloop()
            input_stream.close()
        elif passed != 1:  # if sys argv is NOT ".../shell.py FAKE"
            Shell().onecmd(' '.join(sys.argv[1:]))
    else:
        Shell().cmdloop()
    sys.exit(0)
