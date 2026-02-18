import serial
import time
import pygame

COMPort = "COM10"
bandwidth = 9600

pygame.mixer.init()
pygame.mixer.set_num_channels(6)  # permite até 6 sons simultâneos

# Carregar sons
sons = {
     "16": pygame.mixer.Sound("do.mp3"),
     "17": pygame.mixer.Sound("re.mp3"),
     "5": pygame.mixer.Sound("mi.mp3"),
     "18": pygame.mixer.Sound("fa.mp3"),
     "19": pygame.mixer.Sound("sol.mp3"),
     "12": pygame.mixer.Sound("la.mp3"),
}

try:
    arduino = serial.Serial(COMPort, bandwidth, timeout=1) # Timeout para não bloquear indefinidamente
    print(f"Conectado a {COMPort}...")
except serial.SerialException as e:
    print(f"Erro ao abrir a porta serial {COMPort}: {e}")
    exit()

print("Aguardando dados do Arduino...")

try:
    while True:
        if arduino.in_waiting > 0:
            try:
                data = arduino.readline().decode('latin1').strip().split()
                if not data:
                    continue # Ignora linhas vazias

                if(data == "Err"):
                    print("Unexpected BMP Error")
                else:
                    print(data)
                    nota = data[-1]
                    if nota in sons:
                        sons[nota].play()
            except ValueError:
                print(f"Erro ao converter dado: '{data}'. Linha ignorada.")
            except Exception as e:
                print(f"Ocorreu um erro inesperado ao processar dados: {e}")

        time.sleep(0.01)

except KeyboardInterrupt:
    print("\nInterrompido pelo usuário.")
finally:
    if arduino.is_open:
        arduino.close()
        print("Porta serial fechada.")