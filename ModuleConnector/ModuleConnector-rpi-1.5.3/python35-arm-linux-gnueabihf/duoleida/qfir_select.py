from sympy import*
from sympy import *
from scipy import signal
fig, ax = plt.subplots()

dot, = ax.plot([], [], 'ro')

def init():
    x = [-2, 2]
    y = [0, 0]
    l=ax.scatter(x, y, color='b')
    plt.axis([-3, 3, 0, 5])
    plt.grid(True)
    return l

def gen_dot():
    for i in np.linspace(0, 2*np.pi, 200):
        newdot = [i, np.sin(i)]
        yield newdot

def update_dot(newd):
    dot.set_data(newd[0], newd[1])
    return dot,

ani = animation.FuncAnimation(fig, update_dot, frames = gen_dot, interval = 100, init_func=init)


plt.show()

signal.identify