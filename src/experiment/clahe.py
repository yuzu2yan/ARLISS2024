import cv2
import numpy as np
from matplotlib import pyplot as plt


img = cv2.imread("./dark.jpg") # 画像を読み込む

img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV) # RGB => YUV(YCbCr)
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8)) # claheオブジェクトを生成
img_yuv[:,:,0] = clahe.apply(img_yuv[:,:,0]) # 輝度にのみヒストグラム平坦化
img = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR) # YUV => RGB
cv2.imwrite("clahe.jpg", img) # 書き出す

