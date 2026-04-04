#-----------------------------------------------------------------------
# runserver.py
# Author: Mohemeen Ahmed and Amel Osman
#-----------------------------------------------------------------------
""" Server program that takes in command line arguments and begins
our flask program. """

import sys
import argparse
import reg4

def main():
    parser = argparse.ArgumentParser(description=
    "The registrar application")
    parser.add_argument("port",type=int,
    help= "the port at which the server should listen")

    args = parser.parse_args()

    try:
        reg4.app.run(host='0.0.0.0', port=args.port, debug=True)
    except Exception as ex:
        print(f'{sys.argv[0]}: {ex}', file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
