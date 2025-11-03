import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

def f(x, y):
    return x**2 + y**2

def grad_f(x, y):
    return np.array([2*x, 2*y])

x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x, y)
Z = f(X, Y)

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
ax.set_title('Gradient Descent Visualization (Multivariate Calculus)')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('f(X, Y)')

start = np.array([2.5, -2.0])
lr = 0.15
steps = 25
path = [start]
for _ in range(steps - 1):
    g = grad_f(*path[-1])
    new = path[-1] - lr * g
    path.append(new)
path = np.array(path)

line, = ax.plot([], [], [], 'r-', lw=2)
point, = ax.plot([], [], [], 'ro')

def init():
    line.set_data([], [])
    line.set_3d_properties([])
    point.set_data([], [])
    point.set_3d_properties([])
    return line, point

def update(i):
    line.set_data(path[:i+1, 0], path[:i+1, 1])
    line.set_3d_properties(f(path[:i+1, 0], path[:i+1, 1]))
    point.set_data(path[i, 0:1], path[i, 1:2])
    point.set_3d_properties(f(path[i, 0], path[i, 1]))
    return line, point

ani = animation.FuncAnimation(
    fig, update, frames=len(path), init_func=init, blit=True, interval=300, repeat=False
)

ani.save('multivariate_calculus.gif', writer='pillow', fps=5)
