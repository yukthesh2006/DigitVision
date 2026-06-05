import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image, ImageOps
from streamlit_drawable_canvas import st_canvas
import os
import sys
import cv2

# =========================================================
# IMPORT STYLE
# =========================================================
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.style import apply, page_header, divider

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="DigitVision - Multi Digit",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply()

# Force sidebar always open
with st.sidebar:
    st.markdown("<style>[data-testid=\"stSidebarCollapseButton\"]{display:none!important;}</style>", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================
page_header(
    "",
    "Multi Digit",
    "Write numbers 0-99 with spacing between digits"
)

divider()

# =========================================================
# LOAD MODEL
# =========================================================
MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "mnist_trained_model.h5"
)

if os.path.exists(MODEL_PATH):
    model = tf.keras.models.load_model(MODEL_PATH)
    st.success("CNN Model Loaded Successfully ✔️")
else:
    st.error(f"Model not found at: {MODEL_PATH}")
    st.stop()

divider()

# =========================================================
# LAYOUT
# =========================================================
left, right = st.columns([1, 1], gap="large")

# =========================================================
# LEFT SIDE
# =========================================================
with left:

    st.markdown('<div class="dv-tag">INPUT</div>', unsafe_allow_html=True)
    st.markdown('<div class="dv-section-title">Draw a Number</div>', unsafe_allow_html=True)

    st.info("Leave small spacing between digits for better prediction.")

    invert = st.checkbox("Invert Colors")

    canvas = st_canvas(
        fill_color="black",
        stroke_width=14,
        stroke_color="white",
        background_color="black",
        width=500,
        height=250,
        drawing_mode="freedraw",
        key="canvas"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    predict_btn = st.button("PREDICT NUMBER", use_container_width=True)

    st.markdown("""
    <div style="margin-top:1.2rem;background:#0a1420;border:1px solid #0f2535;
                border-radius:12px;padding:1rem 1.2rem;">
        <div style="font-size:0.6rem;letter-spacing:0.2em;text-transform:uppercase;
                    color:#2a5a7a;margin-bottom:0.5rem;">Tips</div>
        <div style="font-size:0.76rem;color:#3a6a8a;line-height:1.8;">
            Leave a visible gap between digits<br>
            Write large and clear<br>
            Printed digits work best
        </div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# RIGHT SIDE
# =========================================================
with right:

    st.markdown('<div class="dv-tag">OUTPUT</div>', unsafe_allow_html=True)
    st.markdown('<div class="dv-section-title">Result</div>', unsafe_allow_html=True)

    # =====================================================
    # PREDICTION LOGIC
    # =====================================================
    if predict_btn:

        if canvas.image_data is not None:

            img = Image.fromarray(canvas.image_data.astype("uint8")).convert("L")

            if invert:
                img = ImageOps.invert(img)

            img_arr = np.array(img)

            _, thresh = cv2.threshold(img_arr, 50, 255, cv2.THRESH_BINARY)

            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[0])

            digits = []
            probabilities = []

            for contour in contours:

                x, y, w, h = cv2.boundingRect(contour)

                if w < 10 or h < 10:
                    continue

                padding = 10
                x1 = max(x - padding, 0)
                y1 = max(y - padding, 0)
                x2 = min(x + w + padding, thresh.shape[1])
                y2 = min(y + h + padding, thresh.shape[0])

                digit = thresh[y1:y2, x1:x2]
                h2, w2 = digit.shape

                if h2 > w2:
                    new_h = 20
                    new_w = int(w2 * (20 / h2))
                else:
                    new_w = 20
                    new_h = int(h2 * (20 / w2))

                digit = cv2.resize(digit, (new_w, new_h))

                canvas_digit = np.zeros((28, 28), dtype=np.uint8)
                x_offset = (28 - new_w) // 2
                y_offset = (28 - new_h) // 2
                canvas_digit[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = digit

                digit = canvas_digit.astype("float32") / 255.0
                digit = digit.reshape(1, 28, 28, 1)

                prediction = model.predict(digit, verbose=0)
                predicted_digit = np.argmax(prediction)

                digits.append(str(predicted_digit))
                probabilities.append(prediction[0])

            if digits:
                st.session_state["multi_result"] = "".join(digits)
                st.session_state["multi_probs"]  = probabilities
            else:
                st.warning("No digits detected. Try drawing larger with gaps between digits.")

        else:
            st.warning("Please draw something first.")

    # =====================================================
    # DISPLAY RESULT
    # =====================================================
    if "multi_result" not in st.session_state:

        st.markdown("""
        <div class="dv-pred-box" style="text-align:center;padding:3rem 2rem;">
            <div style="font-size:0.65rem;letter-spacing:0.2em;text-transform:uppercase;
                        color:#1a3a5a;margin-bottom:1rem;">WAITING FOR INPUT</div>
            <div style="font-family:'Unbounded',sans-serif;font-size:3rem;font-weight:900;
                        color:#0f2535;line-height:1;">_ _</div>
            <div style="font-size:0.7rem;color:#1a3a5a;margin-top:1rem;letter-spacing:0.1em;">
                Draw a number and press Predict
            </div>
        </div>
        """, unsafe_allow_html=True)

    else:

        result     = st.session_state["multi_result"]
        probs_list = st.session_state["multi_probs"]
        digit_word = "digit" if len(result) == 1 else "digits"

        st.markdown(f"""
        <div class="dv-pred-box live" style="text-align:center;padding:2rem;">
            <div style="font-size:0.62rem;letter-spacing:0.22em;text-transform:uppercase;
                        color:#2a5a7a;margin-bottom:0.5rem;">Predicted Number</div>
            <div style="font-size:5rem;font-weight:900;color:#00ffaa;line-height:1;">{result}</div>
            <div style="font-size:0.8rem;color:#4a7a9b;margin-top:1rem;">
                {len(result)} {digit_word} detected
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("CLEAR", use_container_width=True):
            st.session_state.pop("multi_result", None)
            st.session_state.pop("multi_probs", None)
            st.rerun()

divider()

if st.button("Back to Home"):
    st.switch_page("app.py")