
import requests
import os
from pprint import pprint

MS_API_URL = "https://westus.api.cognitive.microsoft.com/emotion/v1.0/recognize"
if os.getenv("MS_API_KEY", None):
    MS_API_KEY = os.getenv("MS_API_KEY")
else:
    raise ValueError("MS API KEY not found")


"""
An example response from MS API:

[{'faceRectangle': {'height': 140, 'left': 532, 'top': 298, 'width': 140},
  'scores': {'anger': 0.00062697765,
             'contempt': 0.000190300314,
             'disgust': 0.000371130969,
             'fear': 0.00498573529,
             'happiness': 0.00302794622,
             'neutral': 0.9140529,
             'sadness': 0.0381836556,
             'surprise': 0.03856135}}]
"""


def ms_emotion_api():
    headers = {
        "Ocp-Apim-Subscription-Key": MS_API_KEY
    }
    data = {
        "url": "http://static2.businessinsider.com/image/5087f99369bedd394700000d/obama-press-conference-obamacare-sad.jpg"
    }
    req = requests.post(MS_API_URL, headers=headers, json=data)
    if req.status_code != requests.codes.ok:
        pprint(req.headers)
        pprint(req.json())
        return
    return req.json()


def best_fit():
    res = ms_emotion_api()
    if not res:
        return None
    # use the first person in the image: res[0]
    scores = sorted(res[0]["scores"].items(), key=lambda d: d[1], reverse=True)
    # use the emotion with highest score: scores[0]
    return {
        scores[0][0]: scores[0][1]  # emotion -> score
    }
