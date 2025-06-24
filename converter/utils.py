import os
import subprocess
from yt_dlp import YoutubeDL
from pydub import AudioSegment
import librosa
import soundfile as sf
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Informando ffmpeg e ffprobe para pydub
AudioSegment.converter = os.path.join(BASE_DIR, "bin", "ffmpeg")
AudioSegment.ffprobe = os.path.join(BASE_DIR, "bin", "ffprobe")

def baixar_audio(url):
    ydl_opts = {
        'ffmpeg_location': os.path.join(BASE_DIR, "bin", "ffmpeg"),  # ✔️ Corrigido para Render
        'format': 'bestaudio/best',
        'outtmpl': 'media/%(title)s.%(ext)s',
        'noplaylist': True,
        'cookiefile': os.path.join(BASE_DIR, 'converter', 'cookies.txt'),  # ✔️ Caminho absoluto
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url)
        filename = f"media/{info['title']}.mp3"
        return filename


def alterar_tom(caminho_audio, semitons):
    print("ffmpeg path:", AudioSegment.converter)
    print("ffprobe path:", AudioSegment.ffprobe)
    try:
        res = subprocess.run([AudioSegment.ffprobe, "-version"], capture_output=True, text=True, check=True)
        print("ffprobe output:", res.stdout)
    except Exception as e:
        print("Erro ao executar ffprobe:", e)

    y, sr = librosa.load(caminho_audio, sr=None)
    y_shifted = librosa.effects.pitch_shift(y=y, sr=sr, n_steps=semitons)

    novo_nome = caminho_audio.replace(".mp3", f"_pitch_{semitons}.mp3")
    sf.write(novo_nome, y_shifted, sr, format="MP3")
    return novo_nome
