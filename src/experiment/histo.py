import cv2
import numpy as np
from matplotlib import pyplot as plt


# 画像を読み込む
img = cv2.imread('./clahe.jpg')

# 画像のヒストグラムを描画
plt.hist(img.ravel(),256,[0,256])
plt.savefig('histogram1.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 平均を計算
mean = np.mean(gray)
print("Mean:", mean)

