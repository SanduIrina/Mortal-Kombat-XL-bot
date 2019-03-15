import numpy as np
import cv2, struct, sys, pickle, socket
from utils import printTimeDiff, initTimeDiff




sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

data = ''
payload_size = struct.calcsize("L")

curFrame = -1
lastFrame = -1
frameFragments = None
curFragments = 0

def initFrameFragments():
    global frameFragments, curFragments
    fragmentShape = None
    frameFragments = None
    curFragments = 0


def decodeData(p):
    packed_msg_size = p[:payload_size]
    msg_size = struct.unpack("L", packed_msg_size)[0]
    res = p[payload_size:]
    return pickle.loads(res)

compressionRatio = 1

import time



def renderFrame(frameCallback):
    global compressionRatio
    frame = np.concatenate(frameFragments)
    # resize to its original size

    # comment this log (it's verbose, but helpful to benchmark your fps)
    printTimeDiff('receiving new frame ' + str(curFrame)+ ', with ' + str(len(frameFragments)) + ' fragments')
    resized = cv2.resize(frame, (0,0), fx=1/compressionRatio, fy=1/compressionRatio)
    frameCallback(resized)
    initFrameFragments()


def startListening(ip, port, frameCallback):
    global frameFragments, curFragments, lastFrame, curFrame
    global data, compressionRatio, sock, UDP_PORT
    # frames are sent as fragmented UDP packets
    sock.bind((ip, port))
    while True:
        fragment, metadata = (None,) * 2
        try:
            while len(data) < payload_size:
                data += sock.recv(65000)
            (metadata, fragment) = decodeData(data)
            data = ''
            (curFrame, curFragment, maxFragments, compressionRatio) = metadata
            # check if we receive a new fragment or server has restarted
            if curFrame - 20 > lastFrame and lastFrame != -1:
                print('Mismatching stream', curFrame, lastFrame)
                #server or internet was restarted, lost too many frames, drop anything saved
                initFrameFragments()
                lastFrame = curFrame

            #frame had some lost packets, but a new frame already arrived
            #so we forcefully render the last, incomplete frame
            forcedRender = False
            if curFrame > lastFrame or curFrame == 0:
                #some packets were lost along the way
                if (maxFragments >= 10 and float(curFragments) / maxFragments > 0.9):
                    # if the frame has lost less than 10% of its required packets, still render it
                    emptyFragment = None
                    for index, elem in enumerate(frameFragments):
                        if (not (frameFragments[index] is None)):
                            emptyFragment = np.zeros(frameFragments[index].shape, np.uint8)
                            break

                    for index, elem in enumerate(frameFragments):
                        if (frameFragments[index] is None):
                            frameFragments[index] = emptyFragment
                    renderFrame(frameCallback)
                    forcedRender = True
                lastFrame = curFrame
                initFrameFragments()

            if (frameFragments is None):
                # array of <None> with <maxFragments> elements
                frameFragments = [None] * maxFragments

            frameFragments[curFragment] = fragment
            curFragments += 1
            if (curFragments == maxFragments and not forcedRender):
                renderFrame(frameCallback)

            data = ''

        except Exception as e:
            print('error', e)
            initFrameFragments()
            data = ''
