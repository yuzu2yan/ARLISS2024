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
        # cv2.imwrite(directory_path + '/' + now.strftime('%Y%m%d %H:%M:%S') + "_clahe.jpg", img)
        results = model(img)
        print("Model inference completed.")
        # If nothing is detected, return 0
        if len(results[0].boxes) == 0:
            print("No object detected.")
            return 0, 0, "not found", original_file_name, "not found"
        # Annotate the frame with the results
        annotated_frame = results[0].plot()
        cv2.imwrite(directory_path + '/' + now.strftime('%Y%m%d %H:%M:%S') + "_annotated.jpg", annotated_frame)
        print("Frame annotated.")
        result_object = results[0]
        print("Results obtained.")
        try:
            # Get the bounding box positions
            bounding_boxes = result_object.boxes.xyxy
            central_x = ((bounding_boxes[0][0] + bounding_boxes[0][2]) / 2.0).item() / frame.shape[1] * 100
            print("central_x:", central_x)
            percent = int(100 * result_object.boxes.conf[0])
            print("percent:", percent)
            red_cone_percent = ((bounding_boxes[0][2] - bounding_boxes[0][0]) * (bounding_boxes[0][3] - bounding_boxes[0][1]) / (frame.shape[0] * frame.shape[1]) * 100).item()
            print("red_cone_percent:", red_cone_percent)
            print("Bounding boxes obtained.")
        except Exception as e:
            print("Error:", e)
            return 0, 0, "not found", original_file_name, "not found"            
    
    else:
        print("Error: Frame not read successfully.")
        return 0, 0, "not found", "not found", "not found"
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
    model = YOLO('../model/yolo.pt')
    # Initialize Picamera2
    picam2 = Picamera2()
    config = picam2.create_preview_configuration()
    picam2.configure(config)
    picam2.start()  
    
    drive = motor.Motor()
    while True:
        percent, red_cone_percent, loc, original_file_name, annotated_file_name = detect_cone(picam2, model)
        print("percent:", percent, "location:", loc)
        # Goal judgment
        if red_cone_percent < 10 and loc != "not found":
            print("Reach the goal")
            drive.forward()
            time.sleep(2.0)
            drive.stop()
            break
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