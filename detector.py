from ultralytics import YOLO
import cv2

class PersonDetector:
    def __init__(self, model_path='yolov8n.pt', conf=0.5):
        self.model = YOLO(model_path)
        self.conf = conf

    def detect(self, frame):
        results = self.model(frame, classes=[0], 
                           conf=self.conf, verbose=False)
        boxes = []
        for box in results[0].boxes:
            x1,y1,x2,y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            boxes.append({'bbox': (x1,y1,x2,y2), 'conf': conf,
                         'center': ((x1+x2)//2, (y1+y2)//2)})
        return boxes