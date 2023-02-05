import serial
from threading import Thread
from time import sleep
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
import sys

import matplotlib as mpl
mpl.rcParams["toolbar"] = "None"

plt.style.use("ggplot")

porta = "/dev/ttyUSB0"
baud_rate = 115200

fila = np.array([[], [], [], [], [], []]).astype(object)

def ler_dados():
    global fila, start
    try:
        disp = serial.Serial(porta, baud_rate)
        disp.reset_input_buffer()
        while disp.is_open:
            try:
                dado = disp.readline()
                dados1 = str(dado.decode('utf8')).rstrip("\n")
                dados1 = dados1.split(",")
                try:
                    dados_float = np.array([dados1], dtype="float64").T
                    if len(fila[0]) <= 51:
                        fila = np.append(fila, dados_float, axis=1)
                        print(fila)
                    else:
                        fila = np.delete(fila, np.s_[:1], 1)
                        # print(fila)
                except Exception as erro:
                    print(f"Erro: {erro}")
                sleep(0.03)
            except serial.SerialException:
                print("Erro de leitura ...")
                break
        if not disp.is_open:
            disp.close()
            print("Close ...")
    except serial.SerialException:
        print("Erro de conexão...")


new_thread = Thread(target=ler_dados)
new_thread.daemon = True
new_thread.start()

sleep(2)
fig, ax = plt.subplots(figsize=(10, 6))
plt.yticks(range(-12, 12, 2), label="m/s^2")
plt.xticks(range(0, 51, 2))
plt.subplots_adjust(bottom=0.11, top=0.935,
                    right=0.964, left=0.088)

plt.axhline(0, color='dimgray', lw=1)
plt.axvline(0, color='dimgray', lw=1)

x_data = np.linspace(0, 49, 50)
y_data = np.ones(50)
ln, = plt.plot(x_data, y_data, lw=0.9)
tx = ax.text(45, int(fila[0][-1])+1, f"{fila[0][-1]}",
             color=[0.3, 0.3, 0.5],
             fontsize=12,
             fontweight="bold")

plt.xlabel("Tempo (s)", color='dimgray',
           fontdict={
               'fontsize': 12,
               'fontweight': 'medium'
           },
           fontweight="bold")
plt.ylabel("Aceleração no Eixo X$(m/s^2)$", color='dimgray',
           fontdict={
               'fontsize': 12,
               'fontweight': 'medium'
           },
           fontweight="bold")


def init():
    ax.set_ylim(-12, 12)
    ax.set_title("Aceleração no Eixo X$\\bf(m/s^2)$",
                 fontdict={'fontsize': 18, 'fontweight': 'medium'},
                 fontweight="bold")
    tx.set_y(int(fila[0][-1]+1))
    tx.set_text(f"{fila[0][-1]}")
    return ln, tx


def Plot_Data(filaup):
    ln.set_data(x_data, fila[0][:50])
    ln.set_linestyle("-.")
    ln.set_marker(".")
    tx.set_y(int(fila[0][-1]+1))
    tx.set_text(f"{fila[0][-1]:.2f} m/s^2")
    return ln, tx


anima = animation.FuncAnimation(fig, Plot_Data, init_func=init, interval=30)
plt.show()
sys.exit()
