import cv2, sys

from utils import printTimeDiff, initTimeDiff
from client import startListening, curFrame, frameFragments

def example(frame):
    #TODO: do something with your frame
    
    #render frame to our screen
    cv2.imshow('client', frame)
    cv2.waitKey(1)


UDP_IP = "0.0.0.0"
UDP_PORT = 5005
if (len(sys.argv) > 1):
    UDP_PORT = int(sys.argv[1])
startListening(UDP_IP, UDP_PORT, example)
