import cv2
import mediapipe as mp
import serial
import time
import platform
import serial.tools.list_ports

# Função para detectar a porta serial disponível
def detectar_porta_serial():
    portas = serial.tools.list_ports.comports()
    for p in portas:
        if 'USB' in p.description:  # Verifica se a descrição da porta contém 'USB'
            return p.device
    return None  # Retorna None se nenhuma porta USB for encontrada

# Detecta a plataforma
if platform.system() == 'Windows':
    porta_serial = detectar_porta_serial()
elif platform.system() == 'Linux':
    porta_serial = detectar_porta_serial()
else:
    print("Sistema operacional não suportado")
    exit()

if porta_serial is None:
    print("Nenhuma porta serial USB encontrada!")
    exit()

print(f"Usando a porta serial: {porta_serial}")

baud_rate = 9600  # Taxa de transmissão
ser = serial.Serial(porta_serial, baud_rate, timeout=1)

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

hands = mp.solutions.hands
Hands = hands.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils

def enviar_comando(pino, estado):
    # Envia comando via serial, formato: 'PINO:ESTADO'
    comando = f"{pino}:{estado}\n"
    ser.write(comando.encode())

while True:
    success, img = cap.read()
    if not success:
        print("Erro: Falha ao capturar frame")
        break

    frameRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = Hands.process(frameRGB)
    handPoints = results.multi_hand_landmarks
    h, w, _ = img.shape
    pontos = []

    if handPoints:
        for points in handPoints:
            mpDraw.draw_landmarks(img, points, hands.HAND_CONNECTIONS)

            for id, cord in enumerate(points.landmark):
                cx, cy = int(cord.x * w), int(cord.y * h)
                cv2.circle(img, (cx, cy), 4, (255, 0, 0), -1)
                pontos.append((cx, cy))

        if pontos:
            distPolegar = abs(pontos[17][0] - pontos[4][0])
            distIndicador = pontos[5][1] - pontos[8][1]
            distMedio = pontos[9][1] - pontos[12][1]
            distAnelar = pontos[13][1] - pontos[16][1]
            distMinimo = pontos[17][1] - pontos[20][1]

            # Controle do servo com base nas distâncias das falanges
            if distPolegar < 80:
                enviar_comando(10, 0)  # Fechar o polegar
            else:
                enviar_comando(10, 1)  # Abrir o polegar

            if distIndicador >= 1:
                enviar_comando(9, 1)  # Abrir indicador
            else:
                enviar_comando(9, 0)  # Fechar indicador

            if distMedio >= 1:
                enviar_comando(8, 1)  # Abrir médio
            else:
                enviar_comando(8, 0)  # Fechar médio

            if distAnelar >= 1:
                enviar_comando(7, 1)  # Abrir anelar
            else:
                enviar_comando(7, 0)  # Fechar anelar

            if distMinimo >= 1:
                enviar_comando(6, 1)  # Abrir mínimo
            else:
                enviar_comando(6, 0)  # Fechar mínimo

    cv2.imshow('Imagem', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
