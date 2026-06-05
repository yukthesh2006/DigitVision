import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image, ImageOps
from streamlit_drawable_canvas import st_canvas
import matplotlib.pyplot as plt
import os
import cv2
import pickle

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------
st.set_page_config(
    page_title="Handwritten Digit Recognition",
    layout="wide"
)

# ------------------------------------------------
# DARK THEME
# ------------------------------------------------
st.markdown("""
<style>

.stApp {
    background-color: #0E1117;
    color: white;
}

h1, h2, h3 {
    color: #00FFAA;
}

.stButton>button {
    background-color: #00FFAA;
    color: black;
    border-radius: 10px;
    height: 3em;
    font-size: 18px;
    font-weight: bold;
}

.stButton>button:hover {
    background-color: #00CC88;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# TITLE
# ------------------------------------------------
st.title("🧠 Handwritten Digit Recognition System")

st.write("CNN + TensorFlow + Streamlit")

# ------------------------------------------------
# LOAD MODEL
# ------------------------------------------------
MODEL_PATH = "mnist_trained_model.h5"

if os.path.exists(MODEL_PATH):

    model = tf.keras.models.load_model(MODEL_PATH)

    st.success("CNN Model Loaded Successfully ✔️")

else:

    st.error("Model not found! Run project.py first.")
    st.stop()

# ------------------------------------------------
# LOAD TRAINING HISTORY
# ------------------------------------------------
history = None

if os.path.exists("training_history.pkl"):

    with open("training_history.pkl", "rb") as f:

        history = pickle.load(f)

# ------------------------------------------------
# MODEL PERFORMANCE
# ------------------------------------------------
st.markdown("---")

st.subheader("📊 CNN Model Performance")

if history is not None:

    col1, col2 = st.columns(2)

    # ---------------- ACCURACY GRAPH ----------------
    with col1:

        fig1, ax1 = plt.subplots(figsize=(7,4))

        fig1.patch.set_facecolor("#0E1117")
        ax1.set_facecolor("#111827")

        ax1.plot(
            history["accuracy"],
            label="Training Accuracy",
            linewidth=3,
            color="cyan"
        )

        ax1.plot(
            history["val_accuracy"],
            label="Validation Accuracy",
            linewidth=3,
            color="lime"
        )

        ax1.set_title(
            "Accuracy Graph",
            color="white",
            fontsize=16
        )

        ax1.set_xlabel(
            "Epochs",
            color="white"
        )

        ax1.set_ylabel(
            "Accuracy",
            color="white"
        )

        ax1.tick_params(colors="white")

        ax1.legend()

        ax1.grid(True)

        st.pyplot(fig1)

    # ---------------- LOSS GRAPH ----------------
    with col2:

        fig2, ax2 = plt.subplots(figsize=(7,4))

        fig2.patch.set_facecolor("#0E1117")
        ax2.set_facecolor("#111827")

        ax2.plot(
            history["loss"],
            label="Training Loss",
            linewidth=3,
            color="orange"
        )

        ax2.plot(
            history["val_loss"],
            label="Validation Loss",
            linewidth=3,
            color="red"
        )

        ax2.set_title(
            "Loss Graph",
            color="white",
            fontsize=16
        )

        ax2.set_xlabel(
            "Epochs",
            color="white"
        )

        ax2.set_ylabel(
            "Loss",
            color="white"
        )

        ax2.tick_params(colors="white")

        ax2.legend()

        ax2.grid(True)

        st.pyplot(fig2)

else:

    st.warning("training_history.pkl file not found.")

# ------------------------------------------------
# DRAW SECTION
# ------------------------------------------------
st.markdown("---")

st.subheader("✏️ Draw Digits (0–99)")

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

# ------------------------------------------------
# PREDICTION
# ------------------------------------------------
if st.button("Predict"):

    if canvas.image_data is not None:

        # Convert image
        img = Image.fromarray(
            canvas.image_data.astype("uint8")
        ).convert("L")

        if invert:

            img = ImageOps.invert(img)

        img = np.array(img)

        # Threshold
        _, thresh = cv2.threshold(
            img,
            50,
            255,
            cv2.THRESH_BINARY
        )

        # Find contours
        contours, _ = cv2.findContours(
            thresh,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        # Sort left to right
        contours = sorted(
            contours,
            key=lambda c: cv2.boundingRect(c)[0]
        )

        digits = []

        probabilities = []

        for contour in contours:

            x, y, w, h = cv2.boundingRect(contour)

            # Ignore tiny noise
            if w < 10 or h < 10:

                continue

            padding = 10

            x1 = max(x - padding, 0)
            y1 = max(y - padding, 0)

            x2 = min(x + w + padding, thresh.shape[1])
            y2 = min(y + h + padding, thresh.shape[0])

            digit = thresh[y1:y2, x1:x2]

            # Resize while maintaining aspect ratio
            h, w = digit.shape

            if h > w:

                new_h = 20
                new_w = int(w * (20 / h))

            else:

                new_w = 20
                new_h = int(h * (20 / w))

            digit = cv2.resize(
                digit,
                (new_w, new_h)
            )

            # Create blank 28x28 image
            canvas_digit = np.zeros(
                (28, 28),
                dtype=np.uint8
            )

            x_offset = (28 - new_w) // 2
            y_offset = (28 - new_h) // 2

            canvas_digit[
                y_offset:y_offset+new_h,
                x_offset:x_offset+new_w
            ] = digit

            digit = canvas_digit

            # Normalize
            digit = digit.astype("float32") / 255.0

            # CNN input shape
            digit = digit.reshape(
                1,
                28,
                28,
                1
            )

            # Predict
            prediction = model.predict(
                digit,
                verbose=0
            )

            predicted_digit = np.argmax(prediction)

            digits.append(str(predicted_digit))

            probabilities.append(prediction[0])

        # Final output
        result = "".join(digits)

        st.success(f"Predicted Number: {result}")

        # ------------------------------------------------
        # CONFIDENCE GRAPHS
        # ------------------------------------------------
        st.markdown("---")

        st.subheader("📈 Prediction Confidence")

        for i, probs in enumerate(probabilities):

            st.write(f"Digit {i+1}")

            fig3, ax3 = plt.subplots(figsize=(8,3))

            fig3.patch.set_facecolor("#0E1117")
            ax3.set_facecolor("#111827")

            ax3.bar(
                range(10),
                probs,
                color="cyan"
            )

            ax3.set_xticks(range(10))

            ax3.set_xlabel(
                "Digits",
                color="white"
            )

            ax3.set_ylabel(
                "Probability",
                color="white"
            )

            ax3.tick_params(colors="white")

            st.pyplot(fig3)

    else:

        st.warning("Please draw something first.")

# ------------------------------------------------
# FOOTER
# ------------------------------------------------
st.markdown("---")

st.caption(
    "Handwritten Digit Recognition using CNN, TensorFlow, OpenCV and Streamlit"
)