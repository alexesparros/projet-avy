# Fonctions de visualisation pour le projet AVY

import matplotlib.pyplot as plt
import numpy as np

def plot_radar(categories, values, username):
    """Affiche un radar chart du profil joueur."""
    values = list(values)
    values += values[:1]
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, values, linewidth=2)
    ax.fill(angles, values, alpha=0.25)
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=10)
    ax.set_title(f"🧠 Profil de {username}", size=14, pad=20)
    return fig 