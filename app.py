import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils.style import apply, page_header, divider, stat_card

st.set_page_config(
    page_title="DigitVision",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)
apply()

# Force sidebar open with a hidden element
with st.sidebar:
    st.markdown("""
    <style>
    [data-testid="stSidebarCollapseButton"] { display: none !important; }
    </style>
    <div style="height:0;overflow:hidden;"></div>
    """, unsafe_allow_html=True)

page_header("", "DigitVision", "Handwritten digit recognition powered by CNN + TensorFlow")
divider()

# Stats row
c1, c2, c3, c4, c5 = st.columns(5)
stats = [
    ("Test Accuracy", "99.1%",  "on MNIST test set"),
    ("Architecture",  "CNN",    "Conv2D x2 + Dense"),
    ("Dataset",       "MNIST",  "60,000 training samples"),
    ("Training",      "7 epochs", "early stopping"),
    ("Parameters",    "~200K",  "trainable weights"),
]
for col, (label, value, sub) in zip([c1,c2,c3,c4,c5], stats):
    with col:
        st.markdown(stat_card(label, value, sub), unsafe_allow_html=True)

divider()

st.markdown('<div class="dv-tag">Features</div>', unsafe_allow_html=True)
st.markdown('<div class="dv-section-title">What DigitVision Does</div>', unsafe_allow_html=True)

f1, f2, f3, f4 = st.columns(4)
features = [
    ("Single Digit", "Draw any digit 0-9 on the canvas and get an instant CNN prediction with full confidence breakdown."),
    ("Multi Digit",  "Write numbers 0-99 with spacing and the model detects each digit using OpenCV contour detection."),
    ("Metrics",      "Live training graphs showing accuracy and loss curves from your actual training run."),
    ("About",        "Architecture deep-dive, dataset overview, and tech stack documentation."),
]
for col, (title, desc) in zip([f1,f2,f3,f4], features):
    with col:
        st.markdown(f"""
        <div class="dv-card" style="min-height:160px;">
            <div class="dv-card-accent"></div>
            <div style="font-size:0.7rem;letter-spacing:0.18em;text-transform:uppercase;
                        color:#00ffaa;margin-bottom:0.6rem;">{title}</div>
            <div style="font-size:0.82rem;color:#4a7a9b;line-height:1.7;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

divider()

st.markdown('<div class="dv-tag">Navigate</div>', unsafe_allow_html=True)
st.markdown('<div class="dv-section-title">Get Started</div>', unsafe_allow_html=True)

n1, n2, n3, n4 = st.columns(4)
with n1:
    if st.button("Single Digit Predict", use_container_width=True):
        st.switch_page("pages/2_Predict.py")
with n2:
    if st.button("Multi Digit Predict", use_container_width=True):
        st.switch_page("pages/3_MultiDigit.py")
with n3:
    if st.button("Training Metrics", use_container_width=True):
        st.switch_page("pages/4_Metrics.py")
with n4:
    if st.button("About", use_container_width=True):
        st.switch_page("pages/5_About.py")