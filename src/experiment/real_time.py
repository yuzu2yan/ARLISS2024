import cv2
import numpy as np
from picamera2 import Picamera2, Preview
from ultralytics import YOLO

# YOLOv8モデルをロード
try:
    model = YOLO('./best.pt')
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    exit()

# Picamera2を初期化
picam2 = Picamera2()
config = picam2.create_preview_configuration()
picam2.configure(config)
picam2.start()

# ビデオフレームをループ
while True:
    # フレームを取得
    frame = picam2.capture_array()

    if frame is not None:
        # フレームをRGBに変換（4チャンネルから3チャンネルへ）
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

        # YOLOv8推論をフレームに適用
        try:
            results = model(frame_rgb)
            print("Inference successful.")
        except Exception as e:
            print(f"Error during inference: {e}")
            break

        # 結果をフレームに可視化
        annotated_frame = results[0].plot()

        # アノテートされたフレームを表示
        cv2.imshow("YOLOv8 Inference", annotated_frame)

        # 'q' キーが押されたらループを抜ける
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        print("Error: Frame not read successfully.")
        break

# Picamera2とウィンドウを解放
picam2.stop()
cv2.destroyAllWindows()
print("Camera stopped and windows closed.")
