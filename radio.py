import tkinter as tk
import threading
import sounddevice as sd
import datetime
import os
import wave
import logging

# Configurações de gravação
segment_duration = 30  # Duração de cada segmento em segundos (1 minuto)
sample_rate = 48000  # Taxa de amostragem em Hz
output_folder = "gravacoes/"  # Pasta onde os arquivos de áudio serão salvos

# Variáveis de controle
stop_recording = False
is_recording = False

# Configurar o log
log_file = "log.txt"
logging.basicConfig(filename=log_file, level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Função para iniciar a gravação
def start_recording():
    global stop_recording, is_recording
    if not is_recording:
        stop_recording = False
        is_recording = True
        threading.Thread(target=record_audio).start()

# Função para parar a gravação
def stop_recording_func():
    global stop_recording, is_recording
    if is_recording:
        stop_recording = True
        is_recording = False

# Função para finalizar o programa
def exit_program():
    window.quit()
    window.destroy()

# Função para gravar o áudio
def record_audio():
    # Obter a data e hora atual
    now = datetime.datetime.now()

    # Cria uma pasta com o nome da data atual para salvar os arquivos de áudio
    folder_name = now.strftime("%Y-%m-%d")
    folder_path = output_folder + folder_name + "/"
    os.makedirs(folder_path, exist_ok=True)

    segment_start = now

    while not stop_recording:
        segment_end = segment_start + datetime.timedelta(seconds=segment_duration)

        # Verificar se a hora atual ultrapassou o limite de 24 horas
        if segment_end > now + datetime.timedelta(hours=24):
            break

        # Capturar o áudio reproduzido no sistema
        logging.info(f"Gravando segmento: {segment_start} - {segment_end}")
        try:
            audio = sd.rec(int(segment_duration * sample_rate), samplerate=sample_rate, channels=2)
            sd.wait()

            # Nome do arquivo baseado no horário de início do segmento
            filename = segment_start.strftime("%H-%M-%S") + ".wav"
            output_file = folder_path + filename

            # Salvar o áudio em um arquivo WAV
            wave_file = wave.open(output_file, 'wb')
            wave_file.setnchannels(2)
            wave_file.setsampwidth(2)
            wave_file.setframerate(sample_rate)
            wave_file.writeframes(audio.tobytes(order='C'))
            wave_file.close()

        except Exception as e:
            logging.error(f"Erro durante a gravação: {e}")

        # Atualizar a hora de início do próximo segmento
        segment_start = segment_end

    show_message()

# Função para exibir a mensagem de tarefa concluída
def show_message():
    print("Tarefa concluída.")

# Função para executar o outro script
def run_script():
    os.system("converte_audio_texto.py")

# Criar a janela principal
window = tk.Tk()
window.title("Gravação de Áudio")
window.geometry("200x200")

# Botões
start_button = tk.Button(window, text="Iniciar Gravação", command=start_recording)
start_button.pack(pady=10)

stop_button = tk.Button(window, text="Parar Gravação", command=stop_recording_func)
stop_button.pack(pady=10)

script_button = tk.Button(window, text="Converter para Texto", command=run_script)
script_button.pack(pady=10)

exit_button = tk.Button(window, text="Sair", command=exit_program)
exit_button.pack(pady=10)

# Executar a janela
window.mainloop()
