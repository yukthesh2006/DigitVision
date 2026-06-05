import streamlit as st
import pickle, os, sys
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.style import apply, page_header, divider, stat_card

st.set_page_config(page_title="DigitVision - Metrics", page_icon="🧠", layout="wide")
apply()

# Force sidebar always open
with st.sidebar:
    st.markdown("<style>[data-testid=\"stSidebarCollapseButton\"]{display:none!important;}</style>", unsafe_allow_html=True)

page_header("// Analytics", "Training Metrics", "Live accuracy and loss curves from your training run")
divider()

# =========================================================
# LOAD HISTORY
# =========================================================
HIST_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "training_history.pkl"
)

if not os.path.exists(HIST_PATH):
    st.error("training_history.pkl not found.")
    st.stop()

with open(HIST_PATH, "rb") as f:
    history = pickle.load(f)

epochs       = list(range(1, len(history["accuracy"]) + 1))
best_val_acc = max(history["val_accuracy"])
best_epoch   = history["val_accuracy"].index(best_val_acc) + 1

# =========================================================
# COMPUTE EXTRA METRICS
# =========================================================
# R² score: how well validation accuracy improves (1 - residual variance / total variance)
val_acc_arr  = np.array(history["val_accuracy"])
val_loss_arr = np.array(history["val_loss"])
acc_mean     = np.mean(val_acc_arr)
ss_tot       = np.sum((val_acc_arr - acc_mean) ** 2)
# Predicted = linear trend
x      = np.array(epochs, dtype=float)
coeffs = np.polyfit(x, val_acc_arr, 1)
y_pred = np.polyval(coeffs, x)
ss_res = np.sum((val_acc_arr - y_pred) ** 2)
r2     = 1 - (ss_res / ss_tot) if ss_tot > 0 else 1.0

# Overfitting gap (train acc - val acc, last epoch)
overfit_gap = (history["accuracy"][-1] - history["val_accuracy"][-1]) * 100

# Loss reduction %
loss_reduction = ((history["loss"][0] - history["loss"][-1]) / history["loss"][0]) * 100

# =========================================================
# SUMMARY STATS — 7 cards
# =========================================================
c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
stats = [
    ("Final Train Acc",   f"{history['accuracy'][-1]*100:.2f}%",   None),
    ("Final Val Acc",     f"{history['val_accuracy'][-1]*100:.2f}%", None),
    ("Best Val Acc",      f"{best_val_acc*100:.2f}%",               f"epoch {best_epoch}"),
    ("Final Train Loss",  f"{history['loss'][-1]:.4f}",             None),
    ("Final Val Loss",    f"{history['val_loss'][-1]:.4f}",         None),
    ("R² Score",          f"{r2:.4f}",                              "val acc trend fit"),
    ("Overfit Gap",       f"{overfit_gap:.2f}%",                    "train − val acc"),
]
for col, (label, value, sub) in zip([c1,c2,c3,c4,c5,c6,c7], stats):
    with col:
        st.markdown(stat_card(label, value, sub), unsafe_allow_html=True)

divider()

# =========================================================
# GRAPHS
# =========================================================
col_a, col_b = st.columns(2, gap="large")

def dark_fig(w=7, h=4):
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_facecolor("#06080d")
    ax.set_facecolor("#0a1420")
    for spine in ax.spines.values():
        spine.set_edgecolor("#0f2535")
    ax.tick_params(colors="#2a5a7a", labelsize=9)
    ax.grid(True, color="#0f2535", linewidth=0.6, linestyle="--")
    return fig, ax

with col_a:
    st.markdown('<div class="dv-tag">Chart</div>', unsafe_allow_html=True)
    st.markdown('<div class="dv-section-title">Accuracy</div>', unsafe_allow_html=True)
    fig1, ax1 = dark_fig()
    ax1.plot(epochs, history["accuracy"],
             label="Training Accuracy", linewidth=2.5, color="#00ffaa", marker="o", markersize=5)
    ax1.plot(epochs, history["val_accuracy"],
             label="Validation Accuracy", linewidth=2.5, color="#00aaff",
             marker="o", markersize=5, linestyle="--")
    # R² trend line
    ax1.plot(epochs, y_pred,
             label=f"Val Trend (R²={r2:.3f})", linewidth=1.2,
             color="#ffaa44", linestyle=":", alpha=0.8)
    ax1.set_xlabel("Epochs", color="#2a5a7a", fontsize=9)
    ax1.set_ylabel("Accuracy", color="#2a5a7a", fontsize=9)
    ax1.legend(facecolor="#0a1420", edgecolor="#0f2535", labelcolor="#4a7a9b", fontsize=8)
    ax1.set_xticks(epochs)
    st.pyplot(fig1)
    plt.close(fig1)

with col_b:
    st.markdown('<div class="dv-tag">Chart</div>', unsafe_allow_html=True)
    st.markdown('<div class="dv-section-title">Loss</div>', unsafe_allow_html=True)
    fig2, ax2 = dark_fig()
    ax2.plot(epochs, history["loss"],
             label="Training Loss", linewidth=2.5, color="#ff6b6b", marker="o", markersize=5)
    ax2.plot(epochs, history["val_loss"],
             label="Validation Loss", linewidth=2.5, color="#ffaa44",
             marker="o", markersize=5, linestyle="--")
    ax2.set_xlabel("Epochs", color="#2a5a7a", fontsize=9)
    ax2.set_ylabel("Loss", color="#2a5a7a", fontsize=9)
    ax2.legend(facecolor="#0a1420", edgecolor="#0f2535", labelcolor="#4a7a9b", fontsize=8)
    ax2.set_xticks(epochs)
    st.pyplot(fig2)
    plt.close(fig2)

divider()

