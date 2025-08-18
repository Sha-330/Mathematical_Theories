import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

states = ['Sunny', 'Cloudy', 'Rainy']
P = np.array([[0.6, 0.3, 0.1],
              [0.3, 0.4, 0.3],
              [0.2, 0.5, 0.3]])

np.random.seed(42)

n_days = 30
current_state = 0 
weather_sequence = [current_state]
for _ in range(n_days):
    current_state = np.random.choice([0, 1, 2], p=P[current_state])
    weather_sequence.append(current_state)

fig, ax = plt.subplots(figsize=(8, 4))
ax.set_ylim(-0.5, 2.5)
ax.set_xlim(0, n_days)
ax.set_yticks([0, 1, 2])
ax.set_yticklabels(states)
ax.set_xlabel('Day')
ax.set_title('Weather Forecast Simulation Using Markov Chain')
line, = ax.plot([], [], marker='o', color='b', linestyle='-')

def init():
    line.set_data([], [])
    return line,

def update(frame):
    x = list(range(frame + 1))
    y = weather_sequence[:frame + 1]
    line.set_data(x, y)
    return line,

ani = animation.FuncAnimation(fig, update, frames=n_days + 1, init_func=init, blit=True, interval=300, repeat=False)

try:
    print("Saving animation...")
    
    ani.save('weather_forecast.gif', writer='pillow')
    print("Animation saved successfully as 'weather_forecast.mp4'.")
except Exception as e:
    print(f"Failed to save animation. Error: {e}")
    print("Check if 'ffmpeg' is installed and its path is correctly configured.")

