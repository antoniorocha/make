from flask import Flask, request
from PIL import Image
import requests
from io import BytesIO

app = Flask(__name__)

@app.route('/merge', methods=['POST'])
def merge_images():
    url1 = request.json['url1']
    url2 = request.json['url2']
    img1 = Image.open(BytesIO(requests.get(url1).content))
    img2 = Image.open(BytesIO(requests.get(url2).content))
    width = img1.width + img2.width
    height = max(img1.height, img2.height)
    merged = Image.new('RGB', (width, height))
    merged.paste(img1, (0, 0))
    merged.paste(img2, (img1.width, 0))
    merged.save('merged.jpg')
    return {'url': 'http://[seu-replit-url]/merged.jpg'}

app.run(host='0.0.0.0')