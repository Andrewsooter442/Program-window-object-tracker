import pyautogui as gw
import numpy as np
from windowCapture import Windowcapture

class movement:
    def __init__(self):
        pass
    def move(self,coordinates,duration=0.1):
        gw.moveTo(coordinates[0],coordinates[1],duration)

    #outputs = output of the DNN model
    def mouse_snap(self,outputs,window,object_index=0,threshold=0.5,mouse_algo='simple',mouse_time = 500):

        x = 0
        y = 0
        for output in outputs:
            pos = []
            min = 0
            for obj in output:
                scores = obj[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > threshold and class_id == object_index:
                # if (obj[object_index+4]>threshold):
                    x =  obj[0]*window['width']#center of the detected object x
                    y =  obj[1]*window['height']#center of the detected object y
                    xd, yd = gw.position()
                    dist = abs(x-xd) + abs(y-yd)
                    if (dist < min or min == 0):
                        pos = [[x,y]]
                        min = dist
            if len(pos) > 0:
                self.move(pos[-1],mouse_time/1000)



        




