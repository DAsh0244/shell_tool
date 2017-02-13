import sys
from cmd import Cmd
from datetime import datetime as dt
import cmd_parser


class Shell(Cmd):
    def __init__(self):
        super(Shell, self).__init__()
        self.session = str(dt.today())
        self.prompt = 'DAQ-CLI > '
        self.cli = cmd_parser.Cli()

    def help_fin_read(self, *args, **kwargs):
        self.cli.fin_parser.print_help()

    def do_fin_read(self, *args):
        """reads finite amounts of data"""
        cmd = self.cli.fin_parser.parse_args(args)
        cmd.func(**vars(cmd))

    def do_con_read(self, *args):
        """reads continuously until canceled, output saved to file parameter"""
        cmd = self.cli.con_parser.parse_args(args)
        cmd.func(**vars(cmd))

    def help_con_read(self, *args, **kwargs):
        self.cli.con_parser.print_help()

    def do_view_data(self, *args):
        """lets you view the contents of the current buffer"""
        cmd = self.cli.view_parser.parse_args(args)
        cmd.func(**vars(cmd))

    def help_view_data(self, *args, **kwargs):
        self.cli.view_parser.print_help()


    def do_quit(self, flag):
        """Quits the program."""
        if flag == "":
            save = input('save contents of session to file? (y/n)  ')
            if save.lower == 'y':
                with open('{}.txt'.format(self.session), mode='w') as f:
                    f.write(self.cli.get_data())
                    f.write('asdf')
        else:
            try:
                if flag.lower == '-y':
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
            print(self.session)


if __name__ == '__main__':
    prompt = Shell()
    prompt.cmdloop('Starting Capture Tool')
    sys.exit(0)
