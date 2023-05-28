import streamlit as st
import time
from io import BytesIO
import streamlit.components.v1 as components
from st_custom_components import st_audiorec
import datetime
from model.model import convert2txt
from model.pdf_generator import pdf_generator
from model.summ_fun import magic_stuff

wav_audio_data, uploaded_file, text_input, picture_input, final_report = False, False, False, False, "report"

option = st.selectbox(
    'Select your language',
    ('🇬🇧English', '🇮🇹Italiano', '🇹🇷Türkçe', '🇪🇸Español'))

dic_langs = {'🇬🇧English': 'en', '🇮🇹Italiano': 'it', '🇪🇸Español': 'es', '🇹🇷Türkçe': 'tr'}

lang = dic_langs[option]

st.subheader("Select which formats you want to upload")

flags = [False, False, False, False]
functions_running = ['reading your file...', 'reading your input...',
                     'listening to your audio...', 'understanding your photo...']

uploaded_file = None
text_input = st.checkbox('Text')
audio_input = st.checkbox('Voice note')
camera_input = st.checkbox('Photo')

if text_input:
    text_input = st.text_area('Comments and report')
    if text_input:
        flags[1] = True

if audio_input:
    wav_audio_data = st_audiorec()
    if audio_input:
        flags[2] = True


if camera_input:
    picture_input = st.camera_input("Take a picture of notes")
    if camera_input:
        flags[3] = True


if st.button('Confirm upload'):
    if not wav_audio_data and not uploaded_file and not text_input and not picture_input:
        st.error('No data!', icon="🚨")
    else:
        progress_text = "Operation in progress. Please wait..."
        my_bar = st.progress(0, text=progress_text)
        all_text = []
        # call stuff
        print(lang)
        # TODO: remove print(lang) and combine outputs
        for percent_complete in range(len(flags)):
            if flags[percent_complete]:
                progress_text = functions_running[percent_complete]
                my_bar.progress(percent_complete*25, text=progress_text)
                if percent_complete == 0:
                    convert2txt(uploaded_file, 'text', lang)
                    with open("text.txt") as doc:
                        extracted = doc.read()
                        all_text.append(extracted)
                if percent_complete == 1:
                    convert2txt(text_input, 'str', lang)
                    with open("str.txt") as doc:
                        extracted = doc.read()
                        all_text.append(extracted)
                if percent_complete == 2:
                    convert2txt(wav_audio_data, 'audio', lang)
                    with open("audio.txt") as doc:
                        extracted = doc.read()
                        all_text.append(extracted)
                if percent_complete == 3:
                    convert2txt(picture_input, 'image', lang)
                    with open("image.txt") as doc:
                        extracted = doc.read()
                        all_text.append(extracted)
            else:
                pass
        my_bar.empty()
        final_report = "\n".join(all_text)
        with st.spinner('Processing...'):
#            final_report = magic_stuff(final_report)
            pdf_generator(final_report)
            time.sleep(1)
        st.success('Done!')

        with open("complex_report.pdf", "rb") as pdf_file:
            PDFbyte = pdf_file.read()

        st.download_button(label="Download report",
                    data=PDFbyte,
                    file_name="report.pdf",
                    mime='application/octet-stream')

else:
    st.write('Waiting for confirmation')
