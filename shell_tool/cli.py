import argparse
import cmd
from constants import *
import daq_handler
import sys


class Cli:
    def __init__(self):
        self.quit = False
        self.parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        self.parser.add_argument('--version', action='version', version='0.0.1')
        self.subparsers = self.parser.add_subparsers()

        fin_read_parser = self.subparsers.add_parser('fin_read')
        fin_read_parser.add_argument('samples', default=samples_, help='number of samples to read in a given run (default: {})'.format(samples_))
        fin_read_parser.add_argument('--sample_rate', action='store_const', const=sample_rate_, help='set sample rate (Hz) for the DAQ (default: {})'.format(sample_rate_))
        fin_read_parser.add_argument('--min', const=min_, action='store_const', help='minimum input voltage (default: {})'.format(min_))
        fin_read_parser.add_argument('--max', const=max_, action='store_const', help='maximum input voltage (default: {})'.format(max_))
        fin_read_parser.set_defaults(func=daq_handler.fin_read)

        con_read_parser = self.subparsers.add_parser('con_read')
        con_read_parser.add_argument('--sample_rate', action='store_const', const=sample_rate_, help='set sample rate (Hz) for the DAQ (default: {})'.format(sample_rate_))
        con_read_parser.add_argument('--min', const=min_, action='store_const', help='minimum input voltage (default: {})'.format(min_))
        con_read_parser.add_argument('--max', const=max_, action='store_const', help='maximum input voltage (default: {})'.format(max_))
        con_read_parser.set_defaults(func=daq_handler.con_read)



    #     quit_parser = self.subparsers.add_parser('quit')
    #     quit_parser.add_argument('--confirm', action='store_true', default=False, help='exit CLI')
    #     quit_parser.set_defaults(func=self.quitAction)
    #
    # def quitAction(self, confirm):
    #     if confirm is True:
    #         self.quit = True
    #     else:
    #         choice = input('really exit? (y/n): ')
    #         if choice.lower() == 'y':
    #             self.quit = True
    #         else:
    #             pass


class Storage:
    pass

if __name__ == '__main__':
    import os
    storage = Storage()
    cli = Cli()
    args = cli.parser.parse_args()
    while not cli.quit:
        try:
            args.func(args)
        except Exception as err:
            print(err)
            os.system('pause')
            print(daq_handler.data)
        # cli.quitAction(True)
    sys.exit(0)
