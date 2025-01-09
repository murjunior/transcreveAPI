from flask import Flask, request
from flask_cors import CORS
import speech_recognition as sr
from pydub import AudioSegment
import io
import logging
from datetime import datetime

app = Flask(__name__)

CORS(app, origins="https://seu-site.com.br")

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

@app.route('/', methods=['GET'])
def home():
    return '{"message":"Forbidden"}'

@app.route('/transcrever', methods=['POST'])
def transcrever():
    request_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if 'audio' not in request.files:
        logging.error(f"{request_time} - Nenhum arquivo de áudio enviado.")
        return 'Nenhum arquivo de áudio enviado', 400

    audio_file = request.files['audio']
    if not audio_file:
        logging.error(f"{request_time} - Arquivo de áudio inválido.")
        return 'Arquivo de áudio inválido', 400

    # Converte qualquer arquivo de áudio para WAV
    try:
        audio = AudioSegment.from_file(io.BytesIO(audio_file.read()))
        audio = audio.set_frame_rate(22050).set_channels(1)  # Ajuste conforme necessário
        wav_io = io.BytesIO()
        audio.export(wav_io, format='wav')
        wav_io.seek(0)
        audio_file = wav_io

        # Inicializa o reconhecedor de fala
        recognizer = sr.Recognizer()

        # Abre o arquivo de áudio com o SpeechRecognition
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
        
        # Utiliza a função recognize_google para transcrever o áudio em texto
        transcribed_text = recognizer.recognize_google(audio_data, language='pt-BR')
        
        logging.info(f"{request_time} - Transcrição bem-sucedida: {transcribed_text}")
        return transcribed_text, 200

    except sr.UnknownValueError:
        logging.error(f"{request_time} - Não foi possível reconhecer o áudio.")
        return 'Não foi possível reconhecer o áudio', 400
    except sr.RequestError as e:
        logging.error(f"{request_time} - Erro ao se comunicar com o serviço de reconhecimento de fala: {e}")
        return 'Erro ao se comunicar com o serviço de reconhecimento de fala', 500
    except Exception as e:
        logging.error(f"{request_time} - Erro inesperado: {e}")
        return 'Erro interno no servidor', 500
