import os
import time
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
from dotenv import load_dotenv
load_dotenv()

subscription_key = os.environ.get('IMAGE_KEY')
endpoint = os.environ.get('IMAGE_ENDPOINT')


def image2text(input_path, output_path, language='en'):
    """
    Converts a handwritten image file to a text file
    :param input_path: location of the image file
    :param output_path: location of the text file
    :param language: language of the image file
    :return: None
    """
    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

    read_response = computervision_client.read_in_stream(input_path, raw=True, language=language)

    read_operation_location = read_response.headers["Operation-Location"]

    operation_id = read_operation_location.split("/")[-1]

    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in ['notStarted', 'running']:
            break
        time.sleep(1)

    if read_result.status == OperationStatusCodes.succeeded:
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                with open(output_path, "a", encoding='utf-8') as data:
                    data.write(f"{line.text}\n")
