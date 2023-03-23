import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib
import time

import tkinter as Tk
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Modulos criados
from coleta_dados import ColetaDados

matplotlib.style.use("ggplot")
matplotlib.use('TkAgg')
ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

# Objeto para coletar dados do sensor
coleta_dados = ColetaDados()
time.sleep(1)


fig, ((ax1, ax2, ax3),
      (ax4, ax5, ax6)) = plt.subplots(2, 3,
                                      figsize=(11, 6), dpi=100)

fig.suptitle('Gráficos Sensor MPU6050', fontsize=19)
fig.subplots_adjust(wspace=0.32, hspace=0.44, left=0.076,
                    top=0.894, right=0.971, bottom=0.098)

ax1 = fig.add_subplot(231)
ax1.set_title("Aceleração eixo X($m/s^2$)", fontsize=11)
ax1.set_xlabel("Tempo")
ax1.set_ylabel("Amplitude")
ln1, = ax1.plot([], [], lw=0.9, color="sienna")

ax2 = fig.add_subplot(232)
ax2.set_title("Aceleração eixo Y($m/s^2$)", fontsize=11)
ax2.set_xlabel("Tempo")
ax2.set_ylabel("Amplitude")
ln2, = ax2.plot([], [], lw=0.9, color="green")

ax3 = fig.add_subplot(233)
ax3.set_title("Aceleração eixo Z($m/s^2$)", fontsize=11)
ax3.set_xlabel("Tempo")
ax3.set_ylabel("Amplitude")
ln3, = ax3.plot([], [], lw=0.9, color="red")

ax4 = fig.add_subplot(234)
ax4.set_title("Rotação em X [Roll] ($rad/s$)", fontsize=11)
ax4.set_xlabel("Tempo")
ax4.set_ylabel("Amplitude")
ln4, = ax4.plot([], [], lw=0.9, color="blue")

ax5 = fig.add_subplot(235)
ax5.set_title("Rotação em Y [Pitch] ($rad/s$)", fontsize=11)
ax5.set_xlabel("Tempo")
ax5.set_ylabel("Amplitude")
ln5, = ax5.plot([], [], lw=0.9, color="purple")

ax6 = fig.add_subplot(236)
ax6.set_title("Rotação em Z [Yaw] ($rad/s$)", fontsize=11)
ax6.set_xlabel("Tempo")
ax6.set_ylabel("Amplitude")
ln6, = ax6.plot([], [], lw=0.9, color="black")

# Axis que para plotar os gráficos
ln = [ln1, ln2, ln3, ln4, ln5, ln6]
ax = [ax1, ax2, ax3, ax4, ax5, ax6]

fila = coleta_dados.get_dados()

tx = []


def init():
    for i in range(6):
        tx.append(ax[i].text(40, int(fila[i][-1])+2, f"{fila[i][-1]}",
                             color=[0.3, 0.3, 0.5],
                             fontsize=9,
                             fontweight="bold"))
        ax[i].set_xlim(0, 50)
        ax[i].set_ylim(-15, 15)
        if i > 2:
            ax[i].set_xlim(0, 50)
            ax[i].set_ylim(-10, 10)

    return ln1, ln2, ln3, ln4, ln5, ln6


def update(frame):
    dados = coleta_dados.get_dados()
    t = np.arange(0, len(dados[0]))
    for i, ax in enumerate(ln):
        tx[i].set_y(int(dados[i][-1]+2))
        if (i <= 2):
            tx[i].set_text(f"{dados[i][-1]:.2f}\nm/s^2")
        else:
            tx[i].set_text(f"{dados[i][-1]:.2f}\nrad/s")
        ax.set_xdata(t)
        ax.set_ydata(dados[i])
    return ln1, ln2, ln3, ln4, ln5, ln6


# GUI
root = ctk.CTk()
root.title("Gráficos MPU6050")
# root.iconbitmap("mpu6050.ico")
root.geometry("1300x650+20+45")
label = ctk.CTkLabel(root, text="Realtime Animated Graphs").grid(column=1, row=0)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(column=1, row=1)


def quit():
    root.quit()
    root.destroy()


button = ctk.CTkButton(master=root, text="Quit", command=quit)
button.grid(column=0, row=1, padx=20, pady=10)


def aparencia_event(new_appearance_mode):
    ctk.set_appearance_mode(new_appearance_mode)


appearance_mode_menu = ctk.CTkOptionMenu(master=root,
                                         values=["Dark", "Light", "System"],
                                         command=aparencia_event)

appearance_mode_menu.grid(row=1, column=0, padx=20, pady=2, sticky="s")

ani = FuncAnimation(fig, update, init_func=init,
                    cache_frame_data=False, interval=20, blit=True)

root.mainloop()
