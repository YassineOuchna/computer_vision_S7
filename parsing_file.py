import argparse

def create_parser():

    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', '-m', dest='mode',
                        choices=['peer', 'client'],
                        type=str,
                        help='The zenoh session mode.')
    parser.add_argument('--connect', '-e', dest='connect',
                        metavar='ENDPOINT',
                        action='append',
                        type=str,
                        help='Endpoints to connect to.')
    parser.add_argument('--listen', '-l', dest='listen',
                        metavar='ENDPOINT',
                        action='append',
                        type=str,
                        help='Endpoints to listen on.')
    parser.add_argument('--key', '-k', dest='key',
                        default='main/puts',
                        type=str,
                        help='The key expression to publish onto.')
    parser.add_argument('--value', '-v', dest='value',
                        default='Pub from Python!',
                        type=str,
                        help='The value to publish.')
    parser.add_argument("--iter", dest="iter", type=int,
                        help="How many puts to perform")
    parser.add_argument('--config', '-c', dest='config',
                        metavar='FILE',
                        type=str,
                        help='A configuration file.')

    return parser
