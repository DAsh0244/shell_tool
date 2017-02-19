import argparse
# import daq_handler as daq
import fake_daq as daq
import constants as CON


class ReadParser(argparse.ArgumentParser):
    """overloaded class to disable help flags by default
      -- otherwise identical to argparse.ArguementParser"""
    def __init__(self, *args, **kwargs):
        super(ReadParser, self).__init__(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                         add_help=False, *args, **kwargs)


class Cli:
    """
        DAQ CLI shell command parsers
        Ideally want one parser per command for stability of parsing commands"""
    def __init__(self):
        self.save_parser = ReadParser('save')
        self.fin_parser = ReadParser('fin_read')
        self.con_parser = ReadParser('con_read')
        self.view_parser = ReadParser('view')
        self.quit_parser = ReadParser('quit')

        """ Save data Parser """
        self.save_parser.add_argument('--version', action='version', version='0.0.1')
        self.save_parser.add_argument('file_name', type=str, action='store',
                                      help='file name to save current data as')
        self.save_parser.set_defaults(func=daq.save)

        """ Finite Read Parser """
        self.fin_parser.add_argument('--version', action='version', version='0.0.1')
        self.fin_parser.add_argument('samples_', type=int, action='store', default=CON.samples_,
                                     help='number of samples_ to read in a given run (default: {})'.format(CON.samples_))
        self.fin_parser.add_argument('--sample_rate_', type=float, action='store', nargs='?', default=CON.sample_rate_,
                                     help='set sample rate (Hz) for the DAQ (default: {})'.format(CON.sample_rate_))
        self.fin_parser.add_argument('--min_', type=float, default=CON.min_, nargs='?', action='store',
                                     help='minimum input voltage (default: {})'.format(CON.min_))
        self.fin_parser.add_argument('--max_', type=float, default=CON.max_, nargs='?', action='store',
                                     help='maximum input voltage (default: {})'.format(CON.max_))
        self.fin_parser.set_defaults(func=daq.fin_read)

        """ Continuous Read Parser """
        self.con_parser.add_argument('--version', action='version', version='0.0.1')
        self.con_parser.add_argument('--sample_rate_', type=float, action='store', nargs='?', const=CON.sample_rate_,
                                     help='set sample rate (Hz) for the DAQ (default: {})'.format(CON.sample_rate_))
        self.con_parser.add_argument('--min_', type=float, const=CON.min_, nargs='?', action='store',
                                     help='minimum input voltage (default: {})'.format(CON.min_))
        self.con_parser.add_argument('--max_', type=float, const=CON.max_, nargs='?', action='store',
                                     help='maximum input voltage (default: {})'.format(CON.max_))
        self.con_parser.set_defaults(func=daq.con_read)

        """ View Parser """
        self.view_parser.add_argument('--version', action='version', version='0.0.1')
        self.view_parser.add_argument('entries', type=int, action='store', default=CON.buf_size_,
                                      help='how many entries in buffer to view')
        self.view_parser.add_argument('--tail', action="store_true", default=False,
                                      help='view the last elements in the buffer')
        self.view_parser.set_defaults(func=daq.view)

        """" Quit Parser """
        self.quit_parser.add_argument('-q', action='store_true', default=False, help='exit CLI')
        self.quit_parser.add_argument('-f', type=str, action='store', help='exit CLI')
        # self.quit_parser.set_defaults(func=daq.save)

if __name__ == '__main__':
    """ Testing for each parser """
    # todo - automate testing in a seperate file?
    import os
    import sys
    cli = Cli()
    args = cli.fin_parser.parse_args()
    args.func(**vars(args))

    os.system('pause')
    args = cli.con_parser.parse_args(['--sample_rate_', '12'])
    args.func(**vars(args))

    os.system('pause')
    args = cli.view_parser.parse_args(['12'])
    args.func(**vars(args))

    os.system('pause')
    args = cli.quit_parser.parse_args(['-q'])
    # args.func(**vars(args))
    print(**vars(args))

    sys.exit(0)
