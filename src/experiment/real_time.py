import cv2

# カメラを開く
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    # フレームを読み込む
    ret, frame = cap.read()

    if not ret:
        print("Error: Frame not read successfully.")
        break

    # フレームを表示
    cv2.imshow('Camera Test', frame)

    # 'q' キーが押されたらループを抜ける
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# リソースを解放
cap.release()
cv2.destroyAllWindows()
