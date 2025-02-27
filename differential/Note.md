# 画像をイラスト風に変換するプログラム
## 概要
入力された画像を、ラプラシアンフィルタやメディアンフィルタで処理し、イラスト風の画像に変換する。

## 開発の経緯・ストーリー
ラムダ技術部さんの動画（https://youtu.be/GZMJuuOKPrc?si=cgvVjBiMBlavYCbT）を参考に、大学の講義で習った画像処理を用いてPythonで実装してみようと思い、制作した。

## プログラム
### test-laplacian.ipynb
ラプラシアンフィルタの引数の試行。試行錯誤の結果、今回の場合は、ddepthはcv2.CV_8U、ksizeは5が最適だろうと判断した。

### try_differential.ipynb
Jupyter Notebookの形式で仮実装。プログラムの流れを確認し、本実装で行うことを確認した。

### differential.py
本実装。入力の画像と出力先をユーザに入力してもらうことで、汎用性をもたせた。

### 変換前後の画像
変換前の画像はすべて制作者が撮影したものである。
- 20241130_101421.jpg → output.jpg
- 20250111_122040.jpg → output2.jpg
- 20241123_115226.jpg → darumado.jpg

## 今後の展望
- 使いやすいユーザーインターフェイスを実装する

## 参考文献
- https://www.youtube.com/watch?v=GZMJuuOKPrc
- https://www.codevace.com/py-opencv-laplacian/
- https://www.codevace.com/py-opencv-threshold/
- https://pystyle.info/opencv-median-filter/
- https://www.kikagaku.co.jp/kikagaku-blog/python-opencv/
- https://udemy.benesse.co.jp/development/python-work/opencv.html