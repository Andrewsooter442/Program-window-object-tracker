import cv2 as cv
import numpy as np
import mss
from time import time
import pygetwindow as gw

class Windowcapture:

    window = None
    def __init__(self):
         self.window = None

    def object_detection(self,haystack, needle, threshold=0.4, method=cv.TM_CCOEFF_NORMED):
        needle_w = needle.shape[1]
        needle_h= needle.shape[0]

        result = cv.matchTemplate(haystack, needle,method)
        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))
        rectangle = []
        for loc in locations:
            rect = [int(loc[0]),int(loc[1]), needle_w, needle_h]
            #intentional double append
            rectangle.append(rect)
            rectangle.append(rect)

        rectangles , weight =cv.groupRectangles(rectangle,1,0.5)
        return rectangles

    def draw_rectangles(self,img, rectangles, color=(0, 255, 0), thickness=2):
            for (x,y,w,h) in rectangles:
                cv.rectangle(img,(x,y),(x+w,y+h),(0 , 255, 0),cv.LINE_4)
            cv.imshow('img',img)

    def draw_crosses(self,img, rectangles, color=(0, 255, 0), thickness=2):
            for (x,y,w,h) in rectangles:
                cv.drawMarker(img,(x+w//2,y+h//2),(0 , 255, 0),2)
            cv.imshow('img',img)


    def getwindow(self):

    # Get the list of all the open windows and ask the user to choose one
        windows = gw.getAllTitles()
        return windows
        # for i, window in enumerate(windows):
        #     print(f"{i}: {window}")
        # window_title = int(input("Please enter the number of the window you want to capture: "))
        # window= windows[int(window_title)]
        # self.window = gw.getWindowsWithTitle(window)[0]
    
    def setwindow(self,window):
        self.window = gw.getWindowsWithTitle(window)[0]


    def getwindow_coordinates(self):
        bbox = {
            'x': self.window.top,
            'y': self.window.left,
            'width': self.window.width,
            'height': self.window.height
        }
        return bbox


    def capture_window(self):
    # Set the bounding box for mss
        bbox = {
            'top': self.window.top,
            'left': self.window.left,
            'width': self.window.width,
            'height': self.window.height
        }

        with mss.mss() as sct:

                img = sct.grab(bbox)
                img_np = np.array(img)
                img_bgr = cv.cvtColor(img_np, cv.COLOR_BGRA2BGR)
                return img_bgr
 