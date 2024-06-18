import numpy as np
import cv2

gamma = 0.5
input_img = cv2.imread('./clahe.jpg')

output_float = 255 * np.power(input_img / 255, gamma) # 計算結果をいったん実数型(float)で保持
output_float.astype(np.uint8)

cv2.imwrite('gamma.jpg', output_float) # 画像を書き出す