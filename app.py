"""
Whisper 음성/비디오 변환 Streamlit 앱
- 오디오 파일 (mp3, wav, m4a 등) 업로드 및 텍스트 변환
- 비디오 파일 (mp4, avi, mov 등) 업로드 및 오디오 추출 후 텍스트 변환
"""

import streamlit as st
import whisper
import os
import tempfile
from pathlib import Path
import subprocess

# 페이지 설정
st.set_page_config(
    page_title="Whisper 음성/비디오 변환기",
    page_icon="🎤",
    layout="wide"
)

# 세션 상태 초기화
if 'model' not in st.session_state:
    st.session_state.model = None

@st.cache_resource
def load_whisper_model(model_name):
    """Whisper 모델 로드 (캐싱)"""
    return whisper.load_model(model_name)

def extract_audio_from_video(video_path, output_audio_path):
    """
    비디오 파일에서 오디오 추출
    ffmpeg를 사용하여 mp4 등의 비디오 파일에서 오디오를 추출합니다.
    """
    try:
        # ffmpeg 명령어로 오디오 추출
        command = [
            'ffmpeg',
            '-i', video_path,  # 입력 비디오 파일
            '-vn',  # 비디오 스트림 제외
            '-acodec', 'pcm_s16le',  # 오디오 코덱
            '-ar', '16000',  # 샘플링 레이트
            '-ac', '1',  # 모노 채널
            '-y',  # 기존 파일 덮어쓰기
            output_audio_path
        ]
        
        # ffmpeg 실행
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        st.error(f"오디오 추출 중 오류 발생: {e.stderr.decode()}")
        return False
    except FileNotFoundError:
        st.error("ffmpeg가 설치되어 있지 않습니다. conda install ffmpeg -c conda-forge 명령어로 설치해주세요.")
        return False

def transcribe_audio(model, audio_path, language=None):
    """
    오디오 파일을 텍스트로 변환
    """
    try:
        # 언어 설정
        if language and language != "자동 감지":
            result = model.transcribe(audio_path, language=language)
        else:
            result = model.transcribe(audio_path)
        
        return result
    except Exception as e:
        st.error(f"변환 중 오류 발생: {str(e)}")
        return None

# 메인 UI
st.title("🎤 Whisper 음성/비디오 변환기")
st.markdown("---")

# 사이드바 설정
with st.sidebar:
    st.header("⚙️ 설정")
    
    # 모델 선택
    model_option = st.selectbox(
        "Whisper 모델 선택",
        ["tiny", "base", "small", "medium", "large"],
        index=1,  # base가 기본값
        help="모델이 클수록 정확도가 높지만 처리 시간이 오래 걸립니다."
    )
    
    # 언어 선택
    language_option = st.selectbox(
        "언어 선택",
        ["자동 감지", "ko", "en", "ja", "zh", "es", "fr", "de"],
        help="자동 감지를 선택하면 Whisper가 자동으로 언어를 감지합니다."
    )
    
    st.markdown("---")
    st.markdown("""
    ### 📝 지원 파일 형식
    **오디오**: mp3, wav, m4a, flac, ogg, wma
    
    **비디오**: mp4, avi, mov, mkv, wmv
    """)
    
    st.markdown("---")
    st.markdown("""
    ### 💡 모델 크기 정보
    - **tiny**: 가장 빠름, 낮은 정확도
    - **base**: 빠름, 적당한 정확도 (권장)
    - **small**: 보통, 좋은 정확도
    - **medium**: 느림, 높은 정확도
    - **large**: 가장 느림, 최고 정확도
    """)

# 모델 로드
if st.session_state.model is None or st.session_state.get('current_model') != model_option:
    with st.spinner(f'{model_option} 모델 로딩 중...'):
        st.session_state.model = load_whisper_model(model_option)
        st.session_state.current_model = model_option
    st.success(f'{model_option} 모델이 로드되었습니다!')

# 파일 업로드
uploaded_file = st.file_uploader(
    "오디오 또는 비디오 파일을 업로드하세요",
    type=['mp3', 'wav', 'm4a', 'flac', 'ogg', 'wma', 'mp4', 'avi', 'mov', 'mkv', 'wmv'],
    help="지원되는 오디오/비디오 파일을 업로드하세요"
)

