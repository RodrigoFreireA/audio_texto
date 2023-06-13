import tkinter as tk
from tkinter import filedialog
import speech_recognition as sr

def converter_audio():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])

    if file_path:
        r = sr.Recognizer()
        with sr.AudioFile(file_path) as source:
            audio = r.record(source)

        try:
            text = r.recognize_google(audio, language="pt-BR")
            print("Texto reconhecido:")
            print(text)
        except sr.UnknownValueError:
            print("Não foi possível reconhecer o áudio.")
        except sr.RequestError as e:
            print("Erro na requisição ao serviço de reconhecimento de fala: {0}".format(e))

converter_audio()
