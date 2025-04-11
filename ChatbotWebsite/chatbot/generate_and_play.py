import os
from IPython.display import Audio
import pygame
import time
from datetime import datetime

def generate_audio(text, voice, output_file, rate="+0%"):
    command = f'edge-tts --voice "{voice}" --rate={rate} --text "{text}" --write-media "{output_file}"'
    os.system(command)
    print(f"Generated audio saved to {output_file}")

def play_audio_with_pygame(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(1)

def generate_and_play(messages):
    # 使用当前时间戳生成唯一文件名
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    
    directory = "audio_files"
    os.makedirs(directory, exist_ok=True)  # 创建目录（如果不存在）
    
    output_file = os.path.join(directory, f"answer_{timestamp}.mp3")

    generate_audio(messages, "en-US-JennyNeural", output_file)  # 生成音频
    play_audio_with_pygame(output_file)  # 播放音频