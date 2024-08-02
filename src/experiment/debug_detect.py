import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('../../model/yolo.pt')

# Open the video file
cap = cv2.VideoCapture(0)

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 inference on the frame
        results = model(frame)

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Display the annotated frame
        cv2.imshow("YOLOv8 Inference", annotated_frame)

        if len(results[0].boxes) != 0:
                
            bounding_boxes = results[0].boxes.xyxy
            central_x = (bounding_boxes[0][0] + bounding_boxes[0][2]) / 2
            percent = int(100 * results[0].boxes.conf)
            print("percent:", percent)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()