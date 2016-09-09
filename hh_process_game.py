#!/usr/bin/env python
import os, sys, getopt
from lib import queue, partypoker, dbData

def help():
    print '\nUsage:\nhh_process_game.py'
    
def main(argv):
    try:
        opts, args = getopt.getopt(argv, "h")
    except getopt.GetoptError:
        help()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            help()
            os.exit()
            
    print 'Start parsing handhistories to mysql. Ctrl+C to stop.'
    hh_game = queue.queue('hh_game')
    hh_game.consume(callback)
    hh_game.close()

def callback(ch, method, properties, body):
    idPart = body[:20]
    if (partypoker.isValid(idPart)):
        partypoker.parse(body)
        print dbData.Id
    else:
        unknown = queue.queue('hh_unknown')
        unknown.publish(body)

if __name__ == '__main__':
    main(sys.argv[1:])