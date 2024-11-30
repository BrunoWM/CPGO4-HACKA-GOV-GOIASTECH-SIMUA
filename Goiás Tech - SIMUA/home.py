from flask import Flask, render_template_string
import cv2
import time
import os
from datetime import datetime
from threading import Thread

app = Flask(__name__, static_folder='C:/Users/robot/Hackaton', static_url_path='/hackaton')

def capture_frames(url, output_folder, interval=2):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    while True:
        cap = cv2.VideoCapture(url)
        if not cap.isOpened():
            print("Erro ao abrir o vídeo.")
            return

        ret, frame = cap.read()
        if not ret:
            print("Falha ao capturar o vídeo; o stream pode ter terminado.")
            cap.release()
            break

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = os.path.join(output_folder, f'image_{timestamp}.png')
        cv2.imwrite(filename, frame)
        print(f'Imagem salva: {filename}')

        cap.release()
        time.sleep(interval)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Controle de Problemas Urbanos</title>
    <style>
        body, html {
            margin: 0;
            padding: 0;
            font-family: 'Arial', sans-serif;
            background-color: #002580; /* Dark blue background */
            color: #ffffff;
        }
        .sidebar {
            background-color: #01371b; /* Dark green */
            width: 200px; /* Sidebar width */
            height: 100vh; /* Full height */
            position: fixed;
            padding: 20px;
            box-sizing: border-box;
            overflow: auto;
        }
        .sidebar h3 {
            color: #f3e718; /* Yellow color for the category title */
            padding-bottom: 10px;
        }
        .button {
            display: block;
            background-color: #089653; /* Bright green */
            color: white;
            border: none;
            padding: 10px 15px;
            margin: 5px 0;
            width: 100%;
            text-align: left;
            border-radius: 4px;
            transition: background-color 0.3s;
            cursor: pointer;
        }
        .button:hover {
            background-color: #01371b; /* Darker green when hovering */
        }
        .main-content {
            margin-left: 200px; /* Equal to sidebar width */
            padding: 20px;
        }
        .video-container {
            background-color: #8dc8aa; /* Light green for video background */
            border-radius: 8px;
            padding: 10px;
            margin-bottom: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.3);
        }
        iframe {
            width: 100%;
            height: 500px; /* Larger height for video */
            border-radius: 8px;
            border: none;
        }
    </style>
</head>
<body>
    <div class="sidebar">
        <h3>Ocorrências</h3>
        <div onclick="window.location.href='/buracos'" class="button">Buraco no Asfalto</div>
        <div onclick="window.location.href='/bueiros_abertos'" class="button">Bueiro</div>
        <div onclick="window.location.href='/matagal'" class="button">Vegetação irregular</div>
        <div onclick="window.location.href='/matagal'" class="button">Cabos de energia</div>
        <div onclick="window.location.href='/matagal'" class="button">Entulho</div>
        <div onclick="window.location.href='/matagal'" class="button">Animais na pista</div>
    </div>
    <div class="main-content">
        <div class="video-container">
            <iframe src="http://172.20.10.2:8080/video" id="videoStream" alt="Live Stream"></iframe>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)



@app.route('/buracos')
def buracos():
    files_folder = 'C:/Users/robot/Hackaton/buracos'
    files = os.listdir(files_folder)
    images_html = '<div style="background-color: #089653; padding: 20px;">'
    images_html += '<h1 style="color: #f3e718; text-align: center;">Buracos no Asfalto</h1>'
    for file in files:
        file_path = os.path.join('/hackaton/buracos', file)
        file_name, _ = os.path.splitext(file)
        images_html += f'''
        <div style="background-color: #01371b; display: flex; align-items: center; margin-bottom: 10px; padding: 10px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.3);">
            <img src="{file_path}" style="max-width: 200px; max-height: 150px; margin-right: 20px; border-radius: 5px;">
            <p style="color: #8dc8aa; flex: 1; margin: 0;">Localização: {file_name}</p>
        </div>
        '''
    images_html += '</div>'
    return images_html


@app.route('/bueiros_abertos')
def bueiros_abertos():
    files_folder = 'C:/Users/robot/Hackaton/bueiros_abertos'
    files = os.listdir(files_folder)
    images_html = '<div style="background-color: #089653; padding: 20px;">'
    images_html += '<h1 style="color: #f3e718; text-align: center;">Bueiros Abertos ou com Lixo</h1>'
    for file in files:
        file_path = os.path.join('/hackaton/bueiros_abertos', file)
        file_name, _ = os.path.splitext(file)
        images_html += f'''
        <div style="background-color: #01371b; display: flex; align-items: center; margin-bottom: 10px; padding: 10px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.3);">
            <img src="{file_path}" style="max-width: 200px; max-height: 150px; margin-right: 20px; border-radius: 5px;">
            <p style="color: #8dc8aa; flex: 1; margin: 0;">Localização: {file_name}</p>
        </div>
        '''
    images_html += '</div>'
    return images_html

@app.route('/matagal')
def matagal():
    files_folder = 'C:/Users/robot/Hackaton/mato_alto'
    files = os.listdir(files_folder)
    images_html = '<div style="background-color: #089653; padding: 20px;">'
    images_html += '<h1 style="color: #f3e718; text-align: center;">Vegetação irregular </h1>'
    for file in files:
        file_path = os.path.join('/hackaton/mato_alto', file)
        file_name, _ = os.path.splitext(file)
        images_html += f'''
       <div style="background-color: #01371b; display: flex; align-items: center; margin-bottom: 10px; padding: 10px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.3);">
            <img src="{file_path}" style="max-width: 200px; max-height: 150px; margin-right: 20px; border-radius: 5px;">
            <p style="color: #8dc8aa; flex: 1; margin: 0;">Localização: {file_name}</p>
        </div>
        '''
    images_html += '</div>'
    return images_html

@app.route('/copo')
def copo():
    files_folder = 'C:/Users/robot/Hackaton/copo'
    files = os.listdir(files_folder)
    images_html = '<div style="background-color: #089653; padding: 20px;">'
    images_html += '<h1 style="color: #f3e718; text-align: center;">copo</h1>'
    for file in files:
        file_path = os.path.join('/hackaton/copo', file)
        file_name, _ = os.path.splitext(file)
        images_html += f'''
       <div style="background-color: #01371b; display: flex; align-items: center; margin-bottom: 10px; padding: 10px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.3);">
            <img src="{file_path}" style="max-width: 200px; max-height: 150px; margin-right: 20px; border-radius: 5px;">
            <p style="color: #8dc8aa; flex: 1; margin: 0;">Localização: {file_name}</p>
        </div>
        '''
    images_html += '</div>'
    return images_html



#Obra de arte

def run_capture():
    VIDEO_URL = 'http://172.20.10.2:8080/video'
    OUTPUT_FOLDER = r'imgGrande'
    INTERVAL = 2
    capture_frames(VIDEO_URL, OUTPUT_FOLDER, INTERVAL)

if __name__ == '__main__':
    t = Thread(target=run_capture)
    t.start()
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
