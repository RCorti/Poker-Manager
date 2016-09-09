#!/usr/bin/env python
import os, sys, getopt
from lib import queue

def help():
    print '\nUsage:\nhh_import.py [options]\n\nOptions:\n-d, --dir           Directory to import handhistory files.'
    
def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hd:", ["dir="])
    except getopt.GetoptError:
        help()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            help()
        elif opt in ("-d", "--dir"):
            hh_path(arg)
            
def hh_path(path):
    NoOfQueues = 0
    QueueName = 'hh_game'
    queue_game = queue.queue(QueueName)
    for file in os.listdir(path):
        NoOfQueues += hh_file(path+'/'+file, queue_game)
    queue_game.close()
    if NoOfQueues == 1:
        print "{} handhistory published in queue: '{}'".format(NoOfQueues, QueueName)
    else:
        print "{} handhistories published in queue: '{}'".format(NoOfQueues, QueueName)
    
def hh_file(filename, queue_game):
    NoOfQueues = 0
    file = open(filename, "r", 1)
    found = False
    game = ''
    for line in file:
        isEmpty = len(line.strip()) == 0
        if found:
            if isEmpty:
                queue_game.publish(game)
                NoOfQueues += 1
                found = False
            else:
                game += line
        else:
            if not isEmpty:
                game = line
                found = True
    if found:
        queue_game.publish(game)
        NoOfQueues += 1
        found = False
        
    file.close()
    return NoOfQueues
   
if __name__ == '__main__':
    main(sys.argv[1:])