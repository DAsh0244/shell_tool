import sys
from cmd import Cmd
import cmd_parser
from contextlib import suppress
from datetime import datetime as dt


class Shell(Cmd):
    def __init__(self):
        super(Shell, self).__init__()
        self.session = str(dt.today())
        self.prompt = 'DAQ-CLI > '
        self.intro = '\nStarting Capture Tool. Type "help" or "?" to get a list of help commands \n'
        self.cli = cmd_parser.Cli()

    def help_fin_read(self):
        self.cli.fin_parser.print_help()

    def help_con_read(self):
        self.cli.con_parser.print_help()

    def help_view_data(self):
        self.cli.view_parser.print_help()

    def help_save_data(self):
        self.cli.save_parser.print_help()

    def do_fin_read(self, *args):
        """reads finite amounts of data"""
        with suppress(SystemExit):
            command = self.cli.fin_parser.parse_args(args)
            command.func(**vars(command))

    def do_con_read(self, *args):
        """reads continuously until canceled, output saved to file parameter"""
        with suppress(SystemExit):
            command = self.cli.con_parser.parse_args(args)
            command.func(**vars(command))

    def do_view_data(self, *args):
        """lets you view the contents of the current buffer"""
        with suppress(SystemExit):
            command = self.cli.view_parser.parse_args(args)
            command.func(**vars(command))

    def do_save_data(self, *args):
        with suppress(SystemExit):
            command = self.cli.save_parser.parse_args(args)
            command.func(**vars(command))

    def do_quit(self, flag):
        """
        Quit the program.

        Usage:
        quit [-q] [-y  FILENAME]

        Options:
        -q      force quit with no prompt to save (will NOT save current buffer(s) contents
        -y      confirm save and exit with save filename being the string passed in the FILENAME field
        """
        """"
        Example call:
        quit                    before exit ask user if wanting to save contents of buffer(s) to file
        quit -q                 force quit
        quit -y test_run.txt    before exit save contents of buffer(s) to file(s) named 'test_run.txt'
        """
        if flag == "":
            save = input('save contents of session to file? (y/n)  ')
            if save.lower == 'y':
                with open('{}.txt'.format(self.session), mode='w') as f:
                    f.write(self.cli.get_data())
                    f.write('asdf')
        else:
            try:
                if flag.lower == '-q':
                    with open('{}.txt'.format(self.session), mode='w') as f:
                        f.write(self.cli.get_data())
                        f.write('asdf')
            except:
                pass
        raise SystemExit

    def do_session(self, name):
        """if no arguments provided, echos current session name"""
        if name != "":
            self.session = name
        else:
            print('\n'+self.session+'\n')

    @staticmethod
    def do_buffer_size(num):
        cmd_parser.daq.data = cmd_parser.daq.np.array(num)


if __name__ == '__main__':
    prompt = Shell()
    prompt.cmdloop()
    sys.exit(0)
