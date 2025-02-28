# Healthcare-AI-Translation-App

# 🌍 Breaking Language Barriers in Healthcare with Real-Time AI Translation!

This innovative project empowers seamless communication between **patients and healthcare providers** by offering **real-time, multilingual speech-to-text translation**.  

Powered by **cutting-edge Generative AI**, it ensures:
- ✅ **Accurate** translations  
- 🔒 **Secure** interactions  
- 🎯 **User-friendly** experience  

🌟 Bridging language gaps and enhancing **patient care globally**! 🌍



## 📋 Key Features  

### 🎙️ Speech-to-Text  
- Captures speech input via **audio file upload**.  
- Utilizes **AssembleAI Speech Recognition** for accurate transcription in the selected language.  

### 🌐 Real-time Translation  
- Translates text between **13 languages** using **Google Translate**.  
- Handles diverse linguistic needs with **precision**.  

### 🔊 Text-to-Speech with Encryption  
- Converts translated text to **audio output** using **gTTS (Google Text-to-Speech)**.  
- Encrypts audio files for **secure storage and playback**.  

### 🔒 Data Security  
- Uses **Fernet encryption protocol** to secure audio files.  
- **Automatically decrypts files** for playback and removes encrypted files **post-use**.  

### 🖥️ Streamlit-based Interface  
- **Intuitive web app** with customizable language settings.  
- **Mobile-compatible** for on-the-go usage.  



## 🛠️ Technical Details  

### 🚀 Technology Stack  

#### 🎨 Frontend  
- **Streamlit** → Used for creating the user interface.  

#### ⚙️ Backend  
- **Python** → Core logic of the application.  

#### 🔗 APIs  
- 📝 **AssemblyAI** → Used for transcription.  
- 🌍 **Groq** → Handles translation.  
- 🔊 **gTTS** → Converts text to speech.  

#### 🔒 Security  
- **Fernet encryption** (from the cryptography library) → Secures audio files.  


## 🔄 Data Flow  

1️⃣ **Audio Upload** → 🎙️ **AssemblyAI Transcription** → 📝 **Display Transcript**  

2️⃣ **User Selects Languages** → 🌍 **Groq Translation** → 📜 **Display Translation**  

3️⃣ **Google TTS Creates Audio** → 🔒 **Encrypt** → 📂 **Store Temporarily**  

4️⃣ **User Clicks "Play Audio"** → 🔓 **Decrypt Audio** → 🔊 **Playback** → 🧹 **Clean Up** 



## 🔒 Security  

- 🔑 **API keys** are securely stored in **environment variables**.  
- 🛡️ **Temporary file encryption** ensures data protection.  
- 🧹 **File cleanup** is performed after use to maintain security and efficiency. 

## 🚀 User Guide  

### 1️⃣ Upload Audio  
- Click the upload area and select an **MP3** or **WAV** file.  
- Your audio will be **transcribed automatically**.  

### 2️⃣ Select Languages  
- Choose your **input language** (spoken in the audio).  
- Choose your **desired output language**.  

### 3️⃣ Translate  
- Click **"Translate & Generate Audio"**.  
- View **original and translated text** side by side.  

### 4️⃣ Listen  
- Click the **"🔊 Play audio"** button to hear the translation. 


## 🛠️ Technical Notes  

- 🏥 The **translation prompt** is optimized for **medical terminology**.  
- ⚠️ **Error handling** is implemented for both **transcription** and **TTS**.  
- 🖥️ The app uses **standard Streamlit components** for UI elements.  

