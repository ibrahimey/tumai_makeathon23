import os
import time
from model.audio2text import audio2text
from model.image2text import image2text
from model.text_translation import text_translation
# from model.pdf_generator import *
from model.helpers import upload_blob, download_blob, delete_blob, write2txt, input2wav
from dotenv import load_dotenv
load_dotenv()

import argparse


def convert2txt(input_file, input_type, language):
    """
    generate a txt file translated to english from the given text, audio or image
    :param input_file: input to translate
    :param input_type: type of the input
    :param language: language of the input
    :return: None
    """

    if input_type == "text":
        upload_blob(input_file, "input.txt")
        # os.remove("output_text.txt")
        text_translation(language)
        download_blob("text.txt", "input.txt")
        delete_blob("input.txt", "in")
        delete_blob("input.txt", "out")

    elif input_type == "audio":
        input2wav(input_file, 'audio.wav')
        audio2text('audio.wav', "output_audio.txt", language=f"{language}-{language.upper()}")
        upload_blob("output_audio.txt", "input.txt")
        os.remove("output_audio.txt")
        os.remove("audio.wav")
        text_translation(language)
        flag = True
        count = 0
        while flag and count < 20:
            try:
                download_blob("audio.txt", "input.txt")
                flag = False
                count += 1
            except:
                time.sleep(1)
        download_blob("audio.txt", "input.txt")
        delete_blob("input.txt", "in")
        delete_blob("input.txt", "out")

    elif input_type == "image":
        image2text(input_file, "output_image.txt")
        upload_blob("output_image.txt", "input.txt")
        os.remove("output_image.txt")
        text_translation(language)
        flag = True
        count = 0
        while flag and count < 20:
            try:
                download_blob("image.txt", "input.txt")
                flag = False
                count += 1
            except:
                time.sleep(1)
        download_blob("image.txt", "input.txt")
        delete_blob("input.txt", "in")
        delete_blob("input.txt", "out")

    elif input_type == 'str':
        write2txt(input_file, 'output_str.txt')
        upload_blob("output_str.txt", "input.txt")
        os.remove("output_str.txt")
        text_translation(language)
        flag = True
        count = 0
        while flag and count < 20:
            try:
                download_blob("str.txt", "input.txt")
                flag = False
                count += 1
            except:
                time.sleep(1)
        download_blob("str.txt", "input.txt")
        delete_blob("input.txt", "in")
        delete_blob("input.txt", "out")
