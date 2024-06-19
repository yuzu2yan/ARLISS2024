import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
try:
    model = YOLO('./best.pt')
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    exit()

# Open the video file
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video capture.")
    exit()

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 inference on the frame
        try:
            results = model(frame)
            print("Inference successful.")
        except Exception as e:
            print(f"Error during inference: {e}")
            break

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Display the annotated frame
        cv2.imshow("YOLOv8 Inference", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        print("Error: Frame not read successfully.")
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
print("Video capture released and windows closed.")
