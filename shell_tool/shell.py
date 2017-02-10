import sys
from cmd import Cmd
import cli

class Shell(Cmd):
    def __init__(self):
        super(Shell, self).__init__()
        self.cli = cli.Cli()

    def do_fin_read(self, args):
        """reads finite amounts of data"""
        cmd = self.cli.parser.parse_args(['fin_read', args])
        cmd.func(args)

    def do_quit(self, args):
        """Quits the program."""
        print("Quitting.")
        raise SystemExit


if __name__ == '__main__':
    prompt = Shell()
    prompt.prompt = '> '
    prompt.cmdloop('Starting Capture Tool')
    sys.exit(0)
