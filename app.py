from dotenv import load_dotenv
import os
from google import genai
from gtts import gTTS
import streamlit as st 
import pandas as pd 
from pypdf import PdfReader
load_dotenv()
api_key =os.getenv("GEMINI_API_KEY")
client=genai.Client(api_key=api_key)

import streamlit as st 
st.title("Edureka Capstone Project - Language Translator")
text_to_translate =st.text_area("Enter the text you want to translate")
uploaded_file = st.file_uploader("Or upload a text file",type=["txt","pdf","csv","xlsx","xls"])
if uploaded_file is not None:
    if uploaded_file.type =="text/plain":
        text_to_translate = uploaded_file.read().decode("utf-8")
    elif uploaded_file.type =="text/csv":
        dataframe = pd.read_csv(uploaded_file)
        text_to_translate =dataframe.to_string(index=False)
    elif uploaded_file.name.endswith(".xlsx") or uploaded_file.name.endswith(".xls") : 
        dataframe = pd.read_excel(uploaded_file)
        text_to_translate =dataframe.to_string(index=False)
    elif uploaded_file.type =="application/pdf":
        pdf_reader = PdfReader(uploaded_file)
        text_to_translate =""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_to_translate+=page_text+"\n"
st.text_area("File Contents",text_to_translate,height=200)
target_language =  st.selectbox(
    "Choose the language",
    ["Spanish","French","Hindi","German","Italian"])
language_codes ={"Spanish": "es","French": "fr", "Hindi" : "hi", "German": "de", "Italian": "it"}
if st.button("Translate"):
  response =client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents=f"Translate the following text into{target_language}. Return only the translated text, with no explanation, no transliteration, and no extra words:{text_to_translate}")
  st.write(response.text)
  tts = gTTS(text=response.text,lang=language_codes[target_language])
  tts.save("translation.mp3")
  st.audio("translation.mp3")
  with open("translation.mp3","rb") as audio_file:st.download_button("Download Audio",audio_file,file_name="translation.mp3")