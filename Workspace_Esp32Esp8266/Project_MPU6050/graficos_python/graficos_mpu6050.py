import tkinter as tk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
#                                               NavigationToolbar2Tk)
# from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from matplotlib import style
import numpy as np
import time

# Modulos criados
from coleta_dados import ColetaDados

style.use("ggplot")

# Objeto para coletar dados do sensor
coleta_dados = ColetaDados()
time.sleep(2)
root = tk.Tk()
root.title("Gráficos MPU6050")
root.configure(background='white')
# root.iconbitmap("mpu6050.ico")
root.geometry("1100x700+110+30")

fig = Figure(figsize=(10, 5), dpi=100)
fig.suptitle('Gráficos Sensor MPU6050', fontsize=16)
fig.subplots_adjust(wspace=0.295,
                    hspace=0.429,
                    left=0.076,
                    top=0.894,
                    right=0.971,
                    bottom=0.098)

ax1 = fig.add_subplot(231)
ax1.set_title("Aceleração eixo X($m/s^2$)", fontsize=11)
ax1.set_xlabel("Tempo")
ax1.set_ylabel("Amplitude")
ax1.set_xlim(0, 50)
ax1.set_ylim(-15, 15)
ln1 = ax1.plot([], [], lw=0.9, color="sienna")[0]

ax2 = fig.add_subplot(232)
ax2.set_title("Aceleração eixo Y($m/s^2$)", fontsize=11)
ax2.set_xlabel("Tempo")
ax2.set_xlim(0, 50)
ax2.set_ylim(-15, 15)
ax2.set_ylabel("Amplitude")
ln2 = ax2.plot([], [], lw=0.9, color="green")[0]

ax3 = fig.add_subplot(233)
ax3.set_title("Aceleração eixo Z($m/s^2$)", fontsize=11)
ax3.set_xlabel("Tempo")
ax3.set_ylabel("Amplitude")
ax3.set_xlim(0, 50)
ax3.set_ylim(-15, 15)
ln3 = ax3.plot([], [], lw=0.9, color="red")[0]

ax4 = fig.add_subplot(234)
ax4.set_title("Rotação em X [Roll] ($rad/s$)", fontsize=11)
ax4.set_xlabel("Tempo")
ax4.set_ylabel("Amplitude")
ax4.set_xlim(0, 50)
ax4.set_ylim(-10, 10)
ln4 = ax4.plot([], [], lw=0.9, color="blue")[0]

ax5 = fig.add_subplot(235)
ax5.set_title("Rotação em Y [Pitch] ($rad/s$)", fontsize=11)
ax5.set_xlabel("Tempo")
ax5.set_ylabel("Amplitude")
ax5.set_xlim(0, 50)
ax5.set_ylim(-10, 10)
ln5 = ax5.plot([], [], lw=0.9, color="purple")[0]

ax6 = fig.add_subplot(236)
ax6.set_title("Rotação em Z [Yaw] ($rad/s$)", fontsize=11)
ax6.set_xlabel("Tempo")
ax6.set_ylabel("Amplitude")
ax6.set_xlim(0, 50)
ax6.set_ylim(-10, 10)
ln6 = ax6.plot([], [], lw=0.9, color="black")[0]

# Axis que para plotar os gráficos
ln = [ln1, ln2, ln3, ln4, ln5, ln6]
ax = [ax1, ax2, ax3, ax4, ax5, ax6]

fila = coleta_dados.get_dados()

tx = []
for i in range(6):
    tx.append(ax[i].text(40, int(fila[i][-1])+2, f"{fila[i][-1]}",
                         color=[0.3, 0.3, 0.5],
                         fontsize=9,
                         fontweight="bold"))

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
canvas.draw()

# toolbar = NavigationToolbar2Tk(canvas, root)
# toolbar.update()
# canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


# def on_key(event):
#    print(f"You pressed {event.key}")
#    key_press_handler(event, canvas, toolbar)


# canvas.mpl_connect("key_press_event", on_key)


def quit():
    root.quit()
    root.destroy()


button = tk.Button(master=root, text="Quit",
                   compound="top", command=quit)
button.pack(side=tk.BOTTOM, padx=1, pady=1)


def graph_real_time():
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
    canvas.draw()
    root.after(1, graph_real_time)


root.after(1, graph_real_time)
root.mainloop()
