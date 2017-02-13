import argparse
import sys

# import daq_handler as daq
import fake_daq as daq
import constants as CON


class ReadParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super(ReadParser, self).__init__(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                         add_help=False, *args, **kwargs)


class Cli:
    def __init__(self):
        self.fin_parser = ReadParser('fin_read')
        self.con_parser = ReadParser('con_read')
        self.view_parser = ReadParser('view')

        """ Finite Read Parser """
        self.fin_parser.add_argument('--version', action='version', version='0.0.1')
        self.fin_parser.add_argument('samples', type=int, action='store', default=CON._samples,
                                     help='number of samples to read in a given run (default: {})'.format(CON._samples))
        self.fin_parser.add_argument('--sample_rate', type=float, action='store', nargs='?', const=CON._sample_rate,
                                     help='set sample rate (Hz) for the DAQ (default: {})'.format(CON._sample_rate))
        self.fin_parser.add_argument('--min', type=float, const=CON._min, nargs='?', action='store',
                                     help='minimum input voltage (default: {})'.format(CON._min))
        self.fin_parser.add_argument('--max', type=float, const=CON._max, nargs='?', action='store',
                                     help='maximum input voltage (default: {})'.format(CON._max))
        self.fin_parser.set_defaults(func=daq.fin_read)

        """ Continuous Read Parser """
        self.con_parser.add_argument('--version', action='version', version='0.0.1')
        self.con_parser.add_argument('--sample_rate', type=float, action='store', nargs='?', const=CON._sample_rate,
                                     help='set sample rate (Hz) for the DAQ (default: {})'.format(CON._sample_rate))
        self.con_parser.add_argument('--min', type=float, const=CON._min, nargs='?', action='store',
                                     help='minimum input voltage (default: {})'.format(CON._min))
        self.con_parser.add_argument('--max', type=float, const=CON._max, nargs='?', action='store',
                                     help='maximum input voltage (default: {})'.format(CON._max))
        self.con_parser.set_defaults(func=daq.con_read)

        """ View Parser """
        self.view_parser.add_argument('--version', action='version', version='0.0.1')
        self.view_parser.add_argument('entries', action='store', default=CON._BUFSIZE,
                                      help='how many entries in buffer to view')
        self.view_parser.add_argument('--tail', action='store_true',
                                      help='view the last elements in the buffer')
        self.view_parser.set_defaults(func=daq.view)

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

    def get_data(self):
        pass


class Storage:
    pass

if __name__ == '__main__':
    import os
    storage = Storage()
    cli = Cli()
    args = cli.fin_parser.parse_args()
    args.func(**vars(args))

    os.system('pause')
    args = cli.con_parser.parse_args(['--sample_rate','12'])
    args.func(**vars(args))

    os.system('pause')
    args = cli.view_parser.parse_args(['12'])
    args.func(**vars(args))

    # while not cli.quit:
    #     try:
    #         args.func(args)
    #     except Exception as err:
    #         print(err)
    #         os.system('pause')
    #         print(daq.data)
    #     # cli.quitAction(True)
    sys.exit(0)
