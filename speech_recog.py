import streamlit as st
import speech_recognition as sr
import nltk
import random
import string

# Download NLTK data if not already present
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)

from nltk.stem import WordNetLemmatizer

# Load and preprocess chatbot data
def load_corpus(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        raw = f.read().lower()
    return nltk.sent_tokenize(raw)

def preprocess(sentence):
    lemmatizer = WordNetLemmatizer()
    tokens = nltk.word_tokenize(sentence.lower())
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in string.punctuation]
    return tokens

def chatbot_response(user_input, sentences):
    user_tokens = preprocess(user_input)
    best_score = 0
    best_sentence = "I'm sorry, I don't understand."
    for sentence in sentences:
        sentence_tokens = preprocess(sentence)
        score = len(set(user_tokens) & set(sentence_tokens))
        if score > best_score:
            best_score = score
            best_sentence = sentence
    return best_sentence

def transcribe_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Speak now...")
        audio = r.listen(source)
        st.info("Transcribing...")
        try:
            text = r.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I could not understand the audio."
        except sr.RequestError as e:
            return f"API error: {e}"
        except Exception as e:
            return f"An error occurred: {e}"

def main():
    st.title("Speech-Enabled Chatbot")
    st.write("Type your message or use your microphone to talk to the chatbot.")

    # Load chatbot data
    sentences = load_corpus("chatbot_corpus.txt")  # Make sure this file exists

    input_mode = st.radio("Choose input mode:", ("Text", "Speech"))

    user_input = ""
    if input_mode == "Text":
        user_input = st.text_input("You:")
        if st.button("Send") and user_input:
            response = chatbot_response(user_input, sentences)
            st.write("Bot:", response)
    else:
        if st.button("Speak"):
            user_input = transcribe_speech()
            st.write("You (transcribed):", user_input)
            if user_input and "Sorry" not in user_input and "error" not in user_input.lower():
                response = chatbot_response(user_input, sentences)
                st.write("Bot:", response)

if __name__ == "__main__":
    main()import streamlit as st
import speech_recognition as sr
import nltk
import random
import string

# Download NLTK data if not already present
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)

from nltk.stem import WordNetLemmatizer

# Load and preprocess chatbot data
def load_corpus(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        raw = f.read().lower()
    return nltk.sent_tokenize(raw)

def preprocess(sentence):
    lemmatizer = WordNetLemmatizer()
    tokens = nltk.word_tokenize(sentence.lower())
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in string.punctuation]
    return tokens

def chatbot_response(user_input, sentences):
    user_tokens = preprocess(user_input)
    best_score = 0
    best_sentence = "I'm sorry, I don't understand."
    for sentence in sentences:
        sentence_tokens = preprocess(sentence)
        score = len(set(user_tokens) & set(sentence_tokens))
        if score > best_score:
            best_score = score
            best_sentence = sentence
    return best_sentence

def transcribe_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Speak now...")
        audio = r.listen(source)
        st.info("Transcribing...")
        try:
            text = r.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I could not understand the audio."
        except sr.RequestError as e:
            return f"API error: {e}"
        except Exception as e:
            return f"An error occurred: {e}"

def main():
    st.title("Speech-Enabled Chatbot")
    st.write("Type your message or use your microphone to talk to the chatbot.")

    # Load chatbot data
    sentences = load_corpus("chatbot_corpus.txt")  # Make sure this file exists

    input_mode = st.radio("Choose input mode:", ("Text", "Speech"))

    user_input = ""
    if input_mode == "Text":
        user_input = st.text_input("You:")
        if st.button("Send") and user_input:
            response = chatbot_response(user_input, sentences)
            st.write("Bot:", response)
    else:
        if st.button("Speak"):
            user_input = transcribe_speech()
            st.write("You (transcribed):", user_input)
            if user_input and "Sorry" not in user_input and "error" not in user_input.lower():
                response = chatbot_response(user_input, sentences)
                st.write("Bot:", response)

if __name__ == "__main__":
    main()
