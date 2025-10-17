# OpenAI Whisper API를 사용한 음성 인식 앱

이 애플리케이션은 OpenAI의 Whisper API를 사용하여 음성을 녹음하고 텍스트로 변환합니다.

## 설치 방법

### 1. 필요한 패키지 설치

아나콘다 환경에서 다음 명령어를 실행하세요:

```bash
pip install -r requirements.txt
```

### 2. OpenAI API 키 설정

1. [OpenAI Platform](https://platform.openai.com/api-keys)에서 API 키를 발급받습니다.
2. 프로젝트 루트 디렉토리에 `.env` 파일을 생성합니다:

```bash
cp .env.example .env
```

3. `.env` 파일을 열어서 발급받은 API 키를 입력합니다:

```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

## 실행 방법

```bash
streamlit run openai_voice_ver.py
```

## 주요 기능

- **음성 녹음**: 10초 동안 음성을 녹음하여 WAV 파일로 저장
- **텍스트 변환**: OpenAI Whisper API를 사용하여 녹음된 음성을 텍스트로 변환
- **한국어 지원**: 한국어 음성 인식 최적화

## 주의사항

- OpenAI API 사용 시 비용이 발생할 수 있습니다.
- API 키는 절대 공개 저장소에 업로드하지 마세요.
- `.env` 파일은 `.gitignore`에 추가되어 있어야 합니다.

## 로컬 Whisper vs OpenAI API

### 로컬 Whisper (기존 버전)
- 장점: 무료, 오프라인 사용 가능
- 단점: 초기 모델 다운로드 필요, 높은 컴퓨팅 리소스 요구

### OpenAI API (현재 버전)
- 장점: 빠른 처리 속도, 낮은 로컬 리소스 사용, 최신 모델 자동 사용
- 단점: 인터넷 연결 필요, API 사용 비용 발생
