import numpy as np
import cv2
import torch
import time
import datetime

class MangoDetection:
    # Initializing the class
    def __init__(self):
        self.lab = {0: "Unripe", 1: "Semi-ripe", 2: "Ripe"}
        self.start_ripe = [[30, 222, 0], [38, 255, 176]]
        self.semi_ripe  = [[25, 211, 127], [30, 255, 255]]
        self.ripe       = [[16, 195, 137], [27, 255, 255]]
        self.kernel = np.ones((5,5))

        # Loading the actual Machine Learning model file.
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path="media_files/models/model.pt", force_reload=False)
        
        self.classes = self.model.names
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print("Using Device: ", self.device)
    
    def empty():
        pass

    def score_frame(self, frame):
        self.model.to(self.device)
        results = self.model([frame])
        return results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
    
    def classify(self, roi):
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        mask0 = cv2.inRange(hsv, np.array(self.start_ripe[0]), np.array(self.start_ripe[1]))
        mask1 = cv2.inRange(hsv, np.array(self.semi_ripe[0]),  np.array(self.semi_ripe[1]))
        mask2 = cv2.inRange(hsv, np.array(self.ripe[0]),       np.array(self.ripe[1]))
        masks = [mask0, mask1, mask2]
        result = dict()
        for i in range(len(masks)):
            result[i] = np.sum(np.sum(masks[i], axis=0), axis=0)
        max = np.max(list(result.values()))
        classification = list(result.values()).index(max)
        return classification
    
    def plot_boxes(self, results, frame):
        labels, cord = results
        n = len(labels)
        x_shape, y_shape = frame.shape[1], frame.shape[0]
        for i in range(n):
            row = cord[i]
            if row[4] >= 0.5:
                x1, y1, x2, y2 = int(row[0]*x_shape), int(row[1]*y_shape), int(row[2]*x_shape), int(row[3]*y_shape)
                interest = frame[y1:y2, x1:x2]
                clsn = self.classify(interest)
                classification = clsn
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, self.classes[int(labels[i])]+" "+self.lab[classification], (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        image_name = str(datetime.datetime.now())
        print(image_name)
        cv2.imwrite(f"output_images/{image_name}.png", frame)
        return frame
    
    def live_detection(self):
        # Real-time detection
        camera = cv2.VideoCapture(0)
        while (True):
            time.sleep(3)
            ret, frame = camera.read()
            frame = cv2.resize(frame, (640, 640))
            results = self.score_frame(frame)
            frame = self.plot_boxes(results, frame)
            cv2.imshow('Mango Detection and Classification', frame)
            if cv2.waitKey(5) & 0xFF == 27:
                break
        camera.release()
        cv2.destroyAllWindows()
    
    def classify_mango_image(self, image):
        # Testing with sample mango images
        image = cv2.resize(image, (640, 640))
        results = self.score_frame(image)
        image = self.plot_boxes(results, image)
        return image
    
    def __call__(self):
        pass