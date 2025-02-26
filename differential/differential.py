import cv2
import matplotlib.pyplot as plt
import numpy as np

print("変換する画像ファイルを入力してください")
image = input("画像：")

print("出力先を入力してください")
output = input("出力先:")

print("")
print("画像:", image)
print("出力先:", output)
print("Confirm? y/n")
A = input()

assert A == "y", "Try Again"

image_gray = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
# ガウシアンフィルターを適用してノイズを削除
blurred = cv2.GaussianBlur(image_gray, (5, 5), 0)
# ラプラシアンフィルタ
laplacian = cv2.Laplacian(blurred, cv2.CV_8U, ksize=5)
# 絶対値を取得
laplacian = cv2.convertScaleAbs(laplacian)
# 閾値処理を行う
retval, thresholded = cv2.threshold(laplacian, 127, 255, cv2.THRESH_BINARY_INV)
#print(retval)

image = cv2.imread(image)
#メディアンフィルタ
median = cv2.medianBlur(image, 15) 

# 画像を結合
thresholded = cv2.cvtColor(thresholded, cv2.COLOR_GRAY2BGR)
blended = cv2.addWeighted(src1=thresholded, alpha=0.2, src2=median, beta=0.8, gamma=0)

plt.imshow(cv2.cvtColor(blended, cv2.COLOR_BGR2RGB))
plt.show()

print("Confirm? y/n")
B = input()

if B == "y":
    #画像の出力
    cv2.imwrite(output, blended)
    print('output.')

print("Finish")