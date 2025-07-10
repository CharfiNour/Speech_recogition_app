import streamlit as st
import speech_recognition as sr

def transcribe_speech(api, language):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Speak now...")
        audio_text = r.listen(source)
        st.info("Transcribing...")

        try:
            if api == "Google":
                text = r.recognize_google(audio_text, language=language)
            elif api == "Sphinx":
                text = r.recognize_sphinx(audio_text, language=language)
            else:
                text = "API not supported."
            return text
        except sr.UnknownValueError:
            return "Sorry, I could not understand the audio."
        except sr.RequestError as e:
            return f"API error: {e}"
        except Exception as e:
            return f"An error occurred: {e}"

def main():
    st.title("Speech Recognition App")
    st.write("Select options and click 'Start Recording':")

    api = st.selectbox("Choose API", ["Google", "Sphinx"])
    language = st.selectbox("Choose Language", ["en-US", "fr-FR"])

    if st.button("Start Recording"):
        text = transcribe_speech(api, language)
        st.write("Transcription:", text)
        if text and "Sorry" not in text and "error" not in text.lower():
            if st.button("Save to File"):
                with open("transcription.txt", "w", encoding="utf-8") as f:
                    f.write(text)
                st.success("Saved to transcription.txt")

if __name__ == "__main__":
    main()
