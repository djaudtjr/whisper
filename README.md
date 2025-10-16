# Whisper 음성/비디오 변환 Streamlit 앱

Whisper AI를 사용하여 오디오 및 비디오 파일을 텍스트로 변환하는 Streamlit 웹 애플리케이션입니다.

## 주요 기능

- 🎵 **오디오 파일 변환**: mp3, wav, m4a, flac, ogg, wma 등 다양한 오디오 형식 지원
- 🎬 **비디오 파일 변환**: mp4, avi, mov, mkv, wmv 등 비디오 파일에서 자동으로 오디오 추출 후 변환
- 🌐 **다국어 지원**: 한국어, 영어, 일본어, 중국어 등 자동 언어 감지
- 📊 **다양한 모델 선택**: tiny, base, small, medium, large 모델 중 선택 가능
- ⏱️ **타임스탬프**: 세그먼트별 타임스탬프와 함께 텍스트 제공
- 💾 **결과 다운로드**: 변환된 텍스트를 txt 파일로 다운로드

## 설치 방법

### 1. 필수 패키지 설치

아나콘다 환경에서 다음 명령어를 실행하세요:

```bash
# ffmpeg 설치 (비디오 파일 처리에 필요)
conda install ffmpeg -c conda-forge

# Python 패키지 설치
pip install -r requirements.txt
```

### 2. 개별 패키지 설치 (선택사항)

```bash
pip install streamlit
pip install openai-whisper
pip install numpy==1.23.5
```

## 실행 방법

```bash
streamlit run app.py
```

브라우저가 자동으로 열리며 `http://localhost:8501`에서 앱에 접속할 수 있습니다.

## 사용 방법

1. **모델 선택**: 사이드바에서 원하는 Whisper 모델을 선택합니다
   - tiny: 가장 빠름, 낮은 정확도
   - base: 빠름, 적당한 정확도 (권장)
   - small: 보통, 좋은 정확도
   - medium: 느림, 높은 정확도
   - large: 가장 느림, 최고 정확도

2. **언어 선택**: 자동 감지 또는 특정 언어를 선택합니다

3. **파일 업로드**: 오디오 또는 비디오 파일을 업로드합니다

4. **변환 시작**: '변환 시작' 버튼을 클릭합니다

5. **결과 확인**: 변환된 텍스트를 확인하고 필요시 다운로드합니다

## 지원 파일 형식

### 오디오 파일
- mp3, wav, m4a, flac, ogg, wma

### 비디오 파일
- mp4, avi, mov, mkv, wmv

## 주의사항

- 첫 실행 시 선택한 모델을 다운로드하므로 시간이 걸릴 수 있습니다
- 파일 크기가 클수록 처리 시간이 오래 걸립니다
- 비디오 파일 처리를 위해서는 ffmpeg가 반드시 설치되어 있어야 합니다
- 아나콘다 환경에서 실행하는 것을 권장합니다

## 문제 해결

### ffmpeg 관련 오류
```bash
conda install ffmpeg -c conda-forge
```

### numpy 버전 충돌
```bash
pip install numpy==1.23.5 --force-reinstall
```

### CUDA/GPU 사용 (선택사항)
GPU를 사용하려면 PyTorch CUDA 버전을 설치하세요:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

## 기술 스택

- **Streamlit**: 웹 인터페이스
- **OpenAI Whisper**: 음성 인식 AI 모델
- **FFmpeg**: 비디오/오디오 처리
- **PyTorch**: 딥러닝 프레임워크

## 라이선스

이 프로젝트는 개인 및 교육 목적으로 자유롭게 사용할 수 있습니다.
