# Whisper로 로컬 오디오 파일을 텍스트로 변환
# pip install openai-whisper numpy==1.23.5
# conda install ffmpeg -c conda-forge

import whisper
import os

# medium : | 13.7M/1.42G
def transcribe_audio(audio_path):
    # Whisper 모델 로드 (여기서는 'base' 모델 사용)
    model = whisper.load_model("base")

    # 오디오 파일 transcribe
    print("음성을 텍스트로 변환 중...")
    result = model.transcribe(audio_path)

    # 결과 출력
    print("\n변환 결과:")
    print(result["text"])

# 로컬 오디오 파일 경로 지정
audio_file = "아로하.mp3"

# 파일 존재 여부 확인
if not os.path.exists(audio_file):
    print(f"오류: '{audio_file}' 파일을 찾을 수 없습니다.")
    print("파일이 현재 작업 디렉토리에 있는지 확인해 주세요.")
else:
    # 오디오 파일 변환
    transcribe_audio(audio_file)