# =========================================================
# EXTRA METRICS ROW
# =========================================================
st.markdown('<div class="dv-tag">Diagnostics</div>', unsafe_allow_html=True)
st.markdown('<div class="dv-section-title">Model Health</div>', unsafe_allow_html=True)

m1, m2, m3 = st.columns(3, gap="large")

with m1:
    st.markdown(f"""
    <div class="dv-card">
        <div class="dv-card-accent"></div>
        <div style="font-size:0.6rem;letter-spacing:0.2em;text-transform:uppercase;
                    color:#2a5a7a;margin-bottom:0.6rem;">R² Score (Val Accuracy Trend)</div>
        <div style="font-family:'Unbounded',sans-serif;font-size:2.2rem;font-weight:700;
                    color:#00ffaa;">{r2:.4f}</div>
        <div style="font-size:0.75rem;color:#4a7a9b;margin-top:0.5rem;line-height:1.6;">
            Measures how consistently validation accuracy improved over epochs.
            R²=1.0 means perfectly linear improvement.
            Your model scores <strong style="color:#00ffaa">{r2:.4f}</strong>
            — {'excellent' if r2 > 0.95 else 'good' if r2 > 0.85 else 'moderate'} trend.
        </div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    gap_color = "#00ffaa" if overfit_gap < 1.0 else "#ffaa44" if overfit_gap < 2.0 else "#ff6b6b"
    gap_label = "No overfitting" if overfit_gap < 1.0 else "Mild overfitting" if overfit_gap < 2.0 else "Overfitting detected"
    st.markdown(f"""
    <div class="dv-card">
        <div class="dv-card-accent"></div>
        <div style="font-size:0.6rem;letter-spacing:0.2em;text-transform:uppercase;
                    color:#2a5a7a;margin-bottom:0.6rem;">Overfitting Gap</div>
        <div style="font-family:'Unbounded',sans-serif;font-size:2.2rem;font-weight:700;
                    color:{gap_color};">{overfit_gap:.2f}%</div>
        <div style="font-size:0.75rem;color:#4a7a9b;margin-top:0.5rem;line-height:1.6;">
            Difference between final train and validation accuracy.
            <strong style="color:{gap_color}">{gap_label}</strong>.
            Values under 1% indicate a well-generalising model.
        </div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="dv-card">
        <div class="dv-card-accent"></div>
        <div style="font-size:0.6rem;letter-spacing:0.2em;text-transform:uppercase;
                    color:#2a5a7a;margin-bottom:0.6rem;">Loss Reduction</div>
        <div style="font-family:'Unbounded',sans-serif;font-size:2.2rem;font-weight:700;
                    color:#00aaff;">{loss_reduction:.1f}%</div>
        <div style="font-size:0.75rem;color:#4a7a9b;margin-top:0.5rem;line-height:1.6;">
            Training loss dropped from
            <strong style="color:#ff6b6b">{history['loss'][0]:.4f}</strong> to
            <strong style="color:#00ffaa">{history['loss'][-1]:.4f}</strong>
            across {len(epochs)} epochs — the model learned effectively.
        </div>
    </div>
    """, unsafe_allow_html=True)

divider()

# =========================================================
# PER-EPOCH TABLE — using st.columns instead of raw HTML table
# =========================================================
st.markdown('<div class="dv-tag">Data</div>', unsafe_allow_html=True)
st.markdown('<div class="dv-section-title">Per-Epoch Results</div>', unsafe_allow_html=True)

# Header row
h_ep, h_ta, h_va, h_tl, h_vl = st.columns([0.8, 1.3, 1.3, 1.3, 1.3])
header_style = "font-size:0.6rem;letter-spacing:0.18em;text-transform:uppercase;color:#2a5a7a;padding:0.4rem 0;border-bottom:1px solid #0f2535;"
with h_ep: st.markdown(f'<div style="{header_style}">Epoch</div>', unsafe_allow_html=True)
with h_ta: st.markdown(f'<div style="{header_style}">Train Acc</div>', unsafe_allow_html=True)
with h_va: st.markdown(f'<div style="{header_style}">Val Acc</div>', unsafe_allow_html=True)
with h_tl: st.markdown(f'<div style="{header_style}">Train Loss</div>', unsafe_allow_html=True)
with h_vl: st.markdown(f'<div style="{header_style}">Val Loss</div>', unsafe_allow_html=True)

for i, ep in enumerate(epochs):
    is_best   = (i + 1) == best_epoch
    row_bg    = "background:rgba(0,255,170,0.04);border-radius:6px;" if is_best else ""
    ep_color  = "#00ffaa" if is_best else "#4a7a9b"
    badge     = " ★" if is_best else ""

    c_ep, c_ta, c_va, c_tl, c_vl = st.columns([0.8, 1.3, 1.3, 1.3, 1.3])
    cell = f"font-size:0.78rem;padding:0.5rem 0;{row_bg}"

    with c_ep: st.markdown(f'<div style="{cell}color:{ep_color};">{ep}{badge}</div>', unsafe_allow_html=True)
    with c_ta: st.markdown(f'<div style="{cell}color:#00ffaa;">{history["accuracy"][i]*100:.2f}%</div>', unsafe_allow_html=True)
    with c_va: st.markdown(f'<div style="{cell}color:#00aaff;">{history["val_accuracy"][i]*100:.2f}%</div>', unsafe_allow_html=True)
    with c_tl: st.markdown(f'<div style="{cell}color:#ff6b6b;">{history["loss"][i]:.4f}</div>', unsafe_allow_html=True)
    with c_vl: st.markdown(f'<div style="{cell}color:#ffaa44;">{history["val_loss"][i]:.4f}</div>', unsafe_allow_html=True)

divider()

if st.button("Back to Home"):
    st.switch_page("app.py")