if uploaded_file is not None:
    # 파일 정보 표시
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"📁 파일명: {uploaded_file.name}")
    with col2:
        file_size = uploaded_file.size / (1024 * 1024)  # MB로 변환
        st.info(f"📊 크기: {file_size:.2f} MB")
    with col3:
        file_extension = Path(uploaded_file.name).suffix.lower()
        file_type = "비디오" if file_extension in ['.mp4', '.avi', '.mov', '.mkv', '.wmv'] else "오디오"
        st.info(f"🎬 타입: {file_type}")
    
    # 변환 버튼
    if st.button("🚀 변환 시작", type="primary", use_container_width=True):
        # 임시 파일 생성
        with tempfile.TemporaryDirectory() as temp_dir:
            # 업로드된 파일 저장
            input_path = os.path.join(temp_dir, uploaded_file.name)
            with open(input_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            
            # 비디오 파일인 경우 오디오 추출
            if file_type == "비디오":
                st.info("📹 비디오 파일에서 오디오 추출 중...")
                audio_path = os.path.join(temp_dir, "extracted_audio.wav")
                
                with st.spinner("오디오 추출 중..."):
                    if not extract_audio_from_video(input_path, audio_path):
                        st.stop()
                
                st.success("✅ 오디오 추출 완료!")
            else:
                audio_path = input_path
            
            # 음성을 텍스트로 변환
            st.info("🎤 음성을 텍스트로 변환 중...")
            
            # 프로그레스 바 표시
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            with st.spinner("변환 중... 파일 크기에 따라 시간이 걸릴 수 있습니다."):
                progress_bar.progress(30)
                status_text.text("모델 처리 중...")
                
                # 언어 설정
                lang = None if language_option == "자동 감지" else language_option
                result = transcribe_audio(st.session_state.model, audio_path, lang)
                
                progress_bar.progress(100)
                status_text.text("변환 완료!")
            
            if result:
                st.success("✅ 변환이 완료되었습니다!")
                
                # 결과 표시
                st.markdown("---")
                st.subheader("📝 변환 결과")
                
                # 감지된 언어 표시
                if 'language' in result:
                    detected_lang = result['language']
                    st.info(f"🌐 감지된 언어: {detected_lang}")
                
                # 변환된 텍스트 표시
                st.text_area(
                    "변환된 텍스트",
                    value=result['text'],
                    height=300,
                    help="변환된 텍스트를 복사할 수 있습니다."
                )
                
                # 다운로드 버튼
                st.download_button(
                    label="📥 텍스트 파일로 다운로드",
                    data=result['text'],
                    file_name=f"{Path(uploaded_file.name).stem}_transcript.txt",
                    mime="text/plain"
                )
                
                # 세그먼트 정보 표시 (선택사항)
                with st.expander("🔍 상세 정보 보기"):
                    st.json({
                        "언어": result.get('language', 'N/A'),
                        "세그먼트 수": len(result.get('segments', [])),
                        "전체 텍스트 길이": len(result['text'])
                    })
                    
                    # 세그먼트별 표시
                    if 'segments' in result and result['segments']:
                        st.markdown("### 타임스탬프별 텍스트")
                        for segment in result['segments']:
                            start_time = segment['start']
                            end_time = segment['end']
                            text = segment['text']
                            st.markdown(f"**[{start_time:.2f}s - {end_time:.2f}s]** {text}")

else:
    # 안내 메시지
    st.info("👆 위의 파일 업로더를 사용하여 오디오 또는 비디오 파일을 업로드하세요.")
    
    # 사용 예시
    with st.expander("📖 사용 방법"):
        st.markdown("""
        1. 사이드바에서 원하는 Whisper 모델을 선택하세요
        2. 언어를 선택하세요 (자동 감지 권장)
        3. 오디오 또는 비디오 파일을 업로드하세요
        4. '변환 시작' 버튼을 클릭하세요
        5. 변환된 텍스트를 확인하고 다운로드하세요
        
        **참고**: 
        - 비디오 파일의 경우 자동으로 오디오를 추출합니다
        - 파일 크기가 클수록 처리 시간이 오래 걸립니다
        - 첫 실행 시 모델 다운로드로 인해 시간이 걸릴 수 있습니다
        """)
