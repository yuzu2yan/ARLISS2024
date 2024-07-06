import cv2
import datetime
from picamera2 import Picamera2
from yolov5 import YOLOv5

# YOLOv5のnanoモデルを読み込む
model = YOLOv5('./best.pt')

# Picamera2の初期化
picam2 = Picamera2()
config = picam2.create_preview_configuration()
picam2.configure(config)
picam2.start()

def process_frame():
    # Get a frame from Picamera2
    frame = picam2.capture_array()

    if frame is not None:
        # Convert the frame to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)

        results = model(frame_rgb)

        # Annotate the frame with the results
        annotated_frame = results.render()[0]
        
        result_object = results.pandas().xyxy[0]

        # Get the bounding box positions
        bounding_boxes = result_object[['xmin', 'ymin', 'xmax', 'ymax']].values

        # Get the class IDs
        class_ids = result_object['class'].values

        # Get the class names
        class_names_dict = results.names

        for box, class_id in zip(bounding_boxes, class_ids):
            class_name = class_names_dict[int(class_id)]
            print(f"Box coordinates: {box}, Object: {class_name}")

        # Save the annotated frame
        now = datetime.datetime.now()
        filename = now.strftime('%Y%m%d %H:%M:%S') + ".jpg"
        cv2.imwrite(filename, annotated_frame)
    else:
        print("Error: Frame not read successfully.")

if __name__ == "__main__":
    process_frame()
