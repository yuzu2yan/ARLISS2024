import cv2
import datetime
import numpy as np
from picamera2 import Picamera2
from ultralytics import YOLO
import motor
import time
import datetime

    
def detect_cone(picam2, model, directory_path="./"):
    frame = picam2.capture_array()
    if frame is not None:
        now = datetime.datetime.now()
        original_file_name = directory_path + '/' + now.strftime('%Y%m%d %H:%M:%S') + "_original.jpg"
        print("Frame read successfully.")
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)
        cv2.imwrite(original_file_name, frame_rgb)
        img_yuv = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2YUV) # RGB => YUV(YCbCr)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8)) # create a CLAHE object
        img_yuv[:,:,0] = clahe.apply(img_yuv[:,:,0]) # Apply CLAHE to the Y-channel (luminance)
        img = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2RGB) # YUV => RGB
        print("CLAHE applied.")
        results = model(img)
        print("Model inference completed.")
        # Annotate the frame with the results
        annotated_frame = results[0].plot()
        result_object = results[0]
        # Get the bounding box positions
        bounding_boxes = result_object.boxes.xyxy
        central_x = (bounding_boxes[0][0] + bounding_boxes[0][2]) / 2
        percent = int(100 * result_object.scores[0])
        red_cone_percent = (bounding_boxes[0][2] - bounding_boxes[0][0]) * (bounding_boxes[0][3] - bounding_boxes[0][1]) / (frame.shape[0] * frame.shape[1]) * 100
        # Get the class IDs
        class_ids = result_object.boxes.cls
        # Get the class names
        class_names_dict = result_object.names
        for box, class_id in zip(bounding_boxes, class_ids):
            class_name = class_names_dict[int(class_id)]
            print(f"Box coordinates: {box}, Object: {class_name}")
    else:
        print("Error: Frame not read successfully.")
        return 0, 0, 0, "not found"
    shape = frame.shape
    if red_cone_percent < 50:
        loc = "not found"
    elif central_x < shape[1] / 3:
        loc = "left"
    elif central_x > shape[1] * 2 / 3:
        loc = "right"
    else:
        loc = "center"
    now = datetime.datetime.now()
    annotated_file_name = directory_path + '/' + now.strftime('%Y%m%d %H:%M:%S') + "_annotated.jpg"
    cv2.imwrite(annotated_file_name, annotated_frame)
    return percent, red_cone_percent, loc, original_file_name, annotated_file_name


if __name__ == '__main__':
    model = YOLO('./best.pt')
    # Initialize Picamera2
    picam2 = Picamera2()
    config = picam2.create_preview_configuration()
    picam2.configure(config)
    picam2.start()  
    
    drive = motor.Motor()
    while True:
        percent, red_cone_percent, loc = detect_cone(picam2, model)
        print("percent:", percent, "location:", loc)
        # Goal judgment
        if red_cone_percent < 10:
            print("Reach the goal")
            drive.forward()
            time.sleep(2.0)
            drive.stop()
            break
        elif red_cone_percent < 1:
            drive.max_dutycycle = 65
        if loc == "right":
            drive.turn_right()
            time.sleep(0.3)
        elif loc == "left":
            drive.turn_left()
            time.sleep(0.3)
        elif loc == "not found":
            drive.forward()

    picam2.stop()   
    # cv2.destroyAllWindows()