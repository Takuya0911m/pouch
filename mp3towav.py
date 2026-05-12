import streamlit as st
from pydub import AudioSegment

if "data" not in st.session_state:
    st.session_state.data = None

@st.cache_data
def process(data, output):
    sound = AudioSegment.from_file(data, format="mp3")
    return sound.export(output, format="wav")

input_file = st.file_uploader("変換する音声ファイルを選択", type='mp3')
if input_file is not None:
    st.markdown(f'**{input_file.name}** をアップロードしました.')
    st.session_state.data = input_file.read() 

st.text_input('ダウンロードファイル名', key='output_filename', value="audio.wav")

if st.button('実行'):
    if st.session_state.data is not None:
        with st.spinner('処理中...'):
            conversion = process(st.session_state.data, st.session_state.output_filename)
        st.download_button(
            label='ダウンロード',
            data=conversion,
            file_name=st.session_state.output_filename
        )