import numpy as np
import matplotlib.pyplot as plt



np.random.seed(7)

def f(P):
    a= 1.4
    b=0.3
    x, y = P[:, 0], P[:, 1]
    x_next = 1-a*x**2+y
    y_next = b*x
    return np.column_stack([x_next, y_next])

s_n = np.array([0.2, -0.1])

K = 8  # number of surrounding points
angles = np.random.rand(K)*2*np.pi
r = 0.3
R = np.random.rand(K) * r                     
dirs = np.column_stack([np.cos(angles), np.sin(angles)]) 
neighbors_n = s_n + R[:, None] * dirs 
neighbors_n += 0.005*np.random.randn(K, 2) 

# 3) We "know" where the surrounding points go at the next step
neighbors_n1 = f(neighbors_n)

# 4) Predict s_{n+1} as the average of the neighbors' next-step positions
s_n1_hat = neighbors_n1.mean(axis=0)

# 5) Also compute the actual s_{n+1}
s_n1_actual = f(s_n.reshape(1, 2)).ravel()
s_n1_actual = s_n1_actual + np.array([0.03, -0.02])  # optional small offset

# 6) Nonlinear prediction error gamma
gamma_vec = s_n1_actual - s_n1_hat
gamma = np.linalg.norm(gamma_vec)

#plotiing 
fig, ax = plt.subplots(figsize=(14, 12))

theta = np.linspace(0, 2*np.pi, 300)
ax.plot(s_n[0] + r*np.cos(theta), s_n[1] + r*np.sin(theta), lw=1, alpha=0.35)

# Time n: neighbors and s_n
ax.scatter(neighbors_n[:, 0], neighbors_n[:, 1], s=55, alpha=0.75, label="Neighbors at $n$")
ax.scatter([s_n[0]], [s_n[1]], s=130, marker="o", edgecolor="k", linewidth=1.0,
           label="Reference state $s_n$")

# Arrows from neighbors_n to neighbors_n1 (known next step)
for p0, p1 in zip(neighbors_n, neighbors_n1):
    ax.annotate("", xy=p1, xytext=p0,
                arrowprops=dict(arrowstyle="->", lw=1.2, alpha=0.55))

# Time n+1: neighbors' next positions
ax.scatter(neighbors_n1[:, 0], neighbors_n1[:, 1], s=55, marker="x", linewidth=2,
           label="Neighbors at $n+1$")

# Predicted and actual s_{n+1}
ax.scatter([s_n1_hat[0]], [s_n1_hat[1]], s=220, marker="*", edgecolor="k", linewidth=0.8,
           label=r"Predicted $\hat{s}_{n+1}=\langle f(\text{neighbors})\rangle$")
ax.scatter([s_n1_actual[0]], [s_n1_actual[1]], s=220, marker="*", edgecolor="k", linewidth=0.8,
           label=r"Actual $s_{n+1}$")

# Error vector gamma from prediction to actual
ax.annotate("", xy=s_n1_actual, xytext=s_n1_hat,
            arrowprops=dict(arrowstyle="<->", lw=2.5))
mid = 0.5 * (s_n1_hat + s_n1_actual)
ax.text(mid[0], mid[1], rf"$\gamma$", fontsize=20,
        ha="left", va="bottom")

# Labels / styling
plt.rcParams.update({
    "font.size": 25,        # base font
    "axes.titlesize": 20,   # title
    "axes.labelsize": 20,   # x/y labels
    "xtick.labelsize":20,  # x tick labels
    "ytick.labelsize": 20,  # y tick labels
    "legend.fontsize": 20,  # legend text
})
ax.set_xlabel("$x$",fontsize=20)
ax.set_ylabel("$y$",fontsize=20)
ax.axhline(0, lw=0.8, alpha=0.3)
ax.axvline(0, lw=0.8, alpha=0.3)
ax.set_aspect("equal", adjustable="datalim")
ax.grid(True, alpha=0.25)
ax.legend(loc="best", framealpha=0.9)

plt.tight_layout()


plt.savefig("./project_konrad/figures/nonlinear_prediction_error.png", dpi=300)
plt.show()