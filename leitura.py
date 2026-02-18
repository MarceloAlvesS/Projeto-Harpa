import serial
import time
import pandas as pd
COMPort = "COM10"
bandwidth = 9600

l1 = []
l2 = []
l3 = []
l4 = []
l5 = []
l6 = []

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
                    l1.append(data[0])
                    l2.append(data[1])
                    l3.append(data[2])
                    l4.append(data[3])
                    l5.append(data[4])
                    l6.append(data[5])
                    
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
        
maximo = len(l6)
l1 = l1[:maximo]
l2 = l2[:maximo]
l3 = l3[:maximo]
l4 = l4[:maximo]
l5 = l5[:maximo]
l6 = l6[:maximo]

tabela = pd.DataFrame()

tabela['l1'] = l1
tabela['l2'] = l2
tabela['l3'] = l3
tabela['l4'] = l4
tabela['l5'] = l5
tabela['l6'] = l6

tabela.to_csv('leitura.csv')
