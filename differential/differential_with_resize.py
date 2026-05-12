import streamlit as st
import cv2
import numpy as np
from io import BytesIO

# --- ページ設定 ---
st.set_page_config(page_title="画像加工ツール", layout="wide")
st.title('🖼️ 画像加工ツール')

# --- 処理用関数 ---

def apply_transformation(image_bgr):
    """画像にエッジ抽出風の変換を適用する"""
    image_gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY) 
    blurred = cv2.GaussianBlur(image_gray, (5, 5), 0)
    laplacian = cv2.Laplacian(blurred, cv2.CV_8U, ksize=5)
    laplacian = cv2.convertScaleAbs(laplacian)
    _, thresholded = cv2.threshold(laplacian, 127, 255, cv2.THRESH_BINARY_INV)
    median = cv2.medianBlur(image_bgr, 15) 
    thresholded_bgr = cv2.cvtColor(thresholded, cv2.COLOR_GRAY2BGR)
    return cv2.addWeighted(src1=thresholded_bgr, alpha=0.2, src2=median, beta=0.8, gamma=0)

# --- メインUI ---

uploaded_file = st.file_uploader("画像をアップロードしてください", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    original_image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    h, w, _ = original_image.shape

    # サイドバー：設定
    st.sidebar.header("加工設定")
    
    # 1. リサイズテンプレート設定
    st.sidebar.subheader("1. サイズ設定")
    
    # テンプレートの定義
    presets = {
        "カスタム (手入力)": (w, h),
        "1920 × 1080 (Full HD)": (1920, 1080),
        "1280 × 720 (HD)": (1280, 720),
        "1080 × 1080 (正方形)": (1080, 1080)
    }
    
    selected_preset = st.sidebar.selectbox("テンプレートを選択", list(presets.keys()))
    preset_w, preset_h = presets[selected_preset]

    # 数値入力（テンプレートを選ぶとここが自動で書き換わります）
    new_w = st.sidebar.number_input('幅 (px)', min_value=1, value=preset_w)
    new_h = st.sidebar.number_input('高さ (px)', min_value=1, value=preset_h)
    
    # 2. 変換ON/OFF設定
    st.sidebar.subheader("2. 特殊効果")
    do_transform = st.sidebar.checkbox('イラスト風変換を適用する', value=True)
    
    output_name = st.sidebar.text_input('保存ファイル名', value="processed_image.png")

    if st.button('処理を実行'):
        with st.spinner('処理中...'):
            # リサイズ
            processed_img = cv2.resize(original_image, (new_w, new_h))
            
            # 変換の適用
            if do_transform:
                processed_img = apply_transformation(processed_img)
            
            # 結果表示
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("元の画像")
                st.image(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB), use_container_width=True)
            with col2:
                st.subheader(f"処理後 ({new_w}x{new_h})")
                st.image(cv2.cvtColor(processed_img, cv2.COLOR_BGR2RGB), use_container_width=True)
            
            # ダウンロード
            st.markdown("---")
            is_success, buffer = cv2.imencode(".png", processed_img)
            if is_success:
                st.download_button(label="処理後の画像をダウンロード", data=buffer.tobytes(), file_name=output_name, mime="image/png")
else:
    st.info('画像をアップロードして「処理を実行」ボタンを押してください。')