from flask import Flask, request, send_file
from PIL import Image
import requests
from io import BytesIO
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route('/merge', methods=['POST'])
def merge_images():
    app.logger.debug(f"Requisição recebida: {request.get_json()}")
    try:
        data = request.get_json()
        if not data or 'url1' not in data or 'url2' not in data:
            app.logger.error("JSON inválido ou faltando url1/url2")
            return "JSON inválido ou faltando url1/url2", 400
        url1 = data['url1']
        url2 = data['url2']
        app.logger.debug(f"Tentando baixar URL1: {url1}, URL2: {url2}")
        response1 = requests.get(url1)
        response2 = requests.get(url2)
        if response1.status_code != 200 or response2.status_code != 200:
            app.logger.error(f"Erro ao baixar imagens: URL1={response1.status_code}, URL2={response2.status_code}")
            return f"Erro ao baixar imagens: URL1={response1.status_code}, URL2={response2.status_code}", 400
        img1 = Image.open(BytesIO(response1.content))
        img2 = Image.open(BytesIO(response2.content))
        width = img1.width + img2.width
        height = max(img1.height, img2.height)
        merged = Image.new('RGB', (width, height))
        merged.paste(img1, (0, 0))
        merged.paste(img2, (img1.width, 0))
        buffer = BytesIO()
        merged.save(buffer, format='JPEG')
        buffer.seek(0)
        app.logger.debug("Imagem mesclada com sucesso")
        return send_file(buffer, mimetype='image/jpeg', as_attachment=True, download_name='merged.jpg')
    except Exception as e:
        app.logger.error(f"Erro no processamento: {str(e)}")
        return f"Erro: {str(e)}", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)