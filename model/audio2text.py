import os
import time
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
load_dotenv()

subscription = os.environ.get('SPEECH_KEY')
region = os.environ.get('SPEECH_REGION')


def write_to_txt(file_path, line):
    with open(file_path, "a", encoding='utf-8') as data:
        data.write(f"{line}\n")


def audio2text(input_path, output_path, language='en-EN'):
    """
    Performs continuous speech recognition with input from an audio file to a text file
    :param input_path: location of the audio file
    :param output_path: location of the text file
    :param language: language of the audio file
    :return: None
    """
    speech_config = speechsdk.SpeechConfig(subscription=subscription, region=region)
    speech_config.speech_recognition_language = language
    audio_config = speechsdk.audio.AudioConfig(filename=input_path)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    done = False

    def stop_cb(evt: speechsdk.SessionEventArgs):
        nonlocal done
        done = True

    speech_recognizer.recognized.connect(lambda evt: write_to_txt(output_path, evt.result.text))
    speech_recognizer.session_stopped.connect(stop_cb)

    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)

    speech_recognizer.stop_continuous_recognition()
