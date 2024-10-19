import cv2 as cv
import numpy as np

class object_detection:
    weight_path = 'models/yolov3-tiny/yolov3-tiny.weights'
    config_path = 'models/yolov3-tiny/yolov3-tiny.cfg'
    classes = []
    with open('models/coco.names', 'r') as f:
        classes = [line.strip() for line in f.readlines()]
    

    def __init__(self,weight_path=weight_path,config_path=config_path,classes=classes):
        self.weight_path=weight_path
        self.config_path=config_path
        self.net = cv.dnn.readNet(weight_path, config_path)
        self.classes = classes
       
    def detect_objects(self,frame):
    

        # Create a blob from the frame and perform a forward pass
        #the frame is already in BGR format
        blob = cv.dnn.blobFromImage(frame, 1/255, (320, 320), (0, 0, 0), swapRB=False, crop=False)
        self.net.setInput(blob)
        # layer_names = self.net.getLayerNames()
        output_layers = self.net.getUnconnectedOutLayersNames()
        #returns a list with first for 4 coordinates and then the rest confidence of the object at the 4 coordinate being the entity at that index - 4 in coco.name (classes)
        outputs = self.net.forward(output_layers)
        return outputs

    def draw_boxes(self,frame,outputs):

        height, width = frame.shape[:2]
        boxes = []
        confidences = []
        class_ids = []



        # Process the outputs
        for output in outputs:
            for detection in output:
                scores = detection[5:]  # Class scores
                # print(f'score for each class: {scores}')
                #returns the index of the class object
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:  # Confidence threshold
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        # Apply Non-Maxima Suppression
        indexes = cv.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        # Draw boxes and labels on the frame
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(self.classes[class_ids[i]])
                confidence = confidences[i]
                color = (0, 255, 0)  # Green color for bounding box
                cv.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv.putText(frame, f"{label} {confidence:.2f}", (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        return frame

