import cv2
import datetime
from ultralytics import YOLO


if __name__ == "__main__":
    now = datetime.datetime.now()
    model = YOLO('./best.pt')
    print("Model loaded successfully.")  
        # Convert the frame to RGB 
    frame = cv2.imread('./8_.jpg')
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)
    img_yuv = cv2.cvtColor(frame_rgb, cv2.COLOR_BGR2YUV) # RGB => YUV(YCbCr)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8)) # create a CLAHE object
    img_yuv[:,:,0] = clahe.apply(img_yuv[:,:,0]) # apply CLAHE to the Y-channel (luminance)
    img = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2RGB) # YUV => RGB
    filename = now.strftime('%Y%m%d %H:%M:%S') + "_clahe.jpg"
    cv2.imwrite(filename, img)
    
    results = model(img)
    print("Model inference completed.")
    # Annotate the frame with the results
    annotated_frame = results[0].plot()
    
    result_object = results[0]

    # Get the bounding box positions
    bounding_boxes = result_object.boxes.xyxy

    # Get the class IDs
    class_ids = result_object.boxes.cls
    # Get the class names
    class_names_dict = result_object.names

    for box, class_id in zip(bounding_boxes, class_ids):
        class_name = class_names_dict[int(class_id)]
        print(f"Box coordinates: {box}, Object: {class_name}")
    
    # # Display the annotated frame
    # cv2.imshow("YOLOv8 Inference", annotated_frame)
    now = datetime.datetime.now()
    filename = now.strftime('%Y%m%d %H:%M:%S') + "_annotated.jpg"
    cv2.imwrite(filename, annotated_frame)

        # # Break the loop if 'q' is pressed
        # if cv2.waitKey(1) & 0xFF == ord("q"):
        #     break