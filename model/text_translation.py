import os
import requests

endpoint = os.getenv("TRANSLATOR_ENDPOINT")
key = os.getenv("TRANSLATOR_KEY")
path = 'translator/text/batch/v1.0/batches'
constructed_url = endpoint + path
sourceSASUrl = os.getenv("SOURCE_SAS_URL")
targetSASUrl = os.getenv("TARGET_SAS_URL")
from dotenv import load_dotenv
load_dotenv()


def text_translation(language):
    """
    Translates all the documents in the source blob to the target language and outputs to target blob
    :param language: language of the input documents
    :return: None
    """
    body = {
        "inputs": [
            {
                "source": {
                    "sourceUrl": sourceSASUrl,
                    "storageSource": "AzureBlob",
                    "language": language
                },
                "targets": [
                    {
                        "targetUrl": targetSASUrl,
                        "storageSource": "AzureBlob",
                        "category": "general",
                        "language": "en"
                    }
                ]
            }
        ]
    }
    headers = {
      'Ocp-Apim-Subscription-Key': key,
      'Content-Type': 'application/json',
    }

    _ = requests.post(constructed_url, headers=headers, json=body)
