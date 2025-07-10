import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import av
import queue
import wave
import io
import speech_recognition as sr

# Set up an audio queue
audio_queue = queue.Queue()

# Custom Audio Processor for webrtc
class AudioProcessor:
    def recv(self, frame: av.AudioFrame):
        # Convert to raw bytes
        audio = frame.to_ndarray().tobytes()
        audio_queue.put(audio)
        return frame

# Convert raw bytes to a WAV audio stream for recognition
def get_wav_audio(audio_bytes, sample_rate=48000, sample_width=2, channels=1):
    buffer = io.BytesIO()
    with wave.open(buffer, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_bytes)
    buffer.seek(0)
    return buffer

# Transcribe function using SpeechRecognition
def transcribe(language):
    recognizer = sr.Recognizer()
    audio_bytes = b"".join(list(audio_queue.queue))
    audio_queue.queue.clear()

    if not audio_bytes:
        return "🎙️ No audio received yet. Please speak before clicking."

    wav_buffer = get_wav_audio(audio_bytes)

    with sr.AudioFile(wav_buffer) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio, language=language)
    except sr.UnknownValueError:
        return "🤷 Sorry, I could not understand the audio"
    except sr.RequestError as e:
        return f"❌ API error: {e}"

# Streamlit interface
def main():
    st.title("🎤 Simple Speech-to-Text App")
    st.caption("Microphone is on. Speak, then click 'Transcribe'.")

    language = st.selectbox("Choose Language", ["en-US", "fr-FR"])

    # Start mic recording via webrtc
    webrtc_streamer(
        key="speech-demo",
        mode=WebRtcMode.SENDONLY,
        audio_processor_factory=AudioProcessor,
        media_stream_constraints={"video": False, "audio": True},
    )

    # Transcribe on button click
    if st.button("📝 Transcribe"):
        text = transcribe(language)
        st.write("📄 Transcription:", text)

if __name__ == "__main__":
    main()
