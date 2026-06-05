import streamlit as st
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.style import apply, page_header, divider, stat_card

st.set_page_config(page_title="DigitVision - About", page_icon="", layout="wide")
apply()

page_header("// About", "DigitVision", "Architecture, dataset, and tech stack documentation")
divider()

# Overview
st.markdown('<div class="dv-tag">Overview</div>', unsafe_allow_html=True)
st.markdown('<div class="dv-section-title">What is DigitVision?</div>', unsafe_allow_html=True)

st.markdown("""
<div style="background:#0a1420;border:1px solid #0f2535;border-radius:12px;
            padding:1.6rem 2rem;max-width:800px;">
    <div style="font-size:0.88rem;color:#4a7a9b;line-height:1.9;">
        DigitVision is a production-grade handwritten digit recognition system built on a
        Convolutional Neural Network trained on the MNIST dataset. It supports both single digit
        and multi-digit (0-99) recognition using OpenCV contour detection to isolate individual
        digits from a canvas drawing.
    </div>
</div>
""", unsafe_allow_html=True)

divider()

# Architecture
st.markdown('<div class="dv-tag">Architecture</div>', unsafe_allow_html=True)
st.markdown('<div class="dv-section-title">CNN Model Design</div>', unsafe_allow_html=True)

a1, a2, a3, a4 = st.columns(4)
layers = [
    ("Conv Block 1", "Conv2D(32, 3x3)\nReLU activation\nMaxPool(2x2)", "Detects edges and basic curves"),
    ("Conv Block 2", "Conv2D(64, 3x3)\nReLU activation\nMaxPool(2x2)", "Detects complex digit shapes"),
    ("Dense Block",  "Flatten\nDense(128, ReLU)\nDropout(0.3)", "Classification with regularisation"),
    ("Output",       "Dense(10)\nSoftmax", "Probability for each digit 0-9"),
]
for col, (name, arch, desc) in zip([a1,a2,a3,a4], layers):
    with col:
        st.markdown(f"""
        <div class="dv-card" style="min-height:180px;">
            <div class="dv-card-accent"></div>
            <div style="font-size:0.6rem;letter-spacing:0.2em;text-transform:uppercase;
                        color:#00ffaa;margin-bottom:0.6rem;">{name}</div>
            <pre style="font-size:0.7rem;color:#00aaff;background:transparent;
                        border:none;padding:0;margin:0 0 0.6rem;line-height:1.6;">{arch}</pre>
            <div style="font-size:0.76rem;color:#2a5a7a;line-height:1.6;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

divider()

# Dataset
st.markdown('<div class="dv-tag">Dataset</div>', unsafe_allow_html=True)
st.markdown('<div class="dv-section-title">MNIST</div>', unsafe_allow_html=True)

d1, d2 = st.columns([1, 1], gap="large")
with d1:
    st.markdown("""
    <div style="background:#0a1420;border:1px solid #0f2535;border-radius:12px;padding:1.4rem 1.6rem;">
        <div style="font-size:0.6rem;letter-spacing:0.2em;text-transform:uppercase;
                    color:#2a5a7a;margin-bottom:1rem;">Dataset Facts</div>
        <div style="font-size:0.82rem;color:#4a7a9b;line-height:2;">
            60,000 training images<br>
            10,000 test images<br>
            28 x 28 pixels per image<br>
            Grayscale, normalised 0-1<br>
            10 classes (digits 0-9)<br>
            Balanced class distribution
        </div>
    </div>
    """, unsafe_allow_html=True)

with d2:
    ds1, ds2 = st.columns(2)
    dstats = [
        ("Train Samples", "60,000"),
        ("Test Samples",  "10,000"),
        ("Image Size",    "28x28"),
        ("Classes",       "10"),
    ]
    for col, (label, val) in zip([ds1, ds2, ds1, ds2], dstats):
        with col:
            st.markdown(stat_card(label, val), unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

divider()

# Tech Stack
st.markdown('<div class="dv-tag">Stack</div>', unsafe_allow_html=True)
st.markdown('<div class="dv-section-title">Technologies Used</div>', unsafe_allow_html=True)

t1, t2, t3, t4, t5 = st.columns(5)
techs = [
    ("TensorFlow 2.x",   "Deep learning framework for building and training the CNN model"),
    ("OpenCV",           "Computer vision library for contour detection in multi-digit mode"),
    ("Streamlit",        "Interactive web UI framework for the dashboard and canvas"),
    ("NumPy / Pillow",   "Array operations and image preprocessing pipeline"),
    ("Matplotlib",       "Training history visualisation and confidence bar charts"),
]
for col, (tech, desc) in zip([t1,t2,t3,t4,t5], techs):
    with col:
        st.markdown(f"""
        <div class="dv-card" style="min-height:160px;">
            <div class="dv-card-accent"></div>
            <div style="font-size:0.7rem;letter-spacing:0.18em;text-transform:uppercase;
                        color:#00ffaa;margin-bottom:0.5rem;">{tech}</div>
            <div style="font-size:0.76rem;color:#2a5a7a;line-height:1.7;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

divider()

# How it works
st.markdown('<div class="dv-tag">Pipeline</div>', unsafe_allow_html=True)
st.markdown('<div class="dv-section-title">How Prediction Works</div>', unsafe_allow_html=True)

steps = [
    ("01", "Draw",      "You draw a digit on the black canvas using your mouse or touch."),
    ("02", "Capture",   "Canvas image is captured as a NumPy array in RGBA format."),
    ("03", "Threshold", "OpenCV converts to grayscale and applies binary thresholding."),
    ("04", "Contours",  "Contour detection isolates each digit region with bounding boxes."),
    ("05", "Resize",    "Each digit region is resized to 28x28 with aspect ratio preserved."),
    ("06", "Predict",   "CNN outputs a 10-class softmax probability vector per digit."),
]

p1, p2, p3 = st.columns(3)
p4, p5, p6 = st.columns(3)

for col, (num, title, desc) in zip([p1,p2,p3,p4,p5,p6], steps):
    with col:
        st.markdown(f"""
        <div class="dv-card" style="min-height:120px;">
            <div class="dv-card-accent"></div>
            <div style="font-family:'Unbounded',sans-serif;font-size:1.4rem;font-weight:900;
                        color:#0f2535;margin-bottom:0.4rem;">{num}</div>
            <div style="font-size:0.7rem;letter-spacing:0.15em;text-transform:uppercase;
                        color:#00ffaa;margin-bottom:0.4rem;">{title}</div>
            <div style="font-size:0.76rem;color:#2a5a7a;line-height:1.6;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

divider()
if st.button("Back to Home"):
    st.switch_page("app.py")