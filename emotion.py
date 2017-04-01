
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

TEST_IMG = "http://static2.businessinsider.com/image/5087f99369bedd394700000d/obama-press-conference-obamacare-sad.jpg"


def ms_emotion_api(file_binary_str=None):
    """Upload single file as octet-stream in request body.
    file: binary stream
    """
    headers = {"Ocp-Apim-Subscription-Key": MS_API_KEY}
    if file_binary_str is None:
        data = {"url": TEST_IMG}
        req = requests.post(MS_API_URL, headers=headers, json=data)
    else:
        headers["Content-Type"] = "application/octet-stream"
        req = requests.post(MS_API_URL, headers=headers, data=file_binary_str)
    if req.status_code != requests.codes.ok:
        pprint(req.request.headers)
        print(req.status_code)
        pprint(req.headers)
        pprint(req.json())
        return
    return req.json()


def best_fit_emotion(file_binary_str=None):
    """
    `file` passed directly to ms_emotion_apai
    """
    res = ms_emotion_api(file_binary_str)
    if not res:
        return None
    # use the first person in the image: res[0]
    scores = sorted(res[0]["scores"].items(), key=lambda d: d[1], reverse=True)
    # use the emotion with highest score: scores[0]
    return {
        scores[0][0]: scores[0][1]  # emotion -> score
    }
