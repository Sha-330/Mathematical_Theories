import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def tri_mf(x, a, b, c):
    y = np.zeros_like(x, dtype=float)
    idx1 = (x >= a) & (x <= b) & (b > a)
    y[idx1] = (x[idx1] - a) / (b - a)
    idx2 = (x >= b) & (x <= c) & (c > b)
    y[idx2] = (c - x[idx2]) / (c - b)
    y[x == b] = 1.0
    return np.clip(y, 0, 1)

x_in = np.linspace(0, 10, 500)
x_out = np.linspace(0, 80, 800)

low_in = tri_mf(x_in, 0, 2, 4)
med_in = tri_mf(x_in, 3, 5, 7)
high_in = tri_mf(x_in, 6, 8, 10)

short_out = tri_mf(x_out, 0, 20, 40)
med_out = tri_mf(x_out, 30, 45, 60)
long_out = tri_mf(x_out, 50, 65, 80)

rng = np.random.default_rng(42)
n_steps = 45
dirtiness = np.empty(n_steps)
dirtiness[0] = rng.uniform(0, 10)
for t in range(1, n_steps):
    dirtiness[t] = np.clip(dirtiness[t-1] + rng.normal(0, 0.8), 0, 10)

fig, ax = plt.subplots(figsize=(8, 4))
ax.set_xlim(0, 10)
ax.set_ylim(0, 1.05)
ax.set_xlabel('Dirtiness (0–10)')
ax.set_ylabel('Membership Degree (0–1)')
ax.set_title('Fuzzy Logic Controller: Dirtiness → Wash Time')

line_low, = ax.plot(x_in, low_in, label='Low Dirtiness')
line_med, = ax.plot(x_in, med_in, label='Medium Dirtiness')
line_high, = ax.plot(x_in, high_in, label='High Dirtiness')
ax.legend(loc='upper right')

vline = ax.axvline(dirtiness[0], linewidth=2)
pt_low, = ax.plot([], [], marker='o', linestyle='')
pt_med, = ax.plot([], [], marker='o', linestyle='')
pt_high, = ax.plot([], [], marker='o', linestyle='')
textbox = ax.text(0.02, 0.95, '', transform=ax.transAxes, va='top')

def infer_wash_minutes(x_d):
    mu_low = float(tri_mf(np.array([x_d]), 0, 2, 4))
    mu_med = float(tri_mf(np.array([x_d]), 3, 5, 7))
    mu_high = float(tri_mf(np.array([x_d]), 6, 8, 10))
    rule_short = np.minimum(mu_low, short_out)
    rule_med = np.minimum(mu_med, med_out)
    rule_long = np.minimum(mu_high, long_out)
    agg = np.maximum.reduce([rule_short, rule_med, rule_long])
    area = np.trapz(agg, x_out)
    if area == 0:
        centroid = 0.0
    else:
        centroid = np.trapz(agg * x_out, x_out) / area
    return mu_low, mu_med, mu_high, centroid

def init():
    vline.set_xdata([dirtiness[0], dirtiness[0]])
    pt_low.set_data([], [])
    pt_med.set_data([], [])
    pt_high.set_data([], [])
    textbox.set_text('')
    return (vline, pt_low, pt_med, pt_high, textbox)

def update(frame):
    x_d = dirtiness[frame]
    mu_low, mu_med, mu_high, minutes = infer_wash_minutes(x_d)
    vline.set_xdata([x_d, x_d])
    pt_low.set_data([x_d], [mu_low])
    pt_med.set_data([x_d], [mu_med])
    pt_high.set_data([x_d], [mu_high])
    textbox.set_text(f'Dirtiness: {x_d:4.2f}\n'
                     f'μ_low={mu_low:4.2f}, μ_med={mu_med:4.2f}, μ_high={mu_high:4.2f}\n'
                     f'→ Wash Time ≈ {minutes:4.1f} min')
    return (vline, pt_low, pt_med, pt_high, textbox)

ani = animation.FuncAnimation(
    fig, update, frames=n_steps, init_func=init, blit=True, interval=250, repeat=False
)

ani.save('fuzzy_washing_machine.gif', writer='pillow', fps=4)
