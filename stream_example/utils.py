
import time
timeDif = time.time();
def printTimeDiff(reason):
    global timeDif
    print(reason.ljust(20), 'took {} seconds'.format(time.time()-timeDif))
    timeDif = time.time()
def initTimeDiff():
    global timeDiff
    timeDiff = time.time();
