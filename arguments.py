import getopt
import sys

def help():
    sys.stderr.write("""Erabilera: python3.3 main.py [aukerak]

    aukerak:
    -p, --port=PORT: Erabili nahi den portu seriaren helbidea
    -t, --timeout=TIMEOUT: Serie portuaren timeout-a (segundutan)
    -d, --timebetweendata=TBD: Behin baino gehiagotan jarriz gero datuak jasotzen, datu bat eta hurrengoaren artean zenbat denbora pasako den (segundutan). GOMENDAGARRIA 5 SEGUNDUTIK GORA

    Adibidez:
        python3.3 main.py -p /dev/ttyUSB0 -t 1 -d 10

    \n""")


def read_arguments():
    
    values = {}
    values['port']=0
    values['timeout']=1
    values['tbd']=5

    try:
        opts, args = getopt.getopt(sys.argv[1:],
                "hp:td",
                ["help", "port=", "timeout", "timebetweendata"]
                )
    except getopt.GetoptError:
        #print help information and exit
        help()
        sys.exit(2)

    #read the arguments
    for o,a in opts:
        print("opts: "+o)
        print("args: "+a)
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
        elif o in ("-d", "--timebetweendata"):
            values['tbd'] = int(a)
    return values
