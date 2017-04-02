
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


def ms_emotion_api(file_bytestr=None):
    """Upload single file as octet-stream in request body.
    file: binary stream
    """
    headers = {"Ocp-Apim-Subscription-Key": MS_API_KEY}
    if file_bytestr is None:
        data = {"url": TEST_IMG}
        req = requests.post(MS_API_URL, headers=headers, json=data)
    else:
        headers["Content-Type"] = "application/octet-stream"
        req = requests.post(MS_API_URL, headers=headers, data=file_bytestr)
    if req.status_code != requests.codes.ok:
        pprint(req.request.headers)
        print(req.status_code)
        pprint(req.headers)
        pprint(req.json())
        return None
    res = req.json()
    if not res:
        print(res)
        return None

    print(">>> MS EMOTION API RESULT")
    pprint(res)
    print("<<< END OF MS EMOTION API RESULT")
    # use the first person in the image: res[0]
    scores = sorted(res[0]["scores"].items(), key=lambda d: d[1], reverse=True)
    # use the emotion with highest score: scores[0]
    return {
        scores[0][0]: scores[0][1]  # emotion -> score
    }
