from argparse import ArgumentParser

def read_arguments():
    parser = ArgumentParser(description="BQ78412 device driver")
    parser.add_argument('-p', '--port', default="/dev/ttyUSB0", type=str, help='Direction of the device')
    parser.add_argument('-t', '--timeout', default=1, type=int, help='Timeout time in seconds waiting a response', choices=range(1,11))
    #parser.add_argument('-d', '--timebetweendata', default=5, type=int, help='Time between updating data from device in seconds', choices=range(5,601))
    parser.add_argument("-v", "--verbose", help="increase output verbosity",action="store_true")
    args = parser.parse_args()
    return vars(args)
