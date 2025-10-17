# pip install streamlit
# pip install openai
# pip install sounddevice
# pip install wavio
# pip install python-dotenv

import streamlit as st      # 웹 애플리케이션 구축용 라이브러리
from openai import OpenAI   # OpenAI API 클라이언트
import sounddevice as sd    # 오디오 녹음용 라이브러리
import wavio                # 오디오 파일 입출력 라이브러리
import os                   # 파일 시스템 조작용 라이브러리
import time                 # 시간 지연 및 측정용 라이브러리
from dotenv import load_dotenv  # 환경 변수 로드용 라이브러리

# 환경 변수 로드 (.env 파일에서 OPENAI_API_KEY 읽기)
load_dotenv()

# OpenAI 클라이언트 초기화
# API 키는 환경 변수 OPENAI_API_KEY에서 자동으로 읽어옴
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 오디오 녹음 설정
duration = 10  # 녹음 지속 시간 (초)
fs = 44100     # 샘플링 레이트 (Hz) - CD 품질의 오디오

# 녹음된 오디오를 저장할 파일 경로
# OpenAI Whisper API는 여러 형식을 지원 (MP3는 파일 크기가 작아 효율적)
audio_file = "recording.mp3"
# 오디오 녹음 함수
# Streamlit 인터페이스
st.title("음성 인식 및 번역 앱")

# 오디오를 녹음하는 함수
def record_audio(duration, fs, file_path):
    st.info("녹음 중...")  # 사용자에게 녹음 중임을 알림

    # sounddevice를 사용하여 오디오 녹음 시작
    # duration * fs: 총 샘플 수, channels=1: 모노 녹음 (음성 인식에 적합)
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)

    # 녹음 진행 상황을 시각적으로 표시하는 프로그레스 바
    progress_bar = st.progress(0)
    for i in range(duration):
        time.sleep(1)  # 1초 대기
        # 진행도 업데이트 (0부터 1까지의 값)
        progress_bar.progress((i + 1) / duration)

    sd.wait()  # 녹음이 끝날 때까지 대기

    # 녹음된 오디오를 파일로 저장
    # sampwidth=2: 16비트 오디오 품질
    wavio.write(file_path, recording, fs, sampwidth=2)
    st.success("녹음 완료!")  # 녹음 완료 메시지 표시

# OpenAI Whisper API를 사용하여 오디오를 문자로 변환하는 함수
def transcribe_audio(file_path):
    st.info("변환 중...")
    
    try:
        # 오디오 파일을 열어서 OpenAI Whisper API로 전송
        with open(file_path, "rb") as audio_file:
            # OpenAI의 Whisper API를 사용하여 음성을 텍스트로 변환
            # model="whisper-1": OpenAI의 Whisper 모델 사용
            # language="ko": 한국어로 인식 (선택사항, 자동 감지도 가능)
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="ko"  # 한국어 설정 (필요시 제거하면 자동 감지)
            )
        
        st.success("변환 완료!")  # 변환 완료 메시지 표시
        return transcript.text
    
    except Exception as e:
        # API 호출 중 오류 발생 시 에러 메시지 표시
        st.error(f"변환 중 오류 발생: {str(e)}")
        return None


if st.button("녹음 시작"):
    record_audio(duration, fs, audio_file)  # 버튼 클릭 시 녹음 함수 호출


# 녹음된 파일이 존재하면 오디오 플레이어와 변환 옵션 표시
if os.path.exists(audio_file):
    # 녹음된 오디오를 재생할 수 있는 플레이어 표시
    st.audio(audio_file, format='audio/mp3')

    # 오디오를 텍스트로 변환하는 버튼
    if st.button("음성을 텍스트로 변환"):
        # 버튼 클릭 시 오디오를 텍스트로 변환
        transcription = transcribe_audio(audio_file)
        
        # 변환 결과가 있으면 텍스트 영역에 표시
        if transcription:
            st.text_area("변환 결과", transcription, height=200)