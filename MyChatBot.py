import cohere
import speech_recognition as sr
from gtts import gTTS
import playsound
import os
import uuid

co = cohere.Client("9Mxsrkyno2H7JanxxmiN8050B0duLCq9kIAbprVG")  

def text_to_audio(text):
    tts = gTTS(text=text, lang='ar')
    filename = f"response_{uuid.uuid4()}.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

def audio_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(" تحدث الآن...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language='ar-SA')
        print(" قلت:", text)
        return text
    except sr.UnknownValueError:
        print(" لم أفهم الصوت.")
        return None
    except sr.RequestError:
        print("⚠️ حدث خطأ في خدمة التعرف على الصوت.")
        return None

def generate_response(prompt):
    print(" يتم إنشاء الرد...")
    response = co.chat(
        model="command-r-plus",  
        message=prompt,
        temperature=0.7,
        chat_history=[
            {"role": "SYSTEM", "message": "الرجاء الرد دائمًا باللغة العربية فقط."}
        ]
    )
    reply = response.text.strip()
    print(" الرد:", reply)
    return reply

def main():
    while True:
        user_input = audio_to_text()
        if user_input:
            ai_reply = generate_response(user_input)
            text_to_audio(ai_reply)

if __name__ == "__main__":
    main()
