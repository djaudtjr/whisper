# 실시간 마이크 입력 전사
# pip install sounddevice

import whisper
import sounddevice as sd
import numpy as np

# Whisper 모델 로드
model = whisper.load_model("small")  # base, small, medium, large, turbo

# 마이크로부터 입력 받기 위한 설정
duration = 10  # 녹음 시간 (초 단위)
sample_rate = 16000  # 샘플링 레이트

print("녹음 시작...")
audio = sd.rec(int(duration * sample_rate),
               samplerate=sample_rate, channels=1, dtype=np.float32)

sd.wait()  # 녹음 종료까지 대기
print("녹음 종료.")

# 음성을 텍스트로 변환
audio = np.squeeze(audio)
result = model.transcribe(audio)
print("인식된 텍스트:", result['text'])