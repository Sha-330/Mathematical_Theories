import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Real life example: Weather forecast with 3 states - Sunny, Cloudy, Rainy
states = ['Sunny', 'Cloudy', 'Rainy']
# Transition probabilities for weather forecast for next day based on current day
P = np.array([[0.6, 0.3, 0.1],
              [0.3, 0.4, 0.3],
              [0.2, 0.5, 0.3]])

np.random.seed(42)

# Simulate weather states over days
n_days = 30
current_state = 0  # Start from Sunny
weather_sequence = [current_state]
for _ in range(n_days):
    current_state = np.random.choice([0, 1, 2], p=P[current_state])
    weather_sequence.append(current_state)

# Animation setup
fig, ax = plt.subplots(figsize=(8, 4))
ax.set_ylim(-0.5, 2.5)
ax.set_xlim(0, n_days)
ax.set_yticks([0, 1, 2])
ax.set_yticklabels(states)
ax.set_xlabel('Day')
ax.set_title('Weather Forecast Simulation Using Markov Chain')
line, = ax.plot([], [], marker='o', color='b', linestyle='-')

# Initialization function
def init():
    line.set_data([], [])
    return line,

# Animation update
def update(frame):
    x = list(range(frame + 1))
    y = weather_sequence[:frame + 1]
    line.set_data(x, y)
    return line,

# Create the animation object
ani = animation.FuncAnimation(fig, update, frames=n_days + 1, init_func=init, blit=True, interval=300, repeat=False)

# To save the animation as an MP4 file, we use the ani.save() method.
# A writer like 'ffmpeg' is required. This might take a few moments to run.
try:
    print("Saving animation...")
    # 'ffmpeg' is a common writer for MP4 files.
    ani.save('weather_forecast.gif', writer='pillow')
    print("Animation saved successfully as 'weather_forecast.mp4'.")
except Exception as e:
    print(f"Failed to save animation. Error: {e}")
    print("Check if 'ffmpeg' is installed and its path is correctly configured.")

# plt.show() is commented out to prevent the window from opening.
# If you want to see the animation in a window, uncomment the line below.
# plt.show()