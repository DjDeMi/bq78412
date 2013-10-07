import getopt
import sys

def help():
    sys.stderr.write("""Erabilera: python main.py [aukerak]

    aukerak:
    -p, --port=PORT: Erabili nahi den portu seriaren helbidea

    Adibidez:
        python3.3 main.py -p /dev/ttyUSB0

    """)


def read_arguments():
    
    values = {}
    values['port']=0
    values['timeout']=1
    values['tbd']=5

    try:
        opts, args = getopt.getopt(sys.argv[1:],
                "hp:",
                ["help", "port="]
                )
    except getopt.GetoptError:
        #print help information and exit
        help()
        sys.exit(2)

    #read the arguments
    for o,a in opts:
        if o in ("-h", "--help"):
            help()
            sys.exit()
        elif o in ("-p", "--port"):
            try:
                values['port'] = int(a)
            except ValueError:
                values['port'] = a
        elif o in ("-t", "--timeout"):
            values['timeout'] = int(a)
        elif o in ("-tbd", "--timebetweendata"):
            values['tbd'] = int(a)
    return values
