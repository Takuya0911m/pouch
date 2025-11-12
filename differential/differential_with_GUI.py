import streamlit as st
from PIL import Image
import cv2
import matplotlib.pyplot as plt
import numpy as np
import io

st.title('画像変換')
st.text('')

# 初期化
if "image_data" not in st.session_state:
    st.session_state.image_data = None
if 'blended' not in st.session_state:
    st.session_state.blended = None

# ディスクアクセスを避け、インメモリで処理
@st.cache_data
def process_image(image_data):
    """
    画像バイナリデータを受け取り、処理した画像を返す
    """
    # アップロードされたバイナリデータをnumpy配列に変換し、OpenCVで読み込み
    nparr = np.frombuffer(image_data, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR) # BGR形式で読み込み

    # グレースケール変換
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 

    # ガウシアンフィルターを適用してノイズを削除
    blurred = cv2.GaussianBlur(image_gray, (5, 5), 0)
    # ラプラシアンフィルタ
    laplacian = cv2.Laplacian(blurred, cv2.CV_8U, ksize=5)
    laplacian = cv2.convertScaleAbs(laplacian)
    retval, thresholded = cv2.threshold(laplacian, 127, 255, cv2.THRESH_BINARY_INV)
    
    # メディアンフィルタ
    median = cv2.medianBlur(image, 15) 

    # 画像を結合
    thresholded = cv2.cvtColor(thresholded, cv2.COLOR_GRAY2BGR)
    blended = cv2.addWeighted(src1=thresholded, alpha=0.2, src2=median, beta=0.8, gamma=0)
    
    return blended

def create_download_link(image_np, filename):
    """結果画像をPNGとしてエンコードし、ダウンロードボタンを生成"""
    # cv2.imencodeでメモリ上にPNGデータを作成
    is_success, buffer = cv2.imencode(".png", image_np)
    if is_success:
        st.download_button(
            label="結果をダウンロード",
            data=buffer.tobytes(),
            file_name=filename,
            mime="image/png",
            help=f"処理後の画像を'{filename}'としてダウンロードします"
        )
    else:
        st.error("画像のエンコードに失敗しました。")

# --- Streamlit UI ---

input_file = st.file_uploader("変換する画像ファイルを選択", type=['png', 'jpeg', 'jpg'])
if input_file is not None:
    st.markdown(f'**{input_file.name}** をアップロードしました.')
    
    # 画像バイナリデータをセッションに保存
    st.session_state.image_data = input_file.read() 
    
    # アップロード画像を表示 (PILを使用)
    img = Image.open(io.BytesIO(st.session_state.image_data)) # io.BytesIOでメモリから読み込み
    st.image(img, caption='アップロードされた画像')

# ダウンロードファイル名の入力
st.text_input('ダウンロードファイル名', key='output_filename', value="converted_image.png")

if st.button('実行'):
    if st.session_state.image_data is not None:
        with st.spinner('処理中...'):
            st.session_state.blended = process_image(st.session_state.image_data)
        
        st.info("変換後の画像を確認してください")
        
        # OpenCV (BGR) を Streamlit/Matplotlib (RGB) に変換して表示
        image_rgb = cv2.cvtColor(st.session_state.blended, cv2.COLOR_BGR2RGB)
        st.image(image_rgb, caption='変換後の画像')
        
        # ダウンロードボタンの表示
        create_download_link(st.session_state.blended, st.session_state.output_filename)

    else:
        st.error('画像をアップロードしてから「実行」ボタンを押してください。')