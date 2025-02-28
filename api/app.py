import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from cryptography.fernet import Fernet
import openai
import tempfile
import assemblyai as aai
from gtts import gTTS
import os

from dotenv import load_dotenv
load_dotenv()

# Load API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") 
aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
ASSEMBLYAI_API_KEY = aai.settings.api_key

# Initialize LangChain LLM
llm = ChatGroq(model="gemma2-9b-it", temperature=0.2, api_key=GROQ_API_KEY)

# Encryption Key
KEY_FILE = "secret.key"
if os.path.exists(KEY_FILE):
    with open(KEY_FILE, "rb") as key_file:
        encryption_key = key_file.read()
else:
    encryption_key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(encryption_key)

cipher = Fernet(encryption_key)

# Language Mapping
LANGUAGES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "zh": "Chinese",
    "ar": "Arabic",
    "hi": "Hindi",
    "it": "Italian",
    "pt": "Portuguese",
    "ru": "Russian",
    "ja": "Japanese",
    "ko": "Korean",
    "tr": "Turkish"
}

# Streamlit UI
st.title("Healthcare Translation Web App with Generative AI")
st.markdown("### 🎙️ Speak, Translate, & Listen with Groq + Assemble AI + Google TTS")

# **🔹 Speech-to-Text (Using Whisper)**
st.subheader("🎤 Record Speech")
audio_file = st.file_uploader("Upload an audio file (MP3/WAV)", type=["mp3", "wav"])

spoken_text = ""
translated_text = ""

if audio_file:
    st.audio(audio_file, format="audio/mp3")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        temp_audio.write(audio_file.read())
        temp_audio_path = temp_audio.name #get file path.

    # Transcribe with AssemblyAI
    transcriber = aai.Transcriber()

    try:
        transcript = transcriber.transcribe(temp_audio_path)

        if transcript.status == aai.TranscriptStatus.error:
            st.error(f"Transcription Error: {transcript.error}")
            print(f"AssemblyAI Error: {transcript.error}")
        else:
            st.success("🎙️ **Original Transcript:**")
            st.write(transcript.text)
            spoken_text = transcript.text # spoken text is assigned here.
            st.session_state["spoken_text"] = spoken_text # store in session state
    except Exception as e:
        st.error(f"Speech Recognition Failed: {str(e)}")
        print(f"General Error: {e}")

    os.remove(temp_audio_path) #cleanup
else:
    if "spoken_text" in st.session_state:
        spoken_text = st.session_state["spoken_text"] #retrieve from session state
    else:
        spoken_text = "" #set default value.
    

# **🔹 Translation**
st.subheader("🌍 Translate")
input_lang = st.selectbox("Input Language", options=LANGUAGES.keys(), format_func=lambda x: LANGUAGES[x])
output_lang = st.selectbox("Output Language", options=LANGUAGES.keys(), format_func=lambda x: LANGUAGES[x])

prompt_template = PromptTemplate(
    input_variables=["text", "input_lang", "output_lang"],
    template="Translate the following text from {input_lang} to {output_lang}. Ensure accuracy for medical terms and do not give any comment after translating.\n\nText: {text}\nTranslation:"
)


        # ** TTS Implementation**
def synthesize_speech(translated_text, lang_code="en"):
        # Extract the text from AIMessage
        text_to_synthesize = translated_text.content if hasattr(translated_text, "content") else str(translated_text)
    
        tts = gTTS(text_to_synthesize, lang=lang_code)
    
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            tts.save(temp_audio.name)
    
        # Encrypt the generated audio file
        with open(temp_audio.name, "rb") as file:
            encrypted_data = cipher.encrypt(file.read())
    
        encrypted_path = temp_audio.name + ".enc"
        with open(encrypted_path, "wb") as file:
            file.write(encrypted_data)
    
        return encrypted_path  # Return encrypted file path


if st.button("Translate & Generate Audio"):
      if st.session_state.get("spoken_text"): #use session state
        spoken_text = st.session_state["spoken_text"] #get spoken text.
        try:
            # Translate using Groq
            translated_text = llm.invoke(prompt_template.format(text=spoken_text, input_lang=input_lang, output_lang=output_lang))

            # **🔹 Dual Transcript Display**
            col1, col2 = st.columns(2)
            with col1:
                st.info("📜 **Original Transcript**")
                st.write(spoken_text)

            with col2:
                st.success("🌎 **Translated Transcript**")
                st.write(translated_text)

            # **🔹 Generate Audio**
            encrypted_audio_path = synthesize_speech(translated_text, lang_code=output_lang)
            st.session_state["encrypted_audio"] = encrypted_audio_path #store audio path.
            st.success("Translation and audio generation complete.")

        except Exception as e:
            st.error(f"Translation/TTS Error: {e}")
            print(f"Translation/TTS Error details: {e}") #debug


if translated_text:
        encrypted_audio_path = synthesize_speech(translated_text, lang_code=output_lang)
        st.session_state["encrypted_audio"] = encrypted_audio_path #store path in session state
        st.success("Translation and audio generation complete.")
# else:
#         st.warning("Please provide audio to translate.")

if "encrypted_audio" in st.session_state:
    if st.button("🔊 Play Audio"): #add play button
        encrypted_audio_path = st.session_state["encrypted_audio"]
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as decrypted_audio:
            with open(encrypted_audio_path, "rb") as enc_file:
                encrypted_data = enc_file.read()
            with open(decrypted_audio.name, "wb") as dec_file:
                dec_file.write(cipher.decrypt(encrypted_data))
            st.audio(decrypted_audio.name, format="audio/mp3")
            os.remove(encrypted_audio_path) #cleanup
