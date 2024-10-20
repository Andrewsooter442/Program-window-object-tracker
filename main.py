#on startup
import cv2 as cv
import numpy as np
from traning import traning
from time import time
from objectdetection import object_detection
from windowCapture import Windowcapture
from movement import movement
class MainProgram():

    def __init__(self,wc,weight_path='model/yolov3-spp.weights',config_path='model/yolov3-spp.cfg',fov = 100, mouse_time = 0.5, mouse_algo = 'simple'):
        self.weight_path = weight_path
        self.config_path = config_path
        self.wc = wc # which window is being capture 
        self.fov =fov 

        #variables for mouse movement
        self.mouse_time = mouse_time
        self.mouse_algo =mouse_algo 


        #create a new object_movement object from the object_movement class. Moves the mouse to the center of the detected object
        self.movement = movement()
        #create a new object_detection object from the object_detection class. Detects the objects in the frame
        self.object_detection = object_detection(weight_path=self.weight_path,config_path=self.config_path)


    def run(self):
        print("Running")
        looptime = time()
        # weight = 'model/yolov3-spp.weights'
        # config = 'model/yolov3-spp.cfg'
        #run on each frame
        while(True):

            fps = 1/(time()-looptime)
            print(fps)
            looptime = time()

            #frame dimensions = window dimensions
            # print(f'fov is {self.fov}')
            frame = self.wc.capture_window()
            # print(f'frame shape {frame.shape}')
            width,height= self.wc.getwindow_coordinates()['width'], self.wc.getwindow_coordinates()['height']
            # print(f'width {width} height {height}')
            croped_width,croped_height= self.wc.getwindow_coordinates()['width']*int((self.fov//100)), self.wc.getwindow_coordinates()['height']*int((self.fov//100))
            # print(f'croped width {croped_width} croped height {croped_height}')
            x = width//2 - croped_width//2
            y = height//2 - croped_height//2
            # print(f'x {x} y {y}')
            frame = frame[y:y+croped_height,x:x+croped_width]    
            # print(frame.shape)



            # Outputs array of array of (x+width/2,y+height/2, width , height, confidence of object being classes[0], classes[1], classes[2], classes[3].....) for each pixel
            #returns a list with first for 4 coordinates and then the rest confidence of the object at the 4 coordinate being the entity at that index - 4 in coco.name (classes)
            outputs = self.object_detection.detect_objects(frame)
            self.object_detection.draw_boxes(frame, outputs)

            #snap the mouse to the center of the object (Algorithm simplesnap)
            self.movement.mouse_snap(outputs,self.wc.getwindow_coordinates(),mouse_algo=self.mouse_algo,mouse_time= self.mouse_time)
            cv.imshow('frame',frame)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break

