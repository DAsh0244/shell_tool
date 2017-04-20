# -*- coding: utf-8 -*-
import argparse
import constants as con
import sys
try:
    if str(sys.argv[1]).upper() == 'FAKE':
        import fake_daq as daq
        print('running in fake daq mode')
except IndexError:
    import daq_handler as daq


class ReadParser(argparse.ArgumentParser):
    """overloaded class to disable help flags by default
      -- otherwise identical to argparse.ArguementParser"""
    def __init__(self, *args, **kwargs):
        super(ReadParser, self).__init__(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                         add_help=False, *args, **kwargs)


class CliParsers:
    """
        DAQ CLI shell command parsers
        Ideally want one parser per command for stability of parsing commands
    """
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
        self.fin_parser.add_argument('samples', type=int, action='store', default=con.samples_,
                                     help='number of samples to read in a given run (default: {})'.format(con.samples_))
        self.fin_parser.add_argument('--sample_rate', type=float, action='store', nargs='?', default=con.sample_rate_,
                                     help='set sample rate (Hz) for the DAQ (default: {})'.format(con.sample_rate_))
        self.fin_parser.add_argument('--min', type=float, default=con.min_, nargs='?', action='store',
                                     help='minimum input voltage (default: {})'.format(con.min_))
        self.fin_parser.add_argument('--max', type=float, default=con.max_, nargs='?', action='store',
                                     help='maximum input voltage (default: {})'.format(con.max_))
        self.fin_parser.set_defaults(func=daq.fin_read)

        """ Continuous Read Parser """
        self.con_parser.add_argument('--version', action='version', version='0.0.1')
        self.con_parser.add_argument('--sample_rate_', type=float, action='store', nargs='?', const=con.sample_rate_,
                                     help='set sample rate (Hz) for the DAQ (default: {})'.format(con.sample_rate_))
        self.con_parser.add_argument('--min', type=float, const=con.min_, nargs='?', action='store',
                                     help='minimum input voltage (default: {})'.format(con.min_))
        self.con_parser.add_argument('--max', type=float, const=con.max_, nargs='?', action='store',
                                     help='maximum input voltage (default: {})'.format(con.max_))
        self.con_parser.add_argument('--file')
        self.con_parser.set_defaults(func=daq.con_read)

        """ View Parser """
        self.view_parser.add_argument('--version', action='version', version='0.0.1')
        self.view_parser.add_argument('entries', type=int, action='store', default=con.buf_size_,
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
    # todo - automate testing in a separate file?
    # import os
    sys.argv.remove('FAKE')
    cli = CliParsers()

    print('\nfin parser:')
    args = cli.fin_parser.parse_args(['120'])
    args.func(**vars(args))

    # os.system('pause')
    print('\ncon parser:')
    args = cli.con_parser.parse_args(['--sample_rate_', '12'])
    args.func(**vars(args))

    # os.system('pause')
    print('\nview parser:')
    args = cli.view_parser.parse_args(['12'])
    args.func(**vars(args))

    # os.system('pause')
    print('\nquit parser:')
    args = cli.quit_parser.parse_args(['-q'])
    # args.func(**vars(args))
    # print(**vars(args))

    sys.exit(0)
