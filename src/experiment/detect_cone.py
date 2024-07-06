import cv2
import datetime
from picamera2 import Picamera2
from ultralytics import YOLO


if __name__ == "__main__":
    model = YOLO('./best.pt')
    print("Model loaded successfully.")
    # Initialize Picamera2
    picam2 = Picamera2()
    config = picam2.create_preview_configuration()
    picam2.configure(config)
    picam2.start()
    print("Picamera2 initialized successfully.")
    # Get a frame from Picamera2
    frame = picam2.capture_array()
    if frame is not None:
        print("Frame read successfully.")
        # Convert the frame to RGB 
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)

        results = model(frame_rgb)
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
        filename = now.strftime('%Y%m%d %H:%M:%S') + ".jpg"
        cv2.imwrite(filename, annotated_frame)

        # # Break the loop if 'q' is pressed
        # if cv2.waitKey(1) & 0xFF == ord("q"):
        #     break
    else:
        print("Error: Frame not read successfully.")

    picam2.stop()
    # cv2.destroyAllWindows()