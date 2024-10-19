import cv2 as cv
class traning:
    


    #take a screenshot after every interval and store it to the traning folder
    @staticmethod       
    def screenshot(frame):
        cv.imwrite('python/training/'+str(time())+'.jpg',frame